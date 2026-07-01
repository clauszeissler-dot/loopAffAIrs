# AGENTS.md — Anweisung fuer KI-Coding-Agenten

Diese Datei richtet sich an ein LLM/einen Coding-Agenten (Claude Code, Codex, Gemini CLI, Cursor o. ae.), das dieses Repo liest, um die Loop Library in einem Projekt anzuwenden. Sie ist KEIN Marketing-Text — sie ist eine Arbeitsanweisung.

## Wann anwenden

Wende dieses Framework an, wenn der Nutzer einen Entwurf will, der automatisch so lange ueberarbeitet wird, bis er eine pruefbare Qualitaetsschwelle erreicht — nicht bei einer einmaligen Generierung "so gut wie es eben wird".

## Was zu tun ist

1. **Lies `SKILL.md` vollstaendig**, bevor du irgendetwas baust. Die drei Bausteine (Builder/Verifier/Loop-Controller) und die drei Stop-Bedingungen (Fixed Cap/Quality-Streak/Severity-Threshold) sind nicht optional — jeder Loop braucht mindestens die Fixed Cap, sonst droht eine Endlosschleife.
2. **Identifiziere die Domaene** des Auftrags (Text/Content, Dokument/Design, Code) und nutze das passende Rezept aus `SKILL.md` als Ausgangspunkt — nicht blind kopieren, sondern auf den konkreten Kontext anpassen (z. B. die tatsaechliche Brand-Voice/das tatsaechliche Design-System/den tatsaechlichen Security-Standard des Projekts einsetzen, falls vorhanden). Fuer den Code-Security-Quality-Loop und die Eskalation-an-den-Menschen bei Fixed Cap gibt es fertige Vorlagen, siehe "Verwandte eigene Projekte" in `SKILL.md`.
3. **Trenne Builder und Verifier strikt.** Der Verifier darf nicht derselbe Kontext/Agentenlauf sein, der gerade gebaut hat — sonst pruefst du dich selbst und uebersiehst dieselben blinden Flecken. Nutze getrennte Agenten-Aufrufe (z. B. ueber ein Workflow-/Orchestrierungs-Tool, falls verfuegbar) oder zumindest einen expliziten Rollenwechsel mit adversarialem Framing ("finde, was nicht stimmt").
4. **Waehle die Stop-Bedingung explizit, bevor der Loop startet** — nicht implizit "ein paar Runden, dann gut sein lassen". Sag dem Nutzer (oder dokumentiere), welche Bedingung gilt und warum.
5. **Bei Fixed-Interval-Loops:** diese terminieren sich nicht selbst. Plane das entsprechend (z. B. ueber einen Scheduler/Cron), nicht als einmaligen manuellen Lauf.
6. **Hooks orchestrieren nicht selbst.** Wenn du einen Hook fuer dieses Framework einrichtest, lass ihn Kontext injizieren oder ein einfaches, deterministisches Skript ausfuehren (z. B. den Pattern-Check) — keine mehrstufige Agenten-Logik in einen Shell-Hook pressen.
7. **Lernschleife respektieren:** Wenn waehrend eines Loops eine generalisierbare Erkenntnis auftaucht (z. B. "diese Stop-Bedingung passt hier nicht"), dokumentiere sie an der richtigen Stelle (siehe "Lernschleife" in `SKILL.md`) statt sie stillschweigend zu ignorieren oder einmalig zu fixen.

## Was NICHT zu tun ist

- Nicht den Loop ohne Fixed Cap laufen lassen.
- Nicht Builder-Output ungeprueft als "fertig" melden, nur weil eine Runde gelaufen ist — der Verifier muss tatsaechlich ausgefuehrt worden sein.
- Nicht die drei Domaenen-Rezepte als vollstaendige, fertige Skills missverstehen — sie sind Vorlagen, die projektspezifisches Wissen (Brand-Voice, Design-Kit, Security-Standard) noch brauchen, um nutzbar zu sein.

## Weiterfuehrend

- `SETUP.md` fuer konkrete Installationsschritte.
- `README.md` (Deutsch) / `README.en.md` (Englisch) fuer den menschenlesbaren Kontext und die Herkunft des Frameworks.
