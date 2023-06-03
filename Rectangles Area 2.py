def calculate(rectangles):
    if len(rectangles) == 0:
        return 0
    
    minX = min(rectangles, key=lambda r: r[0])[0]
    maxX = max(rectangles, key=lambda r: r[2])[2]
    minY = min(rectangles, key=lambda r: r[1])[1]
    maxY = max(rectangles, key=lambda r: r[3])[3]

    width = maxX - minX + 1
    height = maxY - minY + 1
    grid = [[False] * width for _ in range(height)]

    for rect in rectangles:
        x0, y0, x1, y1 = rect[0] - minX, rect[1] - minY, rect[2] - minX, rect[3] - minY
        for y in range(y0, y1):
            for x in range(x0, x1):
                grid[y][x] = True

    return sum(sum(row) for row in grid)
