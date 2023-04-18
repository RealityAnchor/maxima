def get_triangles(point_pairs):
    point_dict = {}
    for a, b in point_pairs:
        if a not in point_dict:
            point_dict[a] = []
        if b not in point_dict:
            point_dict[b] = []
        if b not in point_dict[a]:
            point_dict[a].append(b)
        if a not in point_dict[b]:
            point_dict[b].append(a)
    triangle_list = []
    for p1 in point_dict:
        for p2 in point_dict[p1]:
            for p3 in point_dict[p2]:
                if p3 in point_dict[p1]:
                    triangle = tuple(sorted([(p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])]))
                    triangle_list.append(triangle)
    return sorted(triangle_list)

edges = [((1, 1), (2, 2)),
         ((2, 2), (3, 1)),
         ((2, 2), (3, 1)),
         ((1, 1), (3, 1)),
         ((2, 2), (4, 4)),
         ((4, 4), (5, 5)),
         ((5, 5), (6, 4)),
         ((4, 4), (6, 4)),
         ((1, 1), (4, 4)),
         ((3, 1), (5, 5)),
         ((3, 1), (5, 17)),
         ((2, 2), (5, 17)),
         ((3, 1), (5, 18)),
         ((2, 2), (5, 18)),
         ((2, 2), (5, 20)),
         ((2, 2), (5, 5))]

for t in get_triangles(edges):
    print(t, end='\n')
