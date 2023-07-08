import vsketch
import numpy as np
from shapely.geometry import Point


class Day3Sketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    radius = vsketch.Param(0.25, decimals=3, unit="in")
    fill_probability = vsketch.Param(0.2)
    random_scalar = vsketch.Param(1.0, decimals=3)
    triangle_randomness = vsketch.Param(5)

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

        for x in np.arange(0, self.width - self.radius + 1, self.radius):
            for y in np.arange(0, self.height - self.radius + 1, self.radius):

                layer = layers[int(vsk.random(0, len(layers)))]
                vsk.stroke(layer)
                if vsk.random(0, 1) < self.fill_probability:

                    vsk.fill(layer)
                else:
                    vsk.noFill()
                vsk.pushMatrix()
                vsk.translate(x, y)
                vsk.rotate(angle=vsk.random(-1, 1) *
                           vsk.random(self.random_scalar * (x + y)),
                           degrees=True)

                vsk.triangle(
                    vsk.random(-self.triangle_randomness,
                               self.triangle_randomness),
                    vsk.random(-self.triangle_randomness,
                               self.triangle_randomness), 0, self.radius,
                    self.radius, 0)
                vsk.popMatrix()

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day3Sketch.display()
