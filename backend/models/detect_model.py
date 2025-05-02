import re

ACCENTS = "àèìòùÀÈÌÒÙ"

LEETSYMBOLS = r"[@$€0-9]"

MISSPELLS = {
    "capitl", "citty", "poplution", "defintion",
    "frst", "presidnt", "currncy"
}

NEGATIONS = {"NOT", "never", "isn't"}

def is_adversarial(prompt: str) -> bool:
    if any(ch in prompt for ch in ACCENTS):
        return True

    if re.search(LEETSYMBOLS, prompt):
        return True

    plower = prompt.lower()
    if any(w in plower for w in MISSPELLS):
        return True

    if any(n in prompt for n in NEGATIONS):
        return True

    return False
