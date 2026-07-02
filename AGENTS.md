# AGENTS.md — Anweisung für KI-Coding-Agenten

Diese Datei richtet sich an ein LLM/einen Coding-Agenten (Claude Code, Codex, Gemini CLI, Cursor o. ae.), das dieses Repo liest, um die Loop Library in einem Projekt anzuwenden. Sie ist KEIN Marketing-Text — sie ist eine Arbeitsanweisung.

## Wann anwenden

Wende dieses Framework an, wenn der Nutzer einen Entwurf will, der automatisch so lange überarbeitet wird, bis er eine prüfbare Qualitätsschwelle erreicht — nicht bei einer einmaligen Generierung "so gut wie es eben wird".

## Was zu tun ist

1. **Lies `SKILL.md` vollständig**, bevor du irgendetwas baust. Die drei Bausteine (Builder/Verifier/Loop-Controller) und die drei Stop-Bedingungen (Fixed Cap/Quality-Streak/Severity-Threshold) sind nicht optional — jeder Loop braucht mindestens die Fixed Cap, sonst droht eine Endlosschleife.
2. **Identifiziere die Domäne** des Auftrags (Text/Content, Dokument/Design, Code) und nutze das passende Rezept aus `SKILL.md` als Ausgangspunkt — nicht blind kopieren, sondern auf den konkreten Kontext anpassen (z. B. die tatsächliche Brand-Voice/das tatsächliche Design-System/den tatsächlichen Security-Standard des Projekts einsetzen, falls vorhanden). Für den Code-Security-Quality-Loop und die Eskalation-an-den-Menschen bei Fixed Cap gibt es fertige Vorlagen, siehe "Verwandte eigene Projekte" in `SKILL.md`.
3. **Trenne Builder und Verifier strikt.** Der Verifier darf nicht derselbe Kontext/Agentenlauf sein, der gerade gebaut hat — sonst prüfst du dich selbst und übersiehst dieselben blinden Flecken. Nutze getrennte Agenten-Aufrufe (z. B. über ein Workflow-/Orchestrierungs-Tool, falls verfügbar) oder zumindest einen expliziten Rollenwechsel mit adversarialem Framing ("finde, was nicht stimmt").
4. **Wähle die Stop-Bedingung explizit, bevor der Loop startet** — nicht implizit "ein paar Runden, dann gut sein lassen". Sag dem Nutzer (oder dokumentiere), welche Bedingung gilt und warum.
5. **Bei Fixed-Interval-Loops:** diese terminieren sich nicht selbst. Plane das entsprechend (z. B. über einen Scheduler/Cron), nicht als einmaligen manuellen Lauf.
6. **Hooks orchestrieren nicht selbst.** Wenn du einen Hook für dieses Framework einrichtest, lass ihn Kontext injizieren oder ein einfaches, deterministisches Skript ausführen (z. B. den Pattern-Check) — keine mehrstufige Agenten-Logik in einen Shell-Hook pressen.
7. **Lernschleife respektieren:** Wenn während eines Loops eine generalisierbare Erkenntnis auftaucht (z. B. "diese Stop-Bedingung passt hier nicht"), dokumentiere sie an der richtigen Stelle (siehe "Lernschleife" in `SKILL.md`) statt sie stillschweigend zu ignorieren oder einmalig zu fixen.

## Was NICHT zu tun ist

- Nicht den Loop ohne Fixed Cap laufen lassen.
- Nicht Builder-Output ungeprüft als "fertig" melden, nur weil eine Runde gelaufen ist — der Verifier muss tatsächlich ausgeführt worden sein.
- Nicht die drei Domänen-Rezepte als vollständige, fertige Skills missverstehen — sie sind Vorlagen, die projektspezifisches Wissen (Brand-Voice, Design-Kit, Security-Standard) noch brauchen, um nutzbar zu sein.

## Weiterführend

- `SETUP.md` für konkrete Installationsschritte.
- `README.md` (Deutsch) / `README.en.md` (Englisch) für den menschenlesbaren Kontext und die Herkunft des Frameworks.
