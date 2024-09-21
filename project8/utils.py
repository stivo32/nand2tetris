from typing import List


def skip_empty_lines(content: List[str]) -> List[str]:
    return [line for line in content if line.strip()]


def skip_comments(content: List[str]) -> List[str]:
    return [line for line in content if not line.startswith('//')]