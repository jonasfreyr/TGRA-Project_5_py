class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"C({self.r}, {self.g}, {self.b})"


class Material:
    def __init__(self, diffuse=None, specular=None, ambient=None, shininess=None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse is None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular is None else specular
        self.shininess = 1 if shininess is None else shininess
        self.ambient = Color(0.0, 0.0, 0.0) if ambient is None else ambient
