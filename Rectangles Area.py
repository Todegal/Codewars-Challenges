from collections import OrderedDict 

def find_intersections(index, rectangles):
    intersections = []
    
    A = rectangles[index]
    for i, r in enumerate(rectangles):
        if i == index:
            continue
        
        B = r      
        x0 = max(A[0], B[0])
        y0 = max(A[1], B[1])
        x1 = min(A[2], B[2])
        y1 = min(A[3], B[3])
        if x0 < x1 and y0 < y1:
            intersections.append((x0, y0, x1, y1))
    
    return list(OrderedDict.fromkeys(intersections))  # remove duplicates

def calculate_rect_area(rect):
    return (rect[2] - rect[0]) * (rect[3] - rect[1])

def calculate(rectangles):
    intersections = []
    area = 0
    num_intersections = 0
    for i, rectangle in enumerate(rectangles):
        area += calculate_rect_area(rectangle)
        r_intersections = find_intersections(i, rectangles)
        num_intersections = len(r_intersections)
        if num_intersections > 1:
            area -= calculate(r_intersections)
        elif num_intersections == 1:
            area -= calculate_rect_area(r_intersections[0])
        intersections += r_intersections

    #area = max(area, 0)
    intersections = list(OrderedDict.fromkeys(intersections)) # remove duplicate intersections    
    
    num_intersections = len(intersections)
    if num_intersections > 1:
        area += calculate(intersections)
    elif num_intersections == 1:
        area += calculate_rect_area(intersections[0])
    
    return area
