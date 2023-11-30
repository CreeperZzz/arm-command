def check_intersection(start, direction, cube_min, cube_max):
    """
    Checks if a vector starting from 'start' in the direction of 'direction' collides with a cube
    defined by its minimum corner 'cube_min' and maximum corner 'cube_max'.
    """
    x0, y0, z0 = start
    dx, dy, dz = direction
    xmin, ymin, zmin = cube_min
    xmax, ymax, zmax = cube_max

    # Helper function to check if value is within a range
    def within_range(value, min_val, max_val):
        return min_val <= value <= max_val

    # Check for each axis if the vector intersects the cube
    t_values = []

    if dx != 0:
        tx1 = (xmin - x0) / dx
        tx2 = (xmax - x0) / dx
        t_values.extend([tx1, tx2])

    if dy != 0:
        ty1 = (ymin - y0) / dy
        ty2 = (ymax - y0) / dy
        t_values.extend([ty1, ty2])

    if dz != 0:
        tz1 = (zmin - z0) / dz
        tz2 = (zmax - z0) / dz
        t_values.extend([tz1, tz2])

    # Filter out negative t values, as they indicate intersection in the opposite direction
    t_values = [t for t in t_values if t >= 0]

    for t in t_values:
        x, y, z = x0 + dx * t, y0 + dy * t, z0 + dz * t
        if within_range(x, xmin, xmax) and within_range(y, ymin, ymax) and within_range(z, zmin, zmax):
            return True

    return False

# Example usage
'''
start_point = (0, 0, 0)  # Starting point of the vector
vector_direction = (1, 1, 1)  # Direction of the vector
cube_min_corner = (1, 1, 1)  # Minimum corner of the cube
cube_max_corner = (3, 3, 3)  # Maximum corner of the cube

collision = does_vector_collide_with_cube(start_point, vector_direction, cube_min_corner, cube_max_corner)
print("Collision:", collision)
'''