import re
from typing import Iterable, List

PUNCT_STRIP_RE = re.compile(r"^\W+|\W+$")

def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for raw in text.split():
        t = PUNCT_STRIP_RE.sub("", raw.lower())
        if t:
            tokens.append(t)
    return tokens

def split_paragraphs(content: str) -> List[str]:
    # Split by blank lines into paragraphs
    blocks = [p.strip() for p in content.split("\n\n")]
    return [b for b in blocks if b]
