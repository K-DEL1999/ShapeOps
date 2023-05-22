import ShapeFunctions as sf

point1 = [5,2]
point2 = [2,3]

new_point = [0,0]


while point1 != point2:
    print(point1)
    point1[0],point1[1] = sf.get_new_position(point2[0],point2[1],point1[0],point1[1])

print(point1)
