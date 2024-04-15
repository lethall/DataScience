from math import sin, asin, cos, acos, atan, pi, radians, degrees, sqrt

# Utility functions

class DMS:
    dd : float = 0.0
    deg : int = 0
    min : int = 0
    sec : float = 0.0

    def __init__(self, deg: float = 0.0) -> None:
        """To DMS and back"""
        self.dd = deg
        if abs(deg) < 1.0e-10:
            return
        sign = -1 if deg < 0 else 1
        dd = abs(deg)
        self.deg = int(dd)
        self.sec = s = (dd - self.deg) * 3600
        self.deg *= sign
        self.min = int(s / 60)
        self.sec %= 60

    def assign(self, d: float, m: float = 0, s: float = 0) -> float:
        """Assign a decimal angle using degrees, minutes, seconds"""
        self.deg = int(d)
        self.min = int(m)
        self.sec = s
        sign = -1 if d < 0 else 1
        d = abs(d)
        s += (60 * m)
        d += (s / 3600)
        return d * sign

    def __str__(self) -> str:
        return f"""{self.deg}\xb0 {self.min}' {self.sec:05.2f}" ({self.dd:.5f}\xb0)"""

angle = DMS(83.81234518)

assert f"{angle} == {DMS().assign(angle.deg, angle.min, angle.sec):.5f}" == '83° 48\' 44.44" (83.81235°) == 83.81235'
assert f"{DMS().assign(-5, 30, 1):.4f}" == '-5.5003'
assert f"{DMS().assign(5, 30, 1):.4f}" == '5.5003'
        

class Triangle:
    A_deg : float = 0.0
    B_deg : float = 0.0
    C_deg : float = 0.0
    A_rad : float = 0.0
    B_rad : float = 0.0
    C_rad : float = 0.0
    a : float = 0.0
    b : float = 0.0
    c : float = 0.0
    sine_ratio : float = 0.0

    def __setattr__(self, __name: str, __value) -> None:
        self.__dict__[__name] = __value
        if __name.endswith("_deg"):
            self.__dict__[__name.replace("_deg", "_rad")] = radians(__value)
        if __name.endswith("_rad"):
            self.__dict__[__name.replace("_rad", "_deg")] = degrees(__value)

    def assign(self, a_deg: float, b_deg: float, c_deg: float, a: float, b: float, c:float) -> None:
        """Classic A, B, C (angles) a, b, c (sides)"""
        self.A_deg = a_deg
        self.B_deg = b_deg
        self.C_deg = c_deg
        self.a = a
        self.b = b
        self.c = c
        return self

    def __str__(self) -> str:
        return f"A: {self.A_deg:.4f}\xb0 B: {self.B_deg:.4f}\xb0 C: {self.C_deg:.4f}\xb0 | a: {self.a:.4f} b: {self.b:.4f} c: {self.c:.4f}"
    
# Planar
class Planar(Triangle):
    def law_of_cosine(self, a: float, b: float, c_deg: float) -> float:
        self.C_deg = c_deg
        self.c = sqrt(a**2 + b**2 - 2*a*b*cos(self.C_rad))
        return self.c

    def law_of_sine_ASA(self, a_deg: float, side_a: float, b_deg: float) -> float:
        """Angle, Side, Angle"""
        self.A_deg = a_deg
        self.B_deg = b_deg
        self.sine_ratio = sin(self.A_rad) / side_a
        self.b = sin(self.B_rad) / self.sine_ratio
        return self.b

    def law_of_sine_SSA(self, side_a: float, side_b: float, a_deg: float) -> float:
        """Side, Side, Angle"""
        self.a = side_a
        self.b = side_b
        self.A_deg = a_deg
        self.A_rad = radians(a_deg)
        self.sine_ratio = sin(self.A_rad) / self.a
        self.B_rad = asin(self.sine_ratio * self.b)
        return self.B_deg
        
# Spherical
class Spherical(Triangle):
    def law_of_cosine(self, a: float, b: float, c_deg: float) -> float:
        self.C_deg = c_deg
        cos_c = cos(self.C_rad)
        self.a = a = radians(a)
        self.b = b = radians(b)
        self.c = degrees(acos(cos(a) * cos(b) + sin(a) * sin(b) * cos_c))
        return self.c
    
    def law_of_sine_ASA(self, a_deg: float, side_a: float, b_deg: float) -> float:
        """Angle, Side, Angle
        Should agree with Pythagoras
        """
        self.A_deg = a_deg
        self.a = a = sin(radians(side_a))
        self.sine_ratio = sin(self.A_rad) / a
        return degrees(asin(sin(radians(b_deg)) / self.sine_ratio))
    
    def law_of_sine_SSA(self, side_a: float, side_b: float, a_deg: float) -> float:
        """Side, Side, Angle
        """
        self.a = a = sin(radians(side_a))
        self.b = b = sin(radians(side_b))
        self.A_deg = a_deg
        self.sine_ratio = sin(self.A_rad) / a
        self.B_rad = asin(self.sine_ratio * b)
        return self.B_deg

    def area(self, a_deg: float, b_deg: float, c_deg: float, r: float) -> float:
        self.A_deg = a_deg
        self.B_deg = b_deg
        self.C_deg = c_deg
        eps = (self.A_rad + self.B_rad + self.C_rad) - pi
        return eps * r * r
    
    @staticmethod
    def delta_omega(deg: float) -> float:
        return 2 * pi * (1 - cos(radians(deg)))



class Geo:
    lat: float
    longi: float
    name: str
    EARTH_RADIUS_KM = 6371
    M_PER_S = 200
    
    def __init__(self, name: str, lat: float, lat_dir: str, longi: float, longi_dir: str) -> None:
        self.name = name
        self.lat = abs(lat) if lat_dir == "N" else -1 * abs(lat)
        # self.lat = 
        # both north or both south?
        self.longi = abs(longi) if longi_dir == "E" else -1 * abs(longi)
    
    def great_circle(self, dest) -> tuple[float, float, float]:
        delta_longi = dest.longi - self.longi
        src_lat = 90 - self.lat
        dest_lat = 90 - dest.lat
        tri = Spherical()
        self.gc_path = gc_path = tri.law_of_cosine(src_lat, dest_lat, delta_longi)
        distance = radians(gc_path) * Geo.EARTH_RADIUS_KM
        ang_a = tri.law_of_sine_SSA(gc_path, dest_lat, delta_longi)
        extreme = abs(tri.law_of_sine_ASA(90, src_lat, ang_a))
        self.upper_lat = 90 - extreme
        ang_b = tri.law_of_sine_SSA(gc_path, src_lat, delta_longi)
        return distance, ang_a, (180 - ang_b) % 360
    
    def trip(self, dest) -> None:
        """
        >>> cairo = Geo("Cairo", DMS().assign(30, 2, 40), 'N', DMS().assign(31, 14, 9), 'E');\
            sfo = Geo("San Francisco", DMS().assign(37, 46, 39), 'N', DMS().assign(122, 24, 59), 'W');\
            cairo.trip(sfo)
        From Cairo to San Francisco: 11991.6km (16.65hrs) start: -21° 37' 27.31" (-21.62425°) finish: 203° 48' 12.14" (203.80337°)
        >>> print(f"path: {DMS(cairo.gc_path)} upper latitude: {DMS(cairo.upper_lat)}")
        path: 107° 50' 34.76" (107.84299°) upper latitude: 71° 23' 50.49" (71.39736°)
        """
        km, bearing_start, bearing_end = self.great_circle(dest)
        hrs = (km * 1000 / Geo.M_PER_S) / 3600
        print("From {} to {}: {:.1f}km ({:.2f}hrs) start: {} finish: {}".format(
            self.name, dest.name, km, hrs, DMS(bearing_start), DMS(bearing_end)
        ))

def position(latitude : float, alt_or_decl : float, azm_or_ha : float, azm_correction : bool = False) -> tuple[float, float]:
    """ Convert alt/az to decl/ha
    >>> latitude = 52;h = DMS().assign(19,47,48);A = DMS().assign(282,42,5);lst = 0;decl, hra = position(latitude, h, A);\
        ra = DMS((hra - lst)/15);print(f"RA: {ra.deg:.0f}:{ra.min:2.0f}:{ra.sec:02.2f} ({hra:.5f}\xb0) decl: {DMS(decl)}")
    RA: 5:48:39.00 (87.16249°) decl: 23° 13' 09.45" (23.21929°)
    """
    lat_rad = radians(latitude)
    lat_sin = sin(lat_rad)
    lat_cos = cos(lat_rad)

    azm_rad = radians(azm_or_ha)
    azm_sin = sin(azm_rad)
    azm_cos = cos(azm_rad)

    alt_rad = radians(alt_or_decl)
    alt_sin = sin(alt_rad)
    alt_cos = cos(alt_rad)

    decl_sin = alt_sin * lat_sin + alt_cos * lat_cos * azm_cos
    decl = asin(decl_sin)
    decl_deg = degrees(decl)
    decl_cos = cos(decl)
    hra = acos((alt_sin - lat_sin * decl_sin) / (lat_cos * decl_cos))
    hra_deg = degrees(hra)
    correction = 360 if azm_correction else 180
    hra_deg = correction - hra_deg if azm_sin > 0 else hra_deg

    return decl_deg, hra_deg


if __name__ == "__main__":
    # Planar tests
    # Using pythagorean theorem to test the laws of sin and cos
    tri = Planar().assign(0, 0, 90, 1, 1, 0) 
    assert f"{abs(sqrt(tri.a**2 + tri.b**2) - tri.law_of_cosine(tri.a, tri.b, tri.C_deg)):.4f}" == '0.0000'
    
    tri = Planar()
    b = tri.law_of_sine_ASA(45, 1, 45)
    C_rad = radians(180 - (45 + 45))
    c = sin(C_rad) / tri.sine_ratio
    assert f"{abs(sqrt(c**2 - b**2) - 1):.4f}" == '0.0000'
    
    tri = Planar()
    B_deg = tri.law_of_sine_SSA(1, 1, 45)
    C_rad = radians(180 - (45 + B_deg))
    c = sin(C_rad) / tri.sine_ratio
    assert f"{abs(sqrt(c**2 - 1**2) - 1):.4f}" == '0.0000'
    
    #Spherical tests
    assert f"{Spherical().law_of_cosine(75, 30, 60):.5f}" == '62.24930'

    assert f"{Spherical().law_of_sine_ASA(30, 45, 15):.4f}" == '21.4707'

    assert f"{Spherical().law_of_sine_SSA(62.24930, 75, 60):.4f}" == '70.9502'

    assert f"{Spherical().area(60, 75, 105, 6378000):.1f}" == '42598827710210.5'
    
    import doctest
    doctest.testmod(verbose=False)