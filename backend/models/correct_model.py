import re

CHAR_MAP = str.maketrans({
    "@": "a",
    "0": "o",
    "$": "s",
})

WORD_REPLACEMENTS = {
    "Frànce": "France",
    "primè": "prime",
    "ministèr": "minister",
    "Bṛitain": "Britain",
    "capitl": "capital",
    "citty": "city",
    "poplution": "population",
    "defintion": "definition",
    "headqu@rters": "headquarters",
    "frst": "first",
    "presidnt": "president",
    "electi0n": "election",
    "naem": "name",
    "currncy": "currency",
    "Googlé": "Google",
    "Jàpan": "Japan",
    "It@ly": "Italy",
    "Germ@ny": "Germany",
    "Br@zil": "Brazil",
    "Wh@t": "What",
    "NOT": "",          # strip simple negation
}

def correct_prompt(prompt: str) -> str:
    # char-level replace
    prompt = prompt.translate(CHAR_MAP)

    # word-level replace (regex word boundaries)
    for wrong, right in WORD_REPLACEMENTS.items():
        pattern = rf"\b{re.escape(wrong)}\b"
        prompt = re.sub(pattern, right, prompt, flags=re.IGNORECASE)

    return prompt.strip()
