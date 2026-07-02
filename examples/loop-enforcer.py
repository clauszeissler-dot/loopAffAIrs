#!/usr/bin/env python3
"""UserPromptSubmit hook: nudge toward the loop-library skill for detected domains.

Non-blocking. Only injects additionalContext when a domain keyword matches;
otherwise stays silent. Code/security is intentionally NOT covered here --
that domain already has its own PostToolUse pattern-check hook.
"""
import json
import re
import sys

DOMAIN_PATTERNS = {
    "content": re.compile(
        r"\b(linkedin|instagram|caption|social[- ]media|post(?:s)?\b.*schreib|schreib.*\bpost)\b",
        re.IGNORECASE,
    ),
    "design": re.compile(
        r"\b(slides?|folie(?:n)?|pr[äa]sentation|karussell|design-?kit)\b",
        re.IGNORECASE,
    ),
}

RECIPE_HINT = {
    "content": "Content-Critique-Loop (Rezept 1)",
    "design": "Dokument/Design-Critique-Loop (Rezept 2)",
}


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    prompt = data.get("prompt", "") or ""

    matched = [domain for domain, pattern in DOMAIN_PATTERNS.items() if pattern.search(prompt)]
    if not matched:
        return 0

    recipes = ", ".join(RECIPE_HINT[d] for d in matched)
    context = (
        f"Hinweis (loop-enforcer): Dieser Auftrag klingt nach einer Domäne, "
        f"für die der loop-library-Skill ein Rezept bereitstellt ({recipes}). "
        f"Vor der Auslieferung einen Builder/Verifier-Durchlauf gegen die passende "
        f"Checkliste erwägen, statt einmalig zu generieren."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
