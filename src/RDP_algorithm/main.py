import data

# una linea no vertical.

p3 = data.Point(2.0, 3.0)
p1 = data.Point(1.0, 1.0)
p2 = data.Point(4.0, 3.0)
print(p1)
print(p2)
l1 = data.Line(p1, p2)
print(l1)
l2 = data.Line.get_perpendicular_line_out_of_current_line(p3, l1.get_perpendicular_line_gradient())
print(l2)
p4 = data.Line.get_intersection_point(l1, l2)
print(p4)
print("the distance among 2 points is: ", data.Point.get_distance_between_2_points(p3, p4))

# una linea vertical => NO FUNCIONAL
#p1 = data.Point(1.0, 1.0)
#p2 = data.Point(1.0, 4.0)
#p3 = data.Point(2.0, 3.0)
#l1 = data.Line(p1, p2)
#print(l1)
#print(l1.get_perpendicular_line_gradient())
#l2 = data.Line.get_perpendicular_line_out_of_current_line(p3, l1.get_perpendicular_line_gradient())
#print(l2)



