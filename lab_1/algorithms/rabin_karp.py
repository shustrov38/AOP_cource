from typing import Tuple


MOD = int(1e9) + 7
Q = 101


def __rolling_hash(text: str) -> int:
    _hash = 0
    for ch in text:
        _hash  = (_hash * Q + ord(ch)) %  MOD
    return _hash


def __roll_hash(_hash: int, l: str, r: str, size: int) -> int:
    return (_hash * Q - ord(l) * (Q ** size) + ord(r)) % MOD


def search(text: str, pattern: str) -> Tuple[int, int]:
    comparisons_count = 0
    text_size = len(text)
    pattern_size = len(pattern)

    if pattern_size == 0:
        return 0, 0
    
    if text_size == 0 or pattern_size > text_size:
        return -1, 0
    
    pattern_hash = __rolling_hash(pattern)
    _hash = __rolling_hash(text[:pattern_size])

    for i in range(text_size - pattern_size + 1):
        comparisons_count += 1
        if _hash == pattern_hash:
            return i, comparisons_count
        _hash = __roll_hash(_hash, text[i], text[i + pattern_size], pattern_size)

    return -1, comparisons_count
