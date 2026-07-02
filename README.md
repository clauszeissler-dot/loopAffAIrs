<p align="center">
  <img src="assets/banner.png" alt="Loop Library" width="100%">
</p>

# Loop Library

**Ein Baukasten, der Entwürfe automatisch so lange überarbeitet, bis sie eine prüfbare Qualitätsschwelle erreichen — statt einmal zu generieren und zu hoffen.**

> 🇬🇧 *English version: [README.en.md](README.en.md)*

---

## Warum das Ganze?

KI-Tools generieren in einem Schuss — gut, mittelmäßig, manchmal daneben, ohne dass irgendjemand (Mensch oder Maschine) systematisch nachschärft. Die Loop Library liefert das fehlende Stück: ein **Builder/Verifier-Muster** mit klar definierten Stop-Bedingungen, das einen Entwurf so lange iteriert, bis er eine dokumentierte Qualitätsschwelle erreicht — egal ob Text, Design oder Code.

---

## Das Wichtigste in einem Satz

> Drei Rollen (**Builder → Verifier → Loop-Controller**), drei kombinierbare Stop-Bedingungen (**Fixed Cap, Quality-Streak, Severity-Threshold**), zwei Trigger-Modi (**Self-Paced, Fixed-Interval**) — und drei sofort nutzbare Domänen-Rezepte als Startpunkt.

---

## Die drei Stop-Bedingungen

| Bedingung | Wann nutzen |
|---|---|
| **Fixed Cap** | Immer aktiv, als Notbremse gegen Endlosschleifen |
| **Quality-Streak** | Wenn ein einzelner sauberer Durchlauf nicht reicht — stoppt erst nach N aufeinanderfolgenden sauberen Verifier-Runden |
| **Severity-Threshold** | Wenn nicht jedes Finding blockieren soll — nur Findings ab konfigurierter Schwere stoppen den Loop, der Rest wird nur dokumentiert |

---

## Drei Domänen-Rezepte als Startpunkt

| Domäne | Builder | Verifier | Stop-Bedingung |
|---|---|---|---|
| **Content/Text** | schreibt den Entwurf | prüft gegen eine faktenbasierte, regelmäßig aktualisierte Checkliste (siehe Fixed-Interval-Modus) | Quality-Streak N=1 + Fixed Cap N=2 |
| **Dokument/Design** | baut gegen ein dokumentiertes Design-Kit (Farb-/Typo-Tokens, Layout-Archetypen) | prüft Fidelity gegen das Kit | Quality-Streak N=1 + Fixed Cap N=2 |
| **Code/Security** | schreibt/ändert Code | Security-Audit bei Severity-Threshold + Code-Quality-Review, ergänzt um einen kostenlosen Instant-Pattern-Check (Regex, kein LLM-Call) | Fixed Cap N=3 + Quality-Streak N=2 |

Die Rezepte sind Vorlagen, keine fertigen Skills — sie brauchen projektspezifisches Wissen (eure Brand-Voice, euer Design-System, euer Security-Standard), um wirklich zu greifen. Details in [`SKILL.md`](SKILL.md). Für das Dokument/Design-Rezept gibt es eine vollständige, generische Referenzimplementierung inkl. Fragenkatalog: [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md).

---

## Wie nutze ich das?

### A) Als Skill in Claude Code
Lege [`SKILL.md`](SKILL.md) in deinen Skills-Ordner (`~/.claude/skills/loop-library/`). Danach genügt ein Auftrag wie *„lass das durch eine Iterationsschleife laufen"* oder *„baue mir einen Quality-Loop für X"*.

### B) Als Methodik (kein Setup)
Auch ohne Tool nützlich: eine vollständige Checkliste, wie man iterative Qualitäts-Loops sauber aufsetzt — Rollentrennung, Stop-Bedingungen, Hook-vs-Orchestrierung.

### C) Konkrete Einrichtung
Siehe [`SETUP.md`](SETUP.md) für die genauen Schritte (Skill kopieren, optionalen Pattern-Check-Hook verdrahten, Fixed-Interval-Loop einrichten).

### D) Für KI-Agenten
Siehe [`AGENTS.md`](AGENTS.md) — eine Arbeitsanweisung speziell für einen KI-Coding-Agenten, der dieses Repo selbstständig anwenden soll.

---

## Für wen ist das?

- **Solo-Builder & Teams**, die KI-Entwürfe (Text, Design, Code) nicht einmalig generieren, sondern systematisch nachschärfen wollen.
- **Alle, die Claude-Code-Hooks** nutzen, um Qualitätsschleifen standardmäßig anzustoßen, statt sie manuell aufzurufen.

---

## Inhalt dieses Repos

| Datei | Was drin ist |
|---|---|
| [`README.md`](README.md) | Diese Einführung (Deutsch) |
| [`README.en.md`](README.en.md) | English version |
| [`SKILL.md`](SKILL.md) | Das vollständige Loop-Engine-Wissen (auch als Claude-Code-Skill nutzbar) |
| [`SETUP.md`](SETUP.md) | Konkrete Einrichtungsschritte |
| [`AGENTS.md`](AGENTS.md) | Anweisung für KI-Coding-Agenten |
| [`examples/security-pattern-check.py`](examples/security-pattern-check.py) | Beispiel-Hook für den Code-Security-Quality-Loop (Instant-Regex-Checks, kein LLM-Call) |
| [`examples/loop-enforcer.py`](examples/loop-enforcer.py) | Beispiel-Hook für Content-/Dokument-Design-Loop (UserPromptSubmit, erkennt die Domäne und stößt den passenden Loop an, orchestriert nicht selbst) |
| [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md) | Referenzimplementierung für den Dokument/Design-Critique-Loop (generischer Fragenkatalog + Verifier-Checkliste) |
| [`LICENSE`](LICENSE) | Lizenz (CC BY 4.0) |
| [`NOTICE`](NOTICE) | Attributions-Hinweis — trägt auch die Quellenangabe zur Inspiration |

---

## Verwandte eigene Projekte

Zwei weitere Skills desselben Autors (ebenfalls CC BY 4.0), die sich direkt mit der Loop Library kombinieren lassen:

- [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) — Framework für menschliche Aufsicht (EU AI Act Art. 14); der Quality-Gate-Modus passt als Vorlage für die Eskalation an den Menschen beim Fixed-Cap-Stop.
- [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) — Read-Only Security-Audit-Agent, direkt als Verifier-Skill für den Code-Security-Quality-Loop nutzbar.

---

## Inspiration & verwandte Projekte

Die Grundidee — Trigger/Action/Verify/Stop, Self-Paced vs. Fixed-Interval — wurde durch [Matthew Bermans Loop Library (Forward Future)](https://signals.forwardfuture.ai/loop-library/) angestoßen. Übernommen haben wir das **Quality-Streak-Stop** und das **Severity-Threshold-gated Adversarial-Review** als Konzepte, in eigenen Worten neu beschrieben und auf drei zusammenhängende Domänen-Rezepte angewandt — keine Texte/Tabellen kopiert (siehe [`NOTICE`](NOTICE)).

Empfehlenswert, wenn ihr über Content/Dokumente/Code-Security hinaus wollt:

- [Forward Future Loop Library](https://signals.forwardfuture.ai/loop-library/) — die Originalquelle, 22+ produktionsnahe Ops-Loops für Software-Teams (Docs-Sweeps, Test-Coverage, Deployment, SEO, u. v. m.).
- [az9713/loop-library](https://github.com/az9713/loop-library) — Community-Mirror mit copy-paste-fertigen `/loop`-Prompts für Claude Code.

---

## Lizenz & Urheber

© Claus Zeißler. Lizenziert unter **[Creative Commons CC BY 4.0](LICENSE)** — frei nutzbar, weitergebbar und anpassbar, solange der Urheber genannt wird.

Mehr: [affairs-consulting.de](https://www.affairs-consulting.de)
