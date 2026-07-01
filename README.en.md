<p align="center">
  <img src="assets/banner.png" alt="Loop Library" width="100%">
</p>

# Loop Library

**A toolkit that automatically revises drafts until they pass a checkable quality bar — instead of generating once and hoping.**

> 🇩🇪 *Deutsche Version: [README.md](README.md)*

---

## Why this exists

AI tools generate in one shot — good, mediocre, sometimes off, with nobody (human or machine) systematically sharpening the result. Loop Library provides the missing piece: a **Builder/Verifier pattern** with clearly defined stop conditions that iterates a draft until it meets a documented quality bar — whether that's text, design, or code.

---

## The gist

> Three roles (**Builder → Verifier → Loop Controller**), three combinable stop conditions (**Fixed Cap, Quality Streak, Severity Threshold**), two trigger modes (**Self-Paced, Fixed-Interval**) — plus three ready-to-use domain recipes as a starting point.

---

## The three stop conditions

| Condition | When to use |
|---|---|
| **Fixed Cap** | Always active, as an emergency brake against infinite loops |
| **Quality Streak** | When a single clean pass isn't enough — stops only after N consecutive clean verifier rounds |
| **Severity Threshold** | When not every finding should block — only findings at or above the configured severity stop the loop, the rest is just documented |

---

## Three domain recipes as a starting point

| Domain | Builder | Verifier | Stop condition |
|---|---|---|---|
| **Content/Text** | writes the draft | checks against a fact-grounded, regularly refreshed checklist (see Fixed-Interval mode) | Quality Streak N=1 |
| **Document/Design** | builds against a documented design kit (color/type tokens, layout archetypes) | checks fidelity against the kit | Quality Streak N=1 |
| **Code/Security** | writes/changes code | security audit at a severity threshold + code-quality review, complemented by a free instant pattern check (regex, no LLM call) | Fixed Cap N=3 + Quality Streak N=2 |

These recipes are templates, not finished skills — they need project-specific knowledge (your brand voice, your design system, your security standard) to actually work. Details in [`SKILL.md`](SKILL.md). For the document/design recipe there's a complete, generic reference implementation including an intake questionnaire: [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md).

---

## How do I use this?

### A) As a Claude Code skill
Drop [`SKILL.md`](SKILL.md) into your skills folder (`~/.claude/skills/loop-library/`). After that, a request like *"run this through an iteration loop"* or *"build me a quality loop for X"* is enough.

### B) As a methodology (no setup)
Useful even without the tool: a complete checklist for setting up iterative quality loops correctly — role separation, stop conditions, hook-vs-orchestration.

### C) Concrete setup
See [`SETUP.md`](SETUP.md) for the exact steps (copy the skill, optionally wire up the pattern-check hook, set up a fixed-interval loop).

### D) For AI agents
See [`AGENTS.md`](AGENTS.md) — a working instruction specifically for an AI coding agent applying this repo on its own.

---

## Who is this for?

- **Solo builders & teams** who don't want to generate AI drafts (text, design, code) once, but systematically sharpen them.
- **Anyone using Claude Code hooks** to trigger quality loops by default instead of calling them manually.

---

## What's in this repo

| File | What's inside |
|---|---|
| [`README.md`](README.md) | This intro (German) |
| [`README.en.md`](README.en.md) | This version |
| [`SKILL.md`](SKILL.md) | The full loop-engine knowledge (also usable as a Claude Code skill) |
| [`SETUP.md`](SETUP.md) | Concrete setup steps |
| [`AGENTS.md`](AGENTS.md) | Instruction for AI coding agents |
| [`examples/security-pattern-check.py`](examples/security-pattern-check.py) | Example hook for the code-security-quality loop (instant regex checks, no LLM call) |
| [`examples/slides-design-kit-template.md`](examples/slides-design-kit-template.md) | Reference implementation for the document/design critique loop (generic intake questionnaire + verifier checklist) |
| [`LICENSE`](LICENSE) | License (CC BY 4.0) |
| [`NOTICE`](NOTICE) | Attribution notice — also credits the inspiration source |

---

## Related projects by the same author

Two more skills by the same author (also CC BY 4.0) that combine directly with the Loop Library:

- [human-oversight](https://github.com/clauszeissler-dot/HumanOversight) — human-oversight framework (EU AI Act Art. 14); its Quality-Gate mode is a ready template for the escalate-to-human step on a Fixed-Cap stop.
- [dev-security-affairs](https://github.com/clauszeissler-dot/DevSecurityAffAIrs) — read-only security-audit agent, usable directly as the Verifier skill for the code-security quality loop.

---

## Inspiration & related projects

The core idea — trigger/action/verify/stop, self-paced vs. fixed-interval — was sparked by [Matthew Berman's Loop Library (Forward Future)](https://signals.forwardfuture.ai/loop-library/). We adopted the **Quality-Streak stop** and the **severity-threshold-gated adversarial review** as concepts, re-described in our own words and applied to three connected domain recipes — no text/tables copied (see [`NOTICE`](NOTICE)).

Worth checking out if you want to go beyond content/documents/code-security:

- [Forward Future Loop Library](https://signals.forwardfuture.ai/loop-library/) — the original source, 22+ production-grade ops loops for software teams (docs sweeps, test coverage, deployment, SEO, and more).
- [az9713/loop-library](https://github.com/az9713/loop-library) — community mirror with copy-paste-ready `/loop` prompts for Claude Code.

---

## License & author

© Claus Zeißler. Licensed under **[Creative Commons CC BY 4.0](LICENSE)** — free to use, share, and adapt as long as you credit the author.

More: [affairs-consulting.de](https://www.affairs-consulting.de)
