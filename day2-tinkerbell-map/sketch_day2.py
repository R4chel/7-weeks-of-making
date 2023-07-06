import vsketch
from shapely.geometry import Point


class Day2Sketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    num_steps = vsketch.Param(1000)
    a = vsketch.Param(0.9, decimals=3)
    b = vsketch.Param(-0.6013, decimals=3)
    c = vsketch.Param(2.0, decimals=3)
    d = vsketch.Param(0.5, decimals=3)
    x_0 = vsketch.Param(-0.72)
    y_0 = vsketch.Param(-0.64)

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}",
                 landscape=self.landscape,
                 center=True)
        self.width = self.width - 2 * self.margin
        self.height = self.height - 2 * self.margin
        vsk.translate(self.margin, self.margin)
        vsk.penWidth(f"{self.pen_width}")

        layers = [1 + i for i in range(self.num_layers)]
        f = lambda x: (x + 1) * min(self.width, self.height) / 2
        x = self.x_0
        y = self.y_0
        for step in range(self.num_steps):
            layer = layers[int(vsk.random(0, len(layers)))]
            vsk.stroke(layer)
            vsk.point(f(x), f(y))
            x, y = x * x - y * y + self.a * x + self.b * y, 2 * x * y + self.c * x + self.d * y

            print(x, y)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day2Sketch.display()
