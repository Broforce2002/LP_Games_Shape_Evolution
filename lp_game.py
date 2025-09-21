import random
from dataclasses import dataclass
from lp_shapes import LPShape, lp_draw_shape, lp_draw_ghost_shape
from lp_utils import lp_deg_norm, lp_distance

@dataclass
class LPThresholds:
    # laza alapok; 1–2. szinten még lazábbra húzzuk lejjebb
    pos: float = 500.0    # px
    rot: float = 90.0    # fok
    scale: float = 0.90  # arány (40%)

class LPGame:
    def __init__(self, width: int, height: int, level_count: int, stats):
        self.width = width
        self.height = height
        self.level_count = level_count
        self.stats = stats
        self.canvas = None
        self.level = 1
        self.lives = 3
        self.player_name = "Névtelen"

        self.active_shapes: list[LPShape] = []
        self.target_shapes: list[LPShape] = []

        self.selected_indices: set[int] = set()
        self.focus_index: int | None = None
        self._drag_index: int | None = None
        self._drag_offset = (0, 0)

        self.th = LPThresholds()
        random.seed()

    # canvas
    def attach_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.config(width=self.width, height=self.height)
        self.redraw()

    # flow
    def reset(self):
        self.level = 1
        self.lives = 3
        self.new_level()

    def next_level(self):
        self.level += 1
        self.new_level()

    def is_level_cleared(self) -> bool:
        return len(self.active_shapes) == 0

    def required_batch(self) -> int:
        """Hány alakzatot kell egyszerre kijelölni"""
        return min(self.level, 5, max(1, len(self.active_shapes)))

    # level gen
    def new_level(self):
        if not self.canvas:
            return
        self.canvas.delete("all")
        self._draw_background()
        self._draw_center_circle()

        cw = max(self.canvas.winfo_width(), self.width)
        ch = max(self.canvas.winfo_height(), self.height)

        pairs = min(self.level, 5)  # 1. szint: 1, 2. szint: 2 stb.
        sides = min(3 + (self.level - 1), 7)  # oldal szám növekedés
        self.active_shapes.clear()
        self.target_shapes.clear()
        self.selected_indices.clear()
        self.focus_index = None
        self._drag_index = None

        centers = []
        min_dist = 140
        for _ in range(pairs):
            for _try in range(200):
                x = random.randint(220, cw - 220)
                y = random.randint(160, ch - 160)
                if all(lp_distance((x, y), c) >= min_dist for c in centers):
                    centers.append((x, y))
                    break

        for cx, cy in centers:
            target_size = random.randint(100, 150)
            trot = random.randint(0, 359)
            # cél alakzat (zöld)
            self.target_shapes.append(LPShape(cx=cx, cy=cy, size=target_size,
                                              rotation=trot, sides=sides, color="#3fb950"))
            # játékos alakzat (kék)
            self.active_shapes.append(LPShape(
                cx=cx + random.randint(-180, 180),
                cy=cy + random.randint(-140, 140),
                size=int(target_size * random.uniform(0.75, 1.25)),
                rotation=(trot + random.randint(-70, 70)) % 360,
                sides=sides,
                color="#6cb6ff"
            ))

        self.redraw_shapes()
        self.stats.start_level(self.level)

    def _draw_background(self):
        w = max(self.canvas.winfo_width(), self.width)
        h = max(self.canvas.winfo_height(), self.height)
        self.canvas.create_rectangle(0, 0, w, h, fill="#0f1115", outline="")

    def _draw_center_circle(self):
        cx, cy, r = 80, 80, 28
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#e3b341", width=3)
        self.canvas.create_text(cx, cy, text=f"{self.level-1}/{self.level_count}",
                                fill="#e3b341", font=("Segoe UI", 10, "bold"))

    # interaction
    def pointer_down(self, x, y):
        self._drag_index = None
        for i in reversed(range(len(self.active_shapes))):
            if self.active_shapes[i].contains(x, y):
                need = self.required_batch()
                if i in self.selected_indices:
                    self.selected_indices.remove(i)
                elif len(self.selected_indices) < need:
                    self.selected_indices.add(i)
                self.focus_index = i
                self._drag_index = i
                self._drag_offset = (x - self.active_shapes[i].cx, y - self.active_shapes[i].cy)
                break
        self._update_selection_outline()

    def drag_to(self, x, y):
        if self._drag_index is None:
            return
        sh = self.active_shapes[self._drag_index]
        sh.cx = x - self._drag_offset[0]
        sh.cy = y - self._drag_offset[1]
        self.redraw_shapes()
        self._update_selection_outline()

    def pointer_up(self, x, y):
        self._drag_index = None  # focus marad

    def rotate_active(self, deg):
        targets = list(self.selected_indices) if self.selected_indices else ([self.focus_index] if self.focus_index is not None else [])
        for i in targets:
            sh = self.active_shapes[i]
            sh.rotation = lp_deg_norm(sh.rotation + deg)
        if targets:
            self.redraw_shapes()
            self._update_selection_outline()

    def scale_active(self, factor):
        targets = list(self.selected_indices) if self.selected_indices else ([self.focus_index] if self.focus_index is not None else [])
        for i in targets:
            sh = self.active_shapes[i]
            new_size = int(sh.size * factor)
            sh.size = max(30, min(260, new_size))
        if targets:
            self.redraw_shapes()
            self._update_selection_outline()

    def redraw(self):
        if not self.canvas:
            return
        self.canvas.delete("all")
        self._draw_background()
        self._draw_center_circle()
        self.redraw_shapes()
        self._update_selection_outline()

    def redraw_shapes(self):
        self.canvas.delete("ghost")
        self.canvas.delete("active")
        for t in self.target_shapes:
            lp_draw_ghost_shape(self.canvas, t)
        for a in self.active_shapes:
            lp_draw_shape(self.canvas, a)

    def _update_selection_outline(self):
        self.canvas.delete("selmark")
        for i in self.selected_indices or ([] if self.focus_index is None else [self.focus_index]):
            sh = self.active_shapes[i]
            r = max(12, int(sh.size * 0.18))
            self.canvas.create_oval(sh.cx - r, sh.cy - r, sh.cx + r, sh.cy + r,
                                    outline="#ffd866", width=2, dash=(3, 3), tags=("selmark",))

    # batch check (engedékeny + snap + szintidő mentés)
    def check_alignment_batch(self):
        if len(self.active_shapes) == 0:
            return None, "Ez a szint már kész."
        need = min(self.required_batch(), len(self.active_shapes))
        if len(self.selected_indices) != need:
            return None, f"Jelölj ki egyszerre {need} darabot!"

        # Ellenőrzés a kiválasztottakon
        for i in list(self.selected_indices):
            a = self.active_shapes[i]
            t = self.target_shapes[i]

            d = lp_distance((a.cx, a.cy), (t.cx, t.cy))
            rot_diff = abs(lp_deg_norm(a.rotation - t.rotation))
            rot_diff = min(rot_diff, 360 - rot_diff)
            scale_diff = abs(a.size - t.size) / t.size

            # Alap tűrések (szintről szintre kicsit csökken)
            tight = max(0, self.level - 1)
            pos_thr   = max(60,  self.th.pos   - 1.5  * tight)   # px
            rot_thr   = max(20,  self.th.rot   - 1.0  * tight)   # fok
            scale_thr = max(0.30, self.th.scale - 0.01 * tight)  # arány

            # 1–2. szint extra puhítás
            if self.level == 1:
                pos_thr, rot_thr, scale_thr = 120.0, 50.0, 0.60
            elif self.level == 2:
                pos_thr, rot_thr, scale_thr = max(pos_thr, 100.0), max(rot_thr, 40.0), max(scale_thr, 0.50)

            # alap döntés
            ok = (d <= pos_thr) and (rot_diff <= rot_thr) and (scale_diff <= scale_thr)

            if not ok:
                # SNAP: ha kb. közel vagy, automatikusan rásegítünk és elfogadjuk
                if (d <= pos_thr * 1.6) and (rot_diff <= rot_thr * 1.6) and (scale_diff <= scale_thr * 1.6):
                    a.cx, a.cy = t.cx, t.cy
                    a.rotation = t.rotation
                    a.size = t.size
                    ok = True

            if not ok:
                self.lives -= 1
                return False, (f"Pontatlan: Δpos={d:.1f}px, Δrot={rot_diff:.1f}°, Δscale={scale_diff*100:.1f}%\n"
                               f"(Tűrések: pos≤{pos_thr:.0f}px, rot≤{rot_thr:.0f}°, méret≤{scale_thr*100:.0f}%)")

        # jó: töröljük a kijelölteket
        for i in sorted(self.selected_indices, reverse=True):
            del self.active_shapes[i]
            del self.target_shapes[i]
        self.selected_indices.clear()
        self.focus_index = None
        self.redraw()

        # ha a szint ezzel készen van -> idő rögzítése
        if self.is_level_cleared():
            self.stats.finish_level(self.level)

        return True, f"Találat: {need}/{need} teljesítve."

    # serialize
    def to_dict(self):
        return {
            "level": self.level,
            "lives": self.lives,
            "player_name": self.player_name,
            "active": [s.__dict__ for s in self.active_shapes],
            "target": [s.__dict__ for s in self.target_shapes],
            "stats": self.stats.as_dict(),
            "width": self.width,
            "height": self.height,
            "level_count": self.level_count,
        }

    def from_dict(self, data: dict):
        self.level = int(data.get("level", 1))
        self.lives = int(data.get("lives", 3))
        self.player_name = data.get("player_name", self.player_name)
        self.width = int(data.get("width", self.width))
        self.height = int(data.get("height", self.height))
        self.level_count = int(data.get("level_count", self.level_count))
        self.active_shapes = [LPShape.from_dict(d) for d in data.get("active", []) if d]
        self.target_shapes = [LPShape.from_dict(d) for d in data.get("target", []) if d]
        self.selected_indices.clear()
        self.focus_index = None
        self.redraw()
