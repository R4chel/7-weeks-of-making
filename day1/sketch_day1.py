import vsketch
from shapely.geometry import Point


class Day1Sketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    width = vsketch.Param(5., decimals=2, unit="in")
    height = vsketch.Param(3., decimals=2, unit="in")
    margin = vsketch.Param(0.1, decimals=3, unit="in")
    landscape = vsketch.Param(True)
    pen_width = vsketch.Param(0.7, decimals=3, min_value=1e-10, unit="mm")
    num_layers = vsketch.Param(1)
    num_steps = vsketch.Param(50)
    radius = vsketch.Param(1.0, decimals=3, unit="in")
    fill_probability = vsketch.Param(0.01)

    def random_point(self, vsk: vsketch.Vsketch):
        return Point(vsk.random(0, self.width), vsk.random(0, self.height))

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.height}x{self.width}",
                 landscape=self.landscape,
                 center=False)
        self.width = self.width - 2 * self.margin
        self.height = self.height - 2 * self.margin
        vsk.translate(self.margin, self.margin)
        vsk.penWidth(f"{self.pen_width}")

        start = self.random_point(vsk)

        # implement your sketch here
        layers = [1 + i for i in range(self.num_layers)]
        for step in range(self.num_steps):

            layer = layers[int(vsk.random(0, len(layers)))]
            vsk.stroke(layer)
            if vsk.random(0, 1) < self.fill_probability:
                vsk.fill(layer)
            else:
                vsk.noFill()
            start = self.random_point(vsk)
            vsk.square(start.x, start.y, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day1Sketch.display()
