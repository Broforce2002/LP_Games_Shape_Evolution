# CREATED BY Laczi Péter - R9SAAO

from dataclasses import dataclass
import math


@dataclass
class LPShape:
    cx: int
    cy: int
    size: int
    rotation: float
    sides: int
    color: str = "#6cb6ff"  # kék (aktív)

    def polygon(self):
        r = self.size
        ang0 = math.radians(self.rotation)
        pts = []
        for k in range(self.sides):
            a = ang0 + 2 * math.pi * k / self.sides
            x = self.cx + r * math.cos(a)
            y = self.cy + r * math.sin(a)
            pts.extend((x, y))
        return pts

    def contains(self, x, y) -> bool:
        # egyszerű kör-alapú becslés
        dx, dy = x - self.cx, y - self.cy
        return (dx*dx + dy*dy) <= (self.size * 1.1) ** 2

    def as_dict(self):
        return {
            "cx": self.cx, "cy": self.cy, "size": self.size,
            "rotation": self.rotation, "sides": self.sides, "color": self.color
        }

    @staticmethod
    def from_dict(d):
        return LPShape(
            cx=int(d["cx"]), cy=int(d["cy"]), size=int(d["size"]),
            rotation=float(d["rotation"]), sides=int(d["sides"]),
            color=d.get("color", "#6cb6ff")
        )


def lp_draw_shape(canvas, shape: LPShape):
    canvas.create_polygon(
        shape.polygon(), outline=shape.color, width=7, fill="", tags=("active",)
    )
    canvas.create_oval(
        shape.cx-2, shape.cy-2, shape.cx+2, shape.cy+2,
        fill=shape.color, outline="", tags=("active",)
    )


def lp_draw_ghost_shape(canvas, shape: LPShape):
    canvas.create_polygon(
        shape.polygon(), outline="#3fb950", width=5, dash=(4, 4), fill="", tags=("ghost",)
    )
    canvas.create_oval(
        shape.cx-2, shape.cy-2, shape.cx+2, shape.cy+2,
        fill="#3fb950", outline="", tags=("ghost",)
    )
