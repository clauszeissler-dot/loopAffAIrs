# Setup

Konkrete Schritte, um die Loop Library in einem Claude-Code-Setup einzurichten.

## 1. Skill installieren

```bash
mkdir -p ~/.claude/skills/loop-library
cp SKILL.md SETUP.md AGENTS.md ~/.claude/skills/loop-library/
```

Damit ist der Skill als domänenunabhängiges Wissen verfügbar — Claude zieht ihn, wenn ein Auftrag nach einem iterativen Quality-Loop klingt.

## 2. Instant-Pattern-Check als Hook (optional, für den Code-Security-Quality-Loop)

Ein leichter, kostenloser PostToolUse-Hook gibt sofortiges Feedback bei riskanten Code-Mustern (Regex, kein LLM-Call). Beispielskript: [`examples/security-pattern-check.py`](examples/security-pattern-check.py).

```bash
mkdir -p ~/.claude/hooks
cp examples/security-pattern-check.py ~/.claude/hooks/
```

In `~/.claude/settings.json` unter `hooks.PostToolUse` ergänzen:

```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    {
      "type": "command",
      "command": "python3 \"$HOME/.claude/hooks/security-pattern-check.py\"",
      "timeout": 10,
      "statusMessage": "Security-Pattern-Check"
    }
  ]
}
```

## 2b. Domänen-Enforcer als Hook (optional, für Content-/Dokument-Design-Loop)

Ein leichter UserPromptSubmit-Hook erkennt per Regex, ob ein Auftrag nach der Content- oder der Dokument/Design-Domäne klingt, und injiziert non-blocking einen Hinweis auf das passende Rezept — er orchestriert nichts selbst (siehe „Hook-Enforcement statt Hook-Ausführung" in `SKILL.md`). Beispielskript: [`examples/loop-enforcer.py`](examples/loop-enforcer.py).

```bash
mkdir -p ~/.claude/hooks
cp examples/loop-enforcer.py ~/.claude/hooks/
```

In `~/.claude/settings.json` unter `hooks.UserPromptSubmit` ergänzen:

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "python3 \"$HOME/.claude/hooks/loop-enforcer.py\"",
      "timeout": 5,
      "statusMessage": "Loop-Enforcer (Domänen-Check)"
    }
  ]
}
```

Die Keyword-Patterns (`DOMAIN_PATTERNS`) und Rezept-Namen sind an dieses Repo angelehnt — bei eigenen/zusätzlichen Domänen entsprechend anpassen.

## 3. Fixed-Interval-Loop einrichten (optional, für den Content-Critique-Loop)

Wenn der Verifier eines Content-Loops gegen eine externe, sich ändernde Wissensbasis prüft (z. B. ein jährlich/regelmäßig aktualisierter Best-Practice-Report für einen Social-Kanal), lohnt sich ein wiederkehrender Refresh statt einer live-WebSearch bei jedem einzelnen Loop-Durchlauf:

- In Claude Code: `/schedule` nutzen, um einen wiederkehrenden Auftrag ("prüfe, ob sich Quelle X geändert hat, aktualisiere die interne Checkliste") auf Wochenbasis einzurichten.
- Alternativ ein Cron-/Launchd-Job, der eine Claude-Code-Session headless mit demselben Auftrag startet.

## 4. Domänen-Rezept anwenden

Die drei Rezepte in `SKILL.md` (Content, Dokument/Design, Code-Security) sind Vorlagen, keine fertigen Skills. Konkretes Vorgehen pro Domäne:

1. Eine domänenspezifische Checkliste/Wissensbasis dokumentieren (Brand-Voice-Regeln, Design-Kit, Security-Pattern-Liste — was auch immer der Verifier prüfen soll).
2. Die passende Stop-Bedingung wählen (Fixed Cap ist Pflicht, Quality-Streak und/oder Severity-Threshold je nach Domäne dazu).
3. Builder- und Verifier-Rolle als zwei getrennte Agenten-Aufrufe fahren (z. B. über das Workflow-Tool: `pipeline`/`agent()` mit Builder- und Verifier-Prompt), nicht in einer einzigen Antwort vermischen — der Verifier muss unabhängig prüfen können.
