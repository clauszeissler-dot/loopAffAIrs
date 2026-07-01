# Slides-Design-Kit-Template — Referenzimplementierung fuer Domaenen-Rezept 2

Konkrete, sofort nutzbare Umsetzung des **Dokument/Design-Critique-Loops** aus `SKILL.md` (Rezept 2) fuer Praesentations-Slides. Generisch gehalten — kein festes Farbschema, sondern eine **Abfrage**, die das Design-Kit fuer *dein* Projekt erst erzeugt, bevor der Builder irgendetwas baut.

## Wie es funktioniert

1. **Abfrage zuerst.** Bevor eine einzige Slide gebaut wird, beantwortest du den Fragenkatalog unten (einmalig pro Projekt/Marke). Das Ergebnis ist ein ausgefuelltes Design-Kit — feste Farb-/Typo-Tokens, Layout-Archetypen, Footer-Logik.
2. **Builder baut ausschliesslich gegen das Kit.** Keine Farbe, keine Schriftart, kein Effekt, der nicht im Kit steht. Kein Bauchgefuehl, keine Ad-hoc-Entscheidung pro Slide.
3. **Verifier prueft Fidelity gegen das Kit**, nicht gegen subjektiven Geschmack. Checkliste unten.
4. **Stop-Bedingung:** Quality-Streak N=1 (ein sauberer Durchlauf reicht — siehe `SKILL.md`).

## Die Abfrage

### A) Farbpalette
1. Hintergrund: dunkel, hell, oder markenspezifisch? Genauer Hex-Wert?
2. Primaerakzent (CTAs, Hervorhebungen)? Hex-Wert?
3. Sekundaerakzent (Daten, sekundaere Hervorhebungen)? Hex-Wert?
4. Textfarben: primaer / sekundaer / muted — jeweils Hex-Wert?
5. **Vergleichsslides („gut vs. schlecht", „vorher/nachher"):** Soll „schlecht/vermeiden" eine echte Warnfarbe (z. B. Rot) bekommen, oder bewusst neutral bleiben (nur Kontur-/Deckkraft-Kontrast, keine Ampel-Farbe)? Diese Entscheidung explizit festhalten — sie ist erfahrungsgemaess der haeufigste offene Punkt.

### B) Typografie
1. Headline-Font? Gewicht(e)?
2. Body-Font? Gewicht(e)?
3. Mono-Font fuer Kennzahlen/Kicker/Seitenzahlen (optional)?
4. Headlines: Grossbuchstaben oder normale Schreibung? Letter-Spacing?

### C) Effekte
1. Glow/Neon-Effekt auf Headlines: ja/nein? Wenn ja — subtil (kaum sichtbar) oder stark (deutlicher Leuchteffekt)? Genauer Blur-/Opacity-Wert.
2. Hintergrund-Textur (Grid, Rauschen, Farbverlauf): ja/nein? Wenn ja, welche und wie dezent?
3. Card-/Container-Stil: Glass-/Blur-Effekt, feste Fuellung, oder nur Kontur?

### D) Footer-Logik
1. Was steht im Footer: Seitenzahl? Quellenangabe? Marken-Logo/-Schriftzug? URL? Datum?
2. Position: unten links, unten rechts, oder verteilt?
3. Auf jeder Slide gleich, oder nur auf Titel-/Abschlussslide anders?

### E) Layout-Archetypen
Welche Slide-Typen werden gebraucht? Typische Auswahl (anpassen):
- Titel-Slide (Kicker + H1 + Subline)
- Inhalts-Slide mit Checkliste/Aufzaehlung
- Statistik-/Kennzahlen-Slide (Zahlen-Karten)
- Vergleichs-Slide (zwei Spalten, siehe Punkt A5)
- Zitat-/Quote-Slide
- Abschluss-/CTA-Slide

### F) Format
1. Aufloesung/Seitenverhaeltnis: 16:9 (z. B. 1920×1080) fuer Praesentationen, 4:5 (z. B. 1080×1350) fuer Instagram/LinkedIn-Karussell, etwas anderes?
2. Export: HTML → PNG (z. B. per Headless-Browser/Playwright), direkt als PDF gebuendelt, oder beides?

## Beispiel: ausgefuelltes Kit (illustrativ, generisch)

```yaml
farbe:
  hintergrund: "#0A0A0A"          # dunkel
  akzent_primaer: "#3D8BFF"       # CTAs, Hervorhebungen
  akzent_sekundaer: "#00D9A3"     # Daten, sekundaer
  text_primaer: "#E5E5E5"
  text_muted: "#757575"
  vergleich_negativ: neutral      # bewusst KEINE Ampel-Warnfarbe, nur Kontur-Kontrast
typografie:
  headline_font: "Space Grotesk"
  body_font: "Inter"
  mono_font: "JetBrains Mono"
  headline_case: "uppercase"
effekte:
  glow: true
  glow_intensitaet: subtil        # 8-12px Blur, keine grossen Halo-Effekte
  hintergrund_textur: grid_dezent
footer:
  inhalt: [seitenzahl, marke, url]
  position: "unten, verteilt links/rechts"
layout_archetypen: [titel, inhalt_checkliste, statistik, vergleich, cta]
format:
  aufloesung: "1920x1080"
  export: "HTML -> PNG (Headless-Browser)"
```

## Verifier-Checkliste (Fidelity-Check, keine Geschmacksfrage)

Fuer JEDE generierte Slide pruefen:

- [ ] Nur Farben aus dem Kit verwendet — keine Ad-hoc-Hex-Werte
- [ ] Headline-/Body-Font exakt wie im Kit, korrekte Gewichte
- [ ] Glow-Intensitaet (falls aktiviert) entspricht dem im Kit festgelegten Wert — nicht staerker/schwaecher je nach Slide
- [ ] Footer auf jeder Slide identisch positioniert und mit denselben Elementen (ausser explizit anders im Kit vermerkt)
- [ ] Vergleichsslides folgen der im Kit getroffenen Entscheidung (Warnfarbe vs. neutral) — konsistent ueber alle Vergleichsslides hinweg, nicht slide-abhaengig gemischt
- [ ] Layout entspricht einem der definierten Archetypen, kein Ad-hoc-Layout
- [ ] Format/Aufloesung entspricht der Kit-Vorgabe

**Stop-Bedingung:** Quality-Streak N=1. Bei Abweichung: direkt korrigieren, nicht nur benennen, dann erneut gegen die Checkliste pruefen.
