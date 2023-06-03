def valid_braces(string):
    det = 1
    for c in string:
        if c == "(": det *= 2
        if c == ")": det /= 2
        
        if c == "{": det *= 3
        if c == "}": det /= 3

        if c == "[": det *= 5
        if c == "]": det /= 5

    return det == 1