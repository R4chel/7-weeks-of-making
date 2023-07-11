import vsketch
from point2d import Point2D
from shapely.geometry import Point, LineString, MultiPoint
import numpy as np
import math


def sech(x):
    val = np.cosh(x)
    if val == 0:
        return None
    return 1 / val


fns = {
    "cosh": np.cosh,
    "sinh": np.sinh,
    "sech": sech,
    "csch": (lambda x: None if np.sinh(x) == 0 else 1 / (np.sinh(x)))
}


class Day5Sketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    center = vsketch.Param(True)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    precision = vsketch.Param(3)
    num_shapes = vsketch.Param(10)
    num_points = vsketch.Param(20)
    min_scale = vsketch.Param(10.0, decimals=3)
    max_scale = vsketch.Param(300.0, decimals=3)
    min_cycles = vsketch.Param(1.0, decimals=3, min_value=0)
    max_cycles = vsketch.Param(3.0, decimals=3, min_value=0)
    max_shapes_at_point = vsketch.Param(4, min_value=1)
    min_degrees_between = vsketch.Param(10, min_value=0, max_value=360)
    func = vsketch.Param("cosh", choices=fns.keys())

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw_spiral(self, vsk: vsketch.Vsketch, direction):
        cycles = np.round(vsk.random(self.min_cycles, self.max_cycles),
                          self.precision)
        scale = np.round(vsk.random(self.min_scale, self.max_scale),
                         self.precision)
        thetas = [
            direction * i * 2 * np.pi / self.num_points
            for i in np.arange(0, self.num_points * cycles)
        ]
        for theta in thetas:
            val = fns[self.func](theta)
            if val is None:
                continue
            r = scale * val

            p = Point2D(a=theta, r=r)
            if self.debug:
                print(p)
            vsk.point(p.x, p.y)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}",
                 landscape=self.landscape,
                 center=self.center)
        self.width = self.width - 2 * self.margin
        self.height = self.height - 2 * self.margin
        vsk.translate(self.margin, self.margin)
        vsk.penWidth(f"{self.pen_width}")

        # implement your sketch here
        layers = [1 + i for i in range(self.num_layers)]
        max_shapes = math.floor(360 / self.min_degrees_between)
        if self.max_shapes_at_point > max_shapes:
            self.max_shapes_at_point = max_shapes
        count = 0
        while count < self.num_shapes:
            vsk.pushMatrix()
            p = self.random_point(vsk)
            vsk.translate(p.x, p.y)

            num_shapes_at_point = math.ceil(
                vsk.random(self.max_shapes_at_point))
            direction = 1 if vsk.random(0, 1) < 0.5 else -1
            max_degrees = 360 / num_shapes_at_point
            for i in range(num_shapes_at_point):
                if i == 0:
                    vsk.rotate(angle=vsk.random(0, 360), degrees=True)
                else:
                    vsk.rotate(angle=vsk.random(self.min_degrees_between,
                                                max_degrees),
                               degrees=True)

                layer = layers[int(vsk.random(0, len(layers)))]
                vsk.stroke(layer)
                self.draw_spiral(vsk, direction)
                count += 1
            vsk.popMatrix()

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day5Sketch.display()
