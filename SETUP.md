# Setup

Konkrete Schritte, um die Loop Library in einem Claude-Code-Setup einzurichten.

## 1. Skill installieren

```bash
mkdir -p ~/.claude/skills/loop-library
cp SKILL.md SETUP.md AGENTS.md ~/.claude/skills/loop-library/
```

Damit ist der Skill als domaenenunabhaengiges Wissen verfuegbar — Claude zieht ihn, wenn ein Auftrag nach einem iterativen Quality-Loop klingt.

## 2. Instant-Pattern-Check als Hook (optional, fuer den Code-Security-Quality-Loop)

Ein leichter, kostenloser PostToolUse-Hook gibt sofortiges Feedback bei riskanten Code-Mustern (Regex, kein LLM-Call). Beispielskript: [`examples/security-pattern-check.py`](examples/security-pattern-check.py).

```bash
mkdir -p ~/.claude/hooks
cp examples/security-pattern-check.py ~/.claude/hooks/
```

In `~/.claude/settings.json` unter `hooks.PostToolUse` ergaenzen:

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

## 3. Fixed-Interval-Loop einrichten (optional, fuer den Content-Critique-Loop)

Wenn der Verifier eines Content-Loops gegen eine externe, sich aendernde Wissensbasis prueft (z. B. ein jaehrlich/regelmaessig aktualisierter Best-Practice-Report fuer einen Social-Kanal), lohnt sich ein wiederkehrender Refresh statt einer live-WebSearch bei jedem einzelnen Loop-Durchlauf:

- In Claude Code: `/schedule` nutzen, um einen wiederkehrenden Auftrag ("prüfe, ob sich Quelle X geändert hat, aktualisiere die interne Checkliste") auf Wochenbasis einzurichten.
- Alternativ ein Cron-/Launchd-Job, der eine Claude-Code-Session headless mit demselben Auftrag startet.

## 4. Domaenen-Rezept anwenden

Die drei Rezepte in `SKILL.md` (Content, Dokument/Design, Code-Security) sind Vorlagen, keine fertigen Skills. Konkretes Vorgehen pro Domaene:

1. Eine domaenenspezifische Checkliste/Wissensbasis dokumentieren (Brand-Voice-Regeln, Design-Kit, Security-Pattern-Liste — was auch immer der Verifier pruefen soll).
2. Die passende Stop-Bedingung waehlen (Fixed Cap ist Pflicht, Quality-Streak und/oder Severity-Threshold je nach Domaene dazu).
3. Builder- und Verifier-Rolle als zwei getrennte Agenten-Aufrufe fahren (z. B. ueber das Workflow-Tool: `pipeline`/`agent()` mit Builder- und Verifier-Prompt), nicht in einer einzigen Antwort vermischen — der Verifier muss unabhaengig pruefen koennen.
