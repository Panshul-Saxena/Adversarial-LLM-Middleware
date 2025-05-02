import numpy as np

def extract_leading_digits(logits):
    digits = []
    for val in logits.flatten():
        if val <= 0:
            continue
        first_digit = next((c for c in str(val) if c.isdigit() and c != "0"), None)
        if first_digit:
            digits.append(int(first_digit))
    return digits


def follows_benford_law(logits, threshold: float = 0.1) -> bool:
    digits = extract_leading_digits(logits)
    if not digits:
        return True  # if we can't measure, assume OK

    actual = np.array([digits.count(d) / len(digits) for d in range(1, 10)])
    expected = np.log10(1 + 1 / np.arange(1, 10))

    deviation = np.sum(np.abs(actual - expected))
    return deviation < threshold
