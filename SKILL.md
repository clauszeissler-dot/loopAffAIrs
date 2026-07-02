---
name: loop-library
description: "Baukasten für iterative Qualitäts-Loops (Builder -> Verifier -> Stop-Bedingung) über beliebige Domänen: Content/Text, Dokumente/Design, Code/Security. Nutze diesen Skill, wenn ein Entwurf so lange automatisch überarbeitet werden soll, bis er eine prüfbare Qualitätsschwelle erreicht — bei 'lass das durch eine Iterationsschleife laufen', 'kritisier das und verbessere es', 'baue mir einen Quality-Loop', 'soll das automatisch nachschärfen' oder beim Aufsetzen eines neuen Projekts mit wiederkehrender Qualitätsprüfung."
allowed-tools: ["Read", "Glob", "Grep", "WebSearch", "WebFetch", "Agent"]
metadata:
  author: Claus Zeißler
  version: 1.0.0
  license: CC BY 4.0
---

# Loop Library — Builder/Verifier-Engine für Qualitäts-Loops

Ein domänenunabhängiges Muster, um einen Entwurf (Text, Design, Code) automatisiert so lange zu überarbeiten, bis er eine definierte, prüfbare Qualitätsschwelle erreicht — statt einmalig zu generieren und zu hoffen.

Inspiriert von Matthew Bermans (Forward Future) Loop Library — siehe [Inspiration & verwandte Projekte](#inspiration--verwandte-projekte). Dieses Repo ist kein Klon davon: es konzentriert sich auf drei zusammenhängende, sofort nutzbare Domänen-Rezepte (Content, Dokumente/Design, Code/Security) statt auf eine lose Sammlung einzelner Ops-Loops, und ist auf Claude-Code-Hooks zugeschnitten, die den Loop standardmäßig anstoßen statt ihn nur als Prompt bereitzustellen.

## Die drei Bausteine

Jeder Loop besteht aus genau drei Rollen:

1. **Builder** — erzeugt oder überarbeitet den Entwurf.
2. **Verifier** — unabhängiger, adversarial geframter Kritiker ("finde, was nicht stimmt", nicht "ist das gut?"). Prüft gegen eine konkrete, dokumentierte Checkliste — nie nach Bauchgefühl.
3. **Loop-Controller** — entscheidet nach jeder Verifier-Runde: weiter oder stop, anhand einer der drei Stop-Bedingungen unten. Die Fixed-Cap-Bedingung ist IMMER aktiv, egal welche andere Bedingung zusätzlich gilt — sie ist die Notbremse gegen Endlosschleifen.

## Stop-Bedingungen (kombinierbar)

| Bedingung | Wann nutzen | Beispiel |
|---|---|---|
| **Fixed Cap** | Immer, als Backstop | Max. 3 Runden, danach Abbruch mit Eskalation an den Menschen |
| **Quality-Streak** | Wenn "einmal sauber" nicht reicht (Flakiness, Regression-Risiko) | N=1 bei günstig korrigierbaren Domänen (Text, Design); N=2 bei teuren Fehlern (Production-Code) |
| **Severity-Threshold** | Wenn nicht JEDES Finding den Loop blockieren soll | Nur CRITICAL/HIGH stoppen den Loop, MEDIUM/LOW werden reported, aber lassen den Build durch |

**Quality-Streak** statt fixer Rundenzahl: Der Loop stoppt nicht nach "Runde X", sondern nach **N aufeinanderfolgenden sauberen Verifier-Durchläufen**. Das verhindert sowohl verfrühtes Stoppen (ein zufällig guter Durchlauf reicht nicht) als auch unnötige Extra-Runden (sobald die Qualität steht, wird nicht weiter "verschlimmbessert").

**Severity-Threshold**: Der Verifier liefert Findings mit Schweregrad. Nur Findings ab der konfigurierten Schwelle zählen für den Stop — alles darunter wird dokumentiert, blockiert aber nicht. Verhindert, dass ein Loop an Kleinigkeiten hängen bleibt, während kritische Probleme trotzdem nie durchrutschen.

## Trigger-Modi

| Modus | Verhalten |
|---|---|
| **Self-Paced** | Der Loop wählt sein eigenes Tempo und stoppt selbst, sobald die Stop-Bedingung erfüllt ist. Standard für alle drei Domänen-Rezepte unten. |
| **Fixed-Interval** | Läuft mechanisch auf einem festen Zeitplan (z. B. wöchentlich), ohne sich selbst zu beenden — für wiederkehrende Prüfungen, nicht für "bis fertig". Beispiel: ein wöchentlicher Check, ob sich die externe Wissensbasis eines Verifiers geändert hat (siehe Content-Loop unten). |

Hook-Enforcement statt Hook-Ausführung: Ein Claude-Code-Hook ist ein einfacher Shell-Befehl, kein Agenten-Orchestrator. Ein Hook soll den Loop daher **anstoßen** (Kontext injizieren: "nutze jetzt den passenden Loop"), nicht selbst die Builder/Verifier-Runden fahren. Die eigentliche Iteration läuft als normale Agenten-Session oder als orchestriertes Multi-Agent-Workflow. Konkretes, sofort nutzbares Beispiel für diesen Ansatz: [`examples/loop-enforcer.py`](examples/loop-enforcer.py) — ein UserPromptSubmit-Hook, der per Regex die Content- bzw. Dokument/Design-Domäne erkennt und non-blocking einen Hinweis auf das passende Rezept injiziert, ohne selbst zu orchestrieren.

## Domänen-Rezepte

### 1. Content-Critique-Loop (Text/Marketing-Copy)

- **Builder:** schreibt den Entwurf (Post, Caption, Skript).
- **Verifier:** prüft gegen eine **faktenbasierte, regelmäßig aktualisierte** Checkliste aus öffentlich geteilten Daten echter, nachweislich erfolgreicher Stimmen im jeweiligen Kanal — nicht aus Bauchgefühl oder einer einmal eingefrorenen internen Vorlage. Wichtig: die Wissensbasis selbst veraltet, deshalb ein **Fixed-Interval-Loop** (z. B. wöchentlich), der die Quelle gegenprüft und die interne Checkliste aktualisiert, BEVOR der nächste Content-Loop sie nutzt.
- **Stop-Bedingung:** Quality-Streak N=1 (ein sauberer Durchlauf reicht — Text ist günstig korrigierbar), Fixed Cap N=2 als Backstop.

### 2. Dokument/Design-Critique-Loop (Slides, Präsentationen, Dokumente)

- **Builder:** erstellt den Entwurf gegen ein dokumentiertes Design-Kit (Farb-/Typo-Tokens + Layout-Archetypen + Checkliste — kein Bauchgefühl, kein proprietäres Drittsystem als Blackbox). Das Design-Kit selbst entsteht über eine **Abfrage** (Farbpalette, Typografie, Effekte, Footer-Logik, Layout-Archetypen, Format), nicht durch Kopieren eines fremden Kits — siehe [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md) für den vollständigen Fragenkatalog samt Beispiel-Kit.
- **Verifier:** prüft Fidelity gegen das (per Abfrage erstellte) Design-Kit, nicht gegen einen subjektiven Geschmack.
- **Stop-Bedingung:** Quality-Streak N=1, Fixed Cap N=2 als Backstop.

### 3. Code-Security-Quality-Loop

- **Builder:** schreibt/ändert Code.
- **Verifier:** Security-Audit bei konfiguriertem **Severity-Threshold** (z. B. nur CRITICAL/HIGH blockieren) + separates Code-Quality-Review. Ergänzend: ein ständig aktiver, kostenloser Pattern-Check (reine Regex, kein LLM-Call) bei jedem Edit/Write als frühe Instant-Warnung — der eigentliche Verifier-Durchlauf bleibt der tiefe, bewusst ausgelöste Audit. Als konkreter, sofort einsetzbarer Verifier-Skill für diese Rolle eignet sich [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) (Read-Only Security-Audit-Agent, CC BY 4.0, gleicher Autor) — Deploy-Gate-Modus liefert bereits einen konfigurierbaren Severity-Threshold.
- **Stop-Bedingung:** Fixed Cap N=3 als Backstop, zusätzlich Quality-Streak N=2 (zwei aufeinanderfolgende saubere Audits) für höhere Sicherheit, da Produktionscode-Fehler teuer sind. Wird der Fixed Cap erreicht, ohne dass der Threshold unterschritten wird, greift die Eskalation an den Menschen — siehe [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) für ein ausgearbeitetes Quality-Gate-/Eskalations-Framework (EU-AI-Act-Art.-14-Bezug), das sich direkt als Vorlage für diesen Schritt eignet.

## Lernschleife: wohin mit Erkenntnissen aus dem Loop?

Hybrides Routing, keine neue Parallelstruktur:

- **Taktische, domänenspezifische Erkenntnisse** (z. B. "bei Slide 1 braucht es immer 2 statt 1 Runde") gehören in die jeweilige Domänen-Doku/den Domänen-Skill selbst.
- **Cross-cutting Erkenntnisse über die Loop-Mechanik** (z. B. "Quality-Streak N=2 verbessert die Trefferquote bei Code messbar, bei Text nicht") gehören in eine globale Lernkartei mit Reifegrad-Gate: `beobachtet` → `bestätigt` (mehrfach aufgetreten) → `promoted` (als feste Regel übernommen). Kein Eintrag ohne echten, generalisierbaren Treffer — neutrale Durchläufe tragen nichts bei.

## Setup

Siehe [SETUP.md](SETUP.md) für die konkreten Schritte (Skill kopieren, Hook verdrahten, optionalen Fixed-Interval-Loop einrichten).

## Für KI-Agenten

Siehe [AGENTS.md](AGENTS.md), wenn ein KI-Coding-Agent (Claude Code, Codex, Gemini CLI o. ae.) dieses Repo selbstständig lesen und anwenden soll.

## Verwandte eigene Projekte

Zwei weitere Skills desselben Autors (ebenfalls CC BY 4.0), die sich direkt mit der Loop Library kombinieren lassen:

- [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) — Framework für menschliche Aufsicht (EU AI Act Art. 14), insbesondere der Quality-Gate-Modus passt als Vorlage für die Eskalation-an-den-Menschen beim Fixed-Cap-Stop.
- [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) — Read-Only Security-Audit-Agent, direkt als Verifier-Skill für den Code-Security-Quality-Loop (Rezept 3 oben) nutzbar.

## Inspiration & verwandte Projekte

Die Grundidee — Trigger/Action/Verify/Stop als wiederholbares Muster, mit Self-Paced- vs. Fixed-Interval-Modus — ist durch [Matthew Bermans Loop Library (Forward Future)](https://signals.forwardfuture.ai/loop-library/) angestoßen worden. Konkret hat uns das **Quality-Streak-Stop** (N aufeinanderfolgende saubere Durchläufe statt fixer Rundenzahl) und das **Severity-Threshold-gated Adversarial-Review**-Muster überzeugt, beides haben wir übernommen und in unsere drei Domänen-Rezepte übersetzt.

Empfehlenswerte Alternativen/Ergänzungen, falls du über Content/Dokumente/Code-Security hinaus willst:

- [Forward Future Loop Library](https://signals.forwardfuture.ai/loop-library/) — die Originalquelle, 22+ produktionsnahe Ops-Loops (Docs-Sweeps, Test-Coverage, Deployment, SEO, u. v. m.) für Software-Teams.
- [az9713/loop-library](https://github.com/az9713/loop-library) — Community-Mirror mit copy-paste-fertigen `/loop`-Prompts für Claude Code, basierend auf Bermans Liste.

Wir haben deren konkrete Loop-Texte/Tabellen nicht übernommen (kein offenes Lizenzfeld bei az9713/loop-library zum Zeitpunkt der Recherche) — nur das allgemeine, nicht schutzfähige Konzept in eigenen Worten neu beschrieben und domänenspezifisch ausgearbeitet.
