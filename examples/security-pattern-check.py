#!/usr/bin/env python3
"""Schlanker PostToolUse-Hook: instant Regex-Warnungen bei Edit/Write/MultiEdit.
Ersetzt Layer 1 ("Pattern-based rules") des deinstallierten security-guidance-Plugins.
Keine LLM-Calls, keine Git-Baseline, kein State — reine Regex/Substring-Checks, < 1s.
Volle Klartext+Technisch-Erklaerungen liegen im Skill ai-code-security-audit; hier nur
ein kurzer Reminder zum sofortigen Gegensteuern waehrend des Edits.
"""
import json
import re
import sys

_JS_EXTS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte")
_PY_EXTS = (".py", ".pyi", ".ipynb")
_DOC_EXTS = (".md", ".mdx", ".txt", ".rst")

# Quelle: claude-plugins-official/security-guidance/hooks/patterns.py (Layer 1),
# uebernommen 2026-06-30, Reminder auf eine Zeile gekuerzt.
PATTERNS = [
    {"name": "child_process_exec", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": ["child_process.exec", "execSync("],
     "msg": "child_process.exec()/execSync() koennen Command Injection erlauben — execFile()/spawn() mit Argument-Array statt Shell-String nutzen."},
    {"name": "new_function_injection", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": ["new Function"],
     "msg": "new Function() mit String-Interpolation ist Code Injection — niemals ungeprueften String in den Function-Body interpolieren."},
    {"name": "eval_injection", "regex": r"(?<![a-zA-Z0-9_\.])eval\(",
     "msg": "eval() fuehrt beliebigen Code aus — JSON.parse()/ast.literal_eval()/sicherer Expression-Parser statt eval()."},
    {"name": "react_dangerously_set_html", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": ["dangerouslySetInnerHTML"],
     "msg": "dangerouslySetInnerHTML kann XSS erlauben — Inhalt vorher mit DOMPurify sanitizen."},
    {"name": "innerHTML_xss", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": [".innerHTML =", ".innerHTML="],
     "msg": "innerHTML mit ungeprueftem Inhalt ist ein XSS-Sink — textContent oder DOMPurify nutzen."},
    {"name": "outerHTML_xss", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": [".outerHTML =", ".outerHTML="],
     "msg": "outerHTML ist ein XSS-Sink wie innerHTML — textContent oder DOMPurify nutzen."},
    {"name": "insertAdjacentHTML_xss", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": [".insertAdjacentHTML("],
     "msg": "insertAdjacentHTML ist ein XSS-Sink — insertAdjacentText() oder DOMPurify nutzen."},
    {"name": "document_write_xss", "path_filter": lambda p: p.endswith(_JS_EXTS),
     "substrings": ["document.write"],
     "msg": "document.write() ist XSS-anfaellig — createElement()/appendChild() nutzen."},
    {"name": "pickle_deserialization", "path_filter": lambda p: p.endswith(_PY_EXTS),
     "regex": r"(?<![a-zA-Z0-9_])pickle\.(loads?|Unpickler)\b|(?<![a-zA-Z0-9_])pkl_load\(",
     "msg": "pickle.load(s)/Unpickler aus ungeprueften Quellen erlaubt Remote Code Execution — JSON oder schema-validierte Deserialisierung (pydantic/msgspec) nutzen."},
    {"name": "marshal_loads", "regex": r"\bmarshal\.loads?\s*\(",
     "msg": "marshal.load(s) ist unsicher wie pickle — schema-validierte Deserialisierung nutzen."},
    {"name": "shelve_open", "regex": r"\bshelve\.open\s*\(",
     "msg": "shelve.open() nutzt pickle intern — unsicher bei ungeprueften Quellen."},
    {"name": "pickle_variants_load", "regex": r"\b(cPickle|cloudpickle|dill)\.(load|loads)\s*\(",
     "msg": "cPickle/cloudpickle/dill .load(s) sind unsicher wie pickle."},
    {"name": "pickle_wrapper_load",
     "regex": r"\bjoblib\.load\s*\(|\b(?:pd|pandas)\.read_pickle\s*\(|\.cloudpickle_load\s*\(|\b(?:np|numpy)\.load\s*\([^)\n]{0,200}allow_pickle\s*=\s*True",
     "msg": "joblib.load/pd.read_pickle/np.load(allow_pickle=True) entpacken intern pickle — unsicher bei ungeprueften Quellen."},
    {"name": "os_system_injection", "path_filter": lambda p: p.endswith(_PY_EXTS),
     "regex": r"\bos\.system\s*\(", "substrings": ["from os import system"],
     "msg": "os.system() ist ein Command-Injection-Sink — subprocess.run([...]) mit Argument-Liste nutzen."},
    {"name": "python_subprocess_shell",
     "regex": r"subprocess\.(?:run|call|Popen|check_output|check_call)\(.*shell\s*=\s*True",
     "msg": "subprocess mit shell=True erlaubt Command Injection — Argumente als Liste ohne shell=True uebergeben."},
    {"name": "go_exec_shell_injection", "regex": r'exec\.Command\(\s*"(?:sh|bash|/bin/sh|/bin/bash)"',
     "msg": "exec.Command mit sh/bash erlaubt Command Injection — Argumente direkt ohne Shell uebergeben."},
    {"name": "unsafe_yaml_load", "regex": r"\byaml\.load\s*\((?![^)\n]{0,80}\bSafe)",
     "msg": "yaml.load() ohne SafeLoader fuehrt beliebigen Python-Code aus — yaml.safe_load() nutzen."},
    {"name": "yaml_unsafe_load_variants", "regex": r"(?:\byaml\.unsafe_load|\.yaml_unsafe_load)\s*\(",
     "msg": "yaml.unsafe_load() ist wie yaml.load() ohne SafeLoader — yaml.safe_load() nutzen."},
    {"name": "torch_unsafe_load",
     "regex": r"(?:\btorch\.load|\.torch_load)\s*\((?![^)\n]{0,200}weights_only\s*=\s*True)",
     "msg": "torch.load() ohne weights_only=True entpackt intern pickle — RCE-Risiko bei ungeprueften Dateien."},
    {"name": "node_createcipher_no_iv", "regex": r"\bcrypto\.(createCipher|createDecipher)\b",
     "msg": "crypto.createCipher/createDecipher sind unsicher (kein IV, MD5-KDF) — createCipheriv/createDecipheriv nutzen."},
    {"name": "aes_ecb_mode", "regex": r"\bAES\.MODE_ECB\b|\bmodes\.ECB\s*\(|[\"']aes-\d+-ecb[\"']",
     "msg": "AES-ECB-Modus leakt Klartextstruktur — AES-GCM oder AES-CBC+HMAC nutzen."},
    {"name": "tls_verification_disabled",
     "regex": r"\bverify\s*=\s*False\b|rejectUnauthorized\s*:\s*false|InsecureSkipVerify\s*:\s*true|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*[\"']?0|ssl\._create_unverified_context|check_hostname\s*=\s*False",
     "msg": "TLS-Verifikation deaktiviert — ermoeglicht MITM-Angriffe."},
    {"name": "xml_unsafe_parse",
     "regex": r"\b(xml\.etree\.ElementTree|ElementTree|ET)\.(parse|fromstring|XML)\s*\(|\bminidom\.(parse|parseString)\s*\(|\bxml\.sax\.(parse|make_parser)\b",
     "msg": "Python-Standard-XML-Parser sind anfaellig fuer XXE/Billion-Laughs — defusedxml.ElementTree nutzen."},
    {"name": "script_src_without_sri",
     "regex": r'<script\s+(?![^>]{0,400}integrity\s*=)[^>]{0,200}src\s*=\s*["\'](?:https?:)?//[^"\']{1,300}["\'][^>]{0,100}>',
     "msg": "Externes <script> ohne integrity=\"sha384-...\" — Subresource Integrity gegen CDN-Kompromittierung ergaenzen."},
    {"name": "github_actions_workflow",
     "path_check": lambda p: ".github/workflows/" in p and (p.endswith(".yml") or p.endswith(".yaml")),
     "msg": "GitHub-Actions-Workflow: ungeprueften Issue-/PR-Input (z.B. github.event.issue.title) nie direkt in run: interpolieren — ueber env: mit Quoting fuehren."},
]


def extract_content(tool_name, tool_input):
    if tool_name == "Write":
        return tool_input.get("content", "")
    if tool_name == "Edit":
        return tool_input.get("new_string", "")
    if tool_name == "MultiEdit":
        return " ".join(e.get("new_string", "") for e in tool_input.get("edits", []))
    return ""


def check(file_path, content):
    if file_path.endswith(_DOC_EXTS):
        return []  # Doku/Markdown kann Pattern-Namen als Text nennen, ohne dass Code vorliegt
    hits = []
    for p in PATTERNS:
        if "path_filter" in p and not p["path_filter"](file_path):
            continue
        matched = False
        if "path_check" in p and p["path_check"](file_path):
            matched = True
        if not matched and "substrings" in p and content:
            matched = any(s in content for s in p["substrings"])
        if not matched and "regex" in p and content:
            try:
                matched = bool(re.search(p["regex"], content))
            except re.error:
                pass
        if matched:
            hits.append(p["msg"])
    return hits


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    file_path = (tool_input.get("file_path") or "").lstrip("/")
    content = extract_content(tool_name, tool_input)
    if not file_path:
        sys.exit(0)

    hits = check(file_path, content)
    if not hits:
        sys.exit(0)

    lines = "\n".join(f"⚠️ {m}" for m in hits)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Security-Pattern-Check ({file_path}):\n{lines}",
        }
    }))


if __name__ == "__main__":
    main()
