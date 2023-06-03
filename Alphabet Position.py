import string

def alphabet_position(text):
    positions = []
    for c in text:
        if c.lower() in string.ascii_lowercase:
            positions.append(string.ascii_lowercase.index(c.lower()) + 1)
    return " ".join(map(str, positions))