def snail(snail_map):
    N = len(snail_map)
    if N == 0:
        return []
    if N == 1:
        return [snail_map[0][0]]
    x, y = 0, 0
    mx, my = 1, 0
    output = []
    for _ in range((2*N) + (2 * (N-2))):
        output.append(snail_map[y][x])
        if mx == 1 and x == N-1:
            mx = 0
            my = 1
        elif my == 1 and y == N-1:
            mx = -1
            my = 0
        elif mx == -1 and x == 0:
            mx = 0
            my = -1

        x += mx; y += my
    nMap = [j[1:N-1:] for j in snail_map[1:N-1:]]
    output += snail(nMap)
    return output
