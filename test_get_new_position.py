import ShapeFunctions as sf

point1 = [5,2]
point2 = [2,3]

new_point = [0,0]

new_point[0], new_point[1] = sf.get_new_position(point2[0],point2[1],point1[0],point1[1])

print(new_point)
