from itertools import groupby

def look_say(n: int) -> int:
    result = ""
    groups = ["".join(y) for _, y in groupby(str(n))]
    for group in groups:
        result += str(len(group))
        result += group[0]

    return int(result)