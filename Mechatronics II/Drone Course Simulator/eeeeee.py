import numpy as np
def compute_arc_t_range(self, center, radius, basis1, basis2, point1, point2):
        """
        center: [x, y, z] of circle center
        radius: scalar radius of the circle
        basis1, basis2: orthonormal vectors defining the plane of the circle
        point1, point2: 3D points the arc must pass through

        Returns:
            t_start, t_end — the angle range the drone should travel
            t0, t1, t2 — angles corresponding to origin, point1, point2
        """

        def get_t(point):
            rel = (np.array(point) - np.array(center)) / radius
            a = np.dot(rel, np.array(basis1))
            b = np.dot(rel, np.array(basis2))
            return np.arctan2(b, a) % (2 * np.pi)

        t0 = get_t([0, 0, 0])
        t1 = get_t(point1)
        t2 = get_t(point2)

        # Choose the larger t value to ensure passing through both points
        t_candidates = np.array([t1, t2])
        deltas = (t_candidates - t0) % (2 * np.pi)
        t_end = t0 + np.max(deltas)

        return t0, t_end, t0, t1, t2


x = -30.625
y = 20.995
z = 42.336
r = 56.312
s1 = -0.654
s2 = 0.379
s3 = 0.654

v1 = -0.672
v2 = 0
v3 = -0.741
a, b, c, d, e = compute_arc_t_range("e", (x, y, z), r, (s1, s2, s3), (v1, v2, v3),(23.3, 6.7, 50), (-75, 25, 7.9))
print(a, b, c, d, e)