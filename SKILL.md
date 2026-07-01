---
name: loop-library
description: "Baukasten fuer iterative Qualitaets-Loops (Builder -> Verifier -> Stop-Bedingung) ueber beliebige Domaenen: Content/Text, Dokumente/Design, Code/Security. Nutze diesen Skill, wenn ein Entwurf so lange automatisch ueberarbeitet werden soll, bis er eine pruefbare Qualitaetsschwelle erreicht — bei 'lass das durch eine Iterationsschleife laufen', 'kritisier das und verbessere es', 'baue mir einen Quality-Loop', 'soll das automatisch nachschaerfen' oder beim Aufsetzen eines neuen Projekts mit wiederkehrender Qualitaetspruefung."
allowed-tools: ["Read", "Glob", "Grep", "WebSearch", "WebFetch", "Agent"]
metadata:
  author: Claus Zeißler
  version: 1.0.0
  license: CC BY 4.0
---

# Loop Library — Builder/Verifier-Engine fuer Qualitaets-Loops

Ein domaenenunabhaengiges Muster, um einen Entwurf (Text, Design, Code) automatisiert so lange zu ueberarbeiten, bis er eine definierte, pruefbare Qualitaetsschwelle erreicht — statt einmalig zu generieren und zu hoffen.

Inspiriert von Matthew Bermans (Forward Future) Loop Library — siehe [Inspiration & verwandte Projekte](#inspiration--verwandte-projekte). Dieses Repo ist kein Klon davon: es konzentriert sich auf drei zusammenhaengende, sofort nutzbare Domaenen-Rezepte (Content, Dokumente/Design, Code/Security) statt auf eine lose Sammlung einzelner Ops-Loops, und ist auf Claude-Code-Hooks zugeschnitten, die den Loop standardmaessig anstossen statt ihn nur als Prompt bereitzustellen.

## Die drei Bausteine

Jeder Loop besteht aus genau drei Rollen:

1. **Builder** — erzeugt oder ueberarbeitet den Entwurf.
2. **Verifier** — unabhaengiger, adversarial geframter Kritiker ("finde, was nicht stimmt", nicht "ist das gut?"). Prueft gegen eine konkrete, dokumentierte Checkliste — nie nach Bauchgefuehl.
3. **Loop-Controller** — entscheidet nach jeder Verifier-Runde: weiter oder stop, anhand einer der drei Stop-Bedingungen unten. Die Fixed-Cap-Bedingung ist IMMER aktiv, egal welche andere Bedingung zusaetzlich gilt — sie ist die Notbremse gegen Endlosschleifen.

## Stop-Bedingungen (kombinierbar)

| Bedingung | Wann nutzen | Beispiel |
|---|---|---|
| **Fixed Cap** | Immer, als Backstop | Max. 3 Runden, danach Abbruch mit Eskalation an den Menschen |
| **Quality-Streak** | Wenn "einmal sauber" nicht reicht (Flakiness, Regression-Risiko) | N=1 bei guenstig korrigierbaren Domaenen (Text, Design); N=2 bei teuren Fehlern (Production-Code) |
| **Severity-Threshold** | Wenn nicht JEDES Finding den Loop blockieren soll | Nur CRITICAL/HIGH stoppen den Loop, MEDIUM/LOW werden reported, aber lassen den Build durch |

**Quality-Streak** statt fixer Rundenzahl: Der Loop stoppt nicht nach "Runde X", sondern nach **N aufeinanderfolgenden sauberen Verifier-Durchlaeufen**. Das verhindert sowohl verfruehtes Stoppen (ein zufaellig guter Durchlauf reicht nicht) als auch unnoetige Extra-Runden (sobald die Qualitaet steht, wird nicht weiter "verschlimmbessert").

**Severity-Threshold**: Der Verifier liefert Findings mit Schweregrad. Nur Findings ab der konfigurierten Schwelle zaehlen fuer den Stop — alles darunter wird dokumentiert, blockiert aber nicht. Verhindert, dass ein Loop an Kleinigkeiten haengen bleibt, while kritische Probleme trotzdem nie durchrutschen.

## Trigger-Modi

| Modus | Verhalten |
|---|---|
| **Self-Paced** | Der Loop waehlt sein eigenes Tempo und stoppt selbst, sobald die Stop-Bedingung erfuellt ist. Standard fuer alle drei Domaenen-Rezepte unten. |
| **Fixed-Interval** | Laeuft mechanisch auf einem festen Zeitplan (z. B. woechentlich), ohne sich selbst zu beenden — fuer wiederkehrende Pruefungen, nicht fuer "bis fertig". Beispiel: ein woechentlicher Check, ob sich die externe Wissensbasis eines Verifiers geaendert hat (siehe Content-Loop unten). |

Hook-Enforcement statt Hook-Ausfuehrung: Ein Claude-Code-Hook ist ein einfacher Shell-Befehl, kein Agenten-Orchestrator. Ein Hook soll den Loop daher **anstossen** (Kontext injizieren: "nutze jetzt den passenden Loop"), nicht selbst die Builder/Verifier-Runden fahren. Die eigentliche Iteration laeuft als normale Agenten-Session oder als orchestriertes Multi-Agent-Workflow.

## Domaenen-Rezepte

### 1. Content-Critique-Loop (Text/Marketing-Copy)

- **Builder:** schreibt den Entwurf (Post, Caption, Skript).
- **Verifier:** prueft gegen eine **faktenbasierte, regelmaessig aktualisierte** Checkliste aus oeffentlich geteilten Daten echter, nachweislich erfolgreicher Stimmen im jeweiligen Kanal — nicht aus Bauchgefuehl oder einer einmal eingefrorenen internen Vorlage. Wichtig: die Wissensbasis selbst veraltet, deshalb ein **Fixed-Interval-Loop** (z. B. woechentlich), der die Quelle gegenprueft und die interne Checkliste aktualisiert, BEVOR der naechste Content-Loop sie nutzt.
- **Stop-Bedingung:** Quality-Streak N=1 (ein sauberer Durchlauf reicht — Text ist guenstig korrigierbar).

### 2. Dokument/Design-Critique-Loop (Slides, Praesentationen, Dokumente)

- **Builder:** erstellt den Entwurf gegen ein dokumentiertes Design-Kit (Farb-/Typo-Tokens + Layout-Archetypen + Checkliste — kein Bauchgefuehl, kein proprietaeres Drittsystem als Blackbox). Das Design-Kit selbst entsteht ueber eine **Abfrage** (Farbpalette, Typografie, Effekte, Footer-Logik, Layout-Archetypen, Format), nicht durch Kopieren eines fremden Kits — siehe [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md) fuer den vollstaendigen Fragenkatalog samt Beispiel-Kit.
- **Verifier:** prueft Fidelity gegen das (per Abfrage erstellte) Design-Kit, nicht gegen einen subjektiven Geschmack.
- **Stop-Bedingung:** Quality-Streak N=1.

### 3. Code-Security-Quality-Loop

- **Builder:** schreibt/aendert Code.
- **Verifier:** Security-Audit bei konfiguriertem **Severity-Threshold** (z. B. nur CRITICAL/HIGH blockieren) + separates Code-Quality-Review. Ergaenzend: ein staendig aktiver, kostenloser Pattern-Check (reine Regex, kein LLM-Call) bei jedem Edit/Write als fruehe Instant-Warnung — der eigentliche Verifier-Durchlauf bleibt der tiefe, bewusst ausgeloeste Audit. Als konkreter, sofort einsetzbarer Verifier-Skill fuer diese Rolle eignet sich [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) (Read-Only Security-Audit-Agent, CC BY 4.0, gleicher Autor) — Deploy-Gate-Modus liefert bereits einen konfigurierbaren Severity-Threshold.
- **Stop-Bedingung:** Fixed Cap N=3 als Backstop, zusaetzlich Quality-Streak N=2 (zwei aufeinanderfolgende saubere Audits) fuer hoehere Sicherheit, da Produktionscode-Fehler teuer sind. Wird der Fixed Cap erreicht, ohne dass der Threshold unterschritten wird, greift die Eskalation an den Menschen — siehe [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) fuer ein ausgearbeitetes Quality-Gate-/Eskalations-Framework (EU-AI-Act-Art.-14-Bezug), das sich direkt als Vorlage fuer diesen Schritt eignet.

## Lernschleife: wohin mit Erkenntnissen aus dem Loop?

Hybrides Routing, keine neue Parallelstruktur:

- **Taktische, domaenenspezifische Erkenntnisse** (z. B. "bei Slide 1 braucht es immer 2 statt 1 Runde") gehoeren in die jeweilige Domaenen-Doku/den Domaenen-Skill selbst.
- **Cross-cutting Erkenntnisse ueber die Loop-Mechanik** (z. B. "Quality-Streak N=2 verbessert die Trefferquote bei Code messbar, bei Text nicht") gehoeren in eine globale Lernkartei mit Reifegrad-Gate: `beobachtet` → `bestaetigt` (mehrfach aufgetreten) → `promoted` (als feste Regel uebernommen). Kein Eintrag ohne echten, generalisierbaren Treffer — neutrale Durchlaeufe tragen nichts bei.

## Setup

Siehe [SETUP.md](SETUP.md) fuer die konkreten Schritte (Skill kopieren, Hook verdrahten, optionalen Fixed-Interval-Loop einrichten).

## Fuer KI-Agenten

Siehe [AGENTS.md](AGENTS.md), wenn ein KI-Coding-Agent (Claude Code, Codex, Gemini CLI o. ae.) dieses Repo selbststaendig lesen und anwenden soll.

## Verwandte eigene Projekte

Zwei weitere Skills desselben Autors (ebenfalls CC BY 4.0), die sich direkt mit der Loop Library kombinieren lassen:

- [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) — Framework fuer menschliche Aufsicht (EU AI Act Art. 14), insbesondere der Quality-Gate-Modus passt als Vorlage fuer die Eskalation-an-den-Menschen beim Fixed-Cap-Stop.
- [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) — Read-Only Security-Audit-Agent, direkt als Verifier-Skill fuer den Code-Security-Quality-Loop (Rezept 3 oben) nutzbar.

## Inspiration & verwandte Projekte

Die Grundidee — Trigger/Action/Verify/Stop als wiederholbares Muster, mit Self-Paced- vs. Fixed-Interval-Modus — ist durch [Matthew Bermans Loop Library (Forward Future)](https://signals.forwardfuture.ai/loop-library/) angestossen worden. Konkret hat uns das **Quality-Streak-Stop** (N aufeinanderfolgende saubere Durchlaeufe statt fixer Rundenzahl) und das **Severity-Threshold-gated Adversarial-Review**-Muster ueberzeugt, beides haben wir uebernommen und in unsere drei Domaenen-Rezepte uebersetzt.

Empfehlenswerte Alternativen/Ergaenzungen, falls du ueber Content/Dokumente/Code-Security hinaus willst:

- [Forward Future Loop Library](https://signals.forwardfuture.ai/loop-library/) — die Originalquelle, 22+ produktionsnahe Ops-Loops (Docs-Sweeps, Test-Coverage, Deployment, SEO, u. v. m.) fuer Software-Teams.
- [az9713/loop-library](https://github.com/az9713/loop-library) — Community-Mirror mit copy-paste-fertigen `/loop`-Prompts fuer Claude Code, basierend auf Bermans Liste.

Wir haben deren konkrete Loop-Texte/Tabellen nicht uebernommen (kein offenes Lizenzfeld bei az9713/loop-library zum Zeitpunkt der Recherche) — nur das allgemeine, nicht schutzfaehige Konzept in eigenen Worten neu beschrieben und domaenenspezifisch ausgearbeitet.
