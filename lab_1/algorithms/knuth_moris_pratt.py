from typing import Tuple, List


def __compute_prefix_function(text: str) -> List[int]:
    prefix_function = [0 for _ in text]
    for i in range(1, len(text)):
        j = prefix_function[i - 1]
        while j > 0 and text[i] != text[j]:
            j = prefix_function[j - 1]
        if text[i] == text[j]:
            j += 1
        prefix_function[i] = j
    return prefix_function 


def search(text: str, pattern: str) -> Tuple[int, int]:
    comparisons_count = 0
    text_size = len(text)
    pattern_size = len(pattern)

    if pattern_size == 0:
        return 0, 0
    
    if text_size == 0 or pattern_size > text_size:
        return -1, 0
    
    prefix_function = __compute_prefix_function(text)
    i, j = 0, 0
    while j != text_size - pattern_size + 1:
        if i >= pattern_size:
            return j, comparisons_count
        comparisons_count += 1
        if text[j + i] != pattern[i]:
            if i == 0:
                j += 1
            elif prefix_function[i - 1] == 0:
                j += i
                i = 0
            else:
                j = j + i - prefix_function[i - 1]
                i = prefix_function[i - 1]
        else:
            i += 1

    if i == pattern_size:
        return text_size - pattern_size - 1, comparisons_count

    return -1, comparisons_count
