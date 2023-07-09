import vsketch
from point2d import Point2D
from shapely.geometry import Point, LineString, MultiPoint
import numpy as np


class Day4Sketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    precision = vsketch.Param(3)
    num_steps = vsketch.Param(10)
    num_points = vsketch.Param(360)
    min_scale = vsketch.Param(1.0, decimals=3)
    max_scale = vsketch.Param(3.0, decimals=3)
    min_a = vsketch.Param(0.02, decimals=3)
    max_a = vsketch.Param(0.5, decimals=3)
    min_cycles = vsketch.Param(1.0, decimals=3)
    max_cycles = vsketch.Param(3.0, decimals=3)

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw_spiral(self, vsk: vsketch.Vsketch):
        cycles = np.round(vsk.random(self.min_cycles, self.max_cycles),
                          self.precision)
        a = np.round(vsk.random(self.min_a, self.max_a), self.precision)
        thetas = [
            i * 2 * np.pi / self.num_points
            for i in np.arange(self.num_points * cycles)
        ]
        pts = []
        for theta in thetas:
            sinh = np.sinh(theta)
            if sinh == 0:
                continue
            sinh = 0.000001 if sinh == 0 else sinh
            r = a / sinh

            p = Point2D(a=theta, r=r)
            print(p)
            vsk.point(p.x, p.y)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}",
                 landscape=self.landscape,
                 center=True)
        self.width = self.width - 2 * self.margin
        self.height = self.height - 2 * self.margin
        vsk.translate(self.margin, self.margin)
        vsk.penWidth(f"{self.pen_width}")

        layers = [1 + i for i in range(self.num_layers)]

        for _ in range(self.num_steps):
            layer = layers[int(vsk.random(0, len(layers)))]
            vsk.pushMatrix()
            p = self.random_point(vsk)
            vsk.translate(p.x, p.y)
            vsk.rotate(angle=vsk.random(-360, 360), degrees=True)

            vsk.stroke(layer)
            vsk.scale(
                np.round(vsk.random(self.min_scale, self.max_scale),
                         self.precision))
            self.draw_spiral(vsk)
            vsk.popMatrix()

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day4Sketch.display()
