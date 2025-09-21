import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

from lp_game import LPGame
from lp_stats import LPStats, lp_show_stats_window
from lp_utils import lp_save_json, lp_load_json

APP_TITLE = "LP Shape Evolution"


class LPApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1920x1080")   # Indulás 1920x1080 felbontással
        self.root.minsize(1200, 700)

        # --- Model ---
        self.stats = LPStats(total_levels=5)
        self.game = LPGame(width=1600, height=900, level_count=5, stats=self.stats)

        # --- Layout ---
        self.left = ttk.Frame(self.root)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right = ttk.Frame(self.root, width=260)
        self.right.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas
        self.canvas = tk.Canvas(self.left, bg="#0f1115", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.game.attach_canvas(self.canvas)

        # Fejléc (játékos + életek)
        self.header = tk.Frame(self.right, bg="black")
        self.header.pack(fill=tk.X)
        self.player_var = tk.StringVar(value="Játékban: -")
        tk.Label(
            self.header, textvariable=self.player_var, fg="white", bg="black",
            font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT, padx=8, pady=6)
        self.hearts_var = tk.StringVar(value="")
        tk.Label(
            self.header, textvariable=self.hearts_var, fg="#ff4d4f", bg="black",
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.RIGHT, padx=8, pady=6)

        # Oldalsáv
        self.level_var = tk.StringVar(value="Szint: 1/5")
        self.info_var = tk.StringVar(
            value=("Egér: mozgatás • Görgő: méretezés • A/D: forgatás ±2° • Shift+A/D: ±10° • "
                   "Enter: ellenőrzés • Space: következő • S: mentés • L: betöltés • M: stat • R: új játék")
        )

        ttk.Label(self.right, textvariable=self.level_var, font=("Segoe UI", 12, "bold")).pack(pady=(10, 4))
        ttk.Label(self.right, text="Vezérlés", font=("Segoe UI", 10, "bold")).pack()
        ttk.Label(self.right, textvariable=self.info_var, wraplength=240, justify=tk.LEFT).pack(padx=8)

        self.btn_check = ttk.Button(self.right, text="Ellenőrzés (Enter)", command=self.on_check)
        self.btn_check.pack(pady=(10, 4), fill=tk.X, padx=8)
        self.btn_next = ttk.Button(self.right, text="Következő szint (Space)", command=self.on_next)
        self.btn_next.pack(pady=4, fill=tk.X, padx=8)
        self.btn_reset = ttk.Button(self.right, text="Újrakezdés (R)", command=self.on_reset)
        self.btn_reset.pack(pady=4, fill=tk.X, padx=8)
        ttk.Separator(self.right).pack(fill=tk.X, pady=8)
        ttk.Button(self.right, text="Statisztika (M)",
                   command=lambda: lp_show_stats_window(self.root, self.stats)).pack(pady=4, fill=tk.X, padx=8)

        ttk.Separator(self.right).pack(fill=tk.X, pady=8)
        ttk.Button(self.right, text="Eredmény mentése (S)", command=self.on_save).pack(pady=4, fill=tk.X, padx=8)
        ttk.Button(self.right, text="Eredmény betöltése (L)", command=self.on_load).pack(pady=4, fill=tk.X, padx=8)

        # Menü
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Mentés", command=self.on_save)
        filemenu.add_command(label="Betöltés", command=self.on_load)
        menubar.add_cascade(label="Fájl", menu=filemenu)
        self.root.config(menu=menubar)

        # Canvas események
        self.canvas.bind("<Button-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<MouseWheel>", self.on_wheel)   # Windows
        self.canvas.bind("<Button-4>", self.on_wheel)     # Linux/Mac
        self.canvas.bind("<Button-5>", self.on_wheel)

        # Billentyűk
        self.root.bind("<KeyPress-a>", lambda e: self.rotate(-2))
        self.root.bind("<KeyPress-d>", lambda e: self.rotate(+2))
        self.root.bind("<Shift-KeyPress-a>", lambda e: self.rotate(-10))
        self.root.bind("<Shift-KeyPress-d>", lambda e: self.rotate(+10))
        self.root.bind("<Return>", lambda e: self.on_check())
        self.root.bind("<space>", lambda e: self.on_next())
        self.root.bind("<KeyPress-s>", lambda e: self.on_save())
        self.root.bind("<KeyPress-l>", lambda e: self.on_load())
        self.root.bind("<KeyPress-m>", lambda e: lp_show_stats_window(self.root, self.stats))
        self.root.bind("<KeyPress-r>", lambda e: self.on_reset())

        # Splash és névbekérés
        self.show_splash_and_ask_name()

    # ----------- LOGO KERESÉSE ----------- #
    def _find_logo_path(self) -> str | None:
        """Megkeresi a logo.png fájlt több helyen."""
        here = Path(__file__).resolve().parent
        cwd = Path.cwd()
        names = ["logo.png", "Logo.png", "logo.PNG", "Logo.PNG"]

        for base in (here, here / "assets", cwd, cwd / "assets"):
            for n in names:
                p = base / n
                if p.exists():
                    return str(p)
        return None

    # ----------- SPLASH MEGJELENÍTÉS ----------- #
    def show_splash_and_ask_name(self):
        """
        Splash képernyő:
        1) 0–4 mp: logó középen
        2) 4–6 mp: 'Shape' (kék) + 'Evolution' (zöld) szöveg középen
        3) 6 mp után: névbekérés
        """
        self.canvas.delete("all")
        self.root.update_idletasks()

        w = self.canvas.winfo_width() or self.game.width
        h = self.canvas.winfo_height() or self.game.height

        # Háttér
        self.canvas.create_rectangle(0, 0, w, h, fill="#0f1115", outline="")

        # Splash elemek ID-k
        self.splash_img_id = None
        self.splash_shape_text_id = None
        self.splash_evol_text_id = None
        self.logo_img = None

        # Logó megjelenítése
        path = self._find_logo_path()
        if path:
            try:
                img = tk.PhotoImage(file=path)
                img = img.subsample(3, 3)  # ha túl nagy, kicsinyítés
                self.logo_img = img
                self.splash_img_id = self.canvas.create_image(0, 0, image=self.logo_img, anchor="center")
            except tk.TclError as e:
                print(f"[LOGO] Betöltési hiba: {e}")
                self.splash_img_id = None

        if not self.splash_img_id:
            # Ha nincs logó, helyettesítő szöveg (ez is eltűnik 4 mp után)
            self.splash_img_id = self.canvas.create_text(
                w // 2, h // 2,
                text="LP Games",
                fill="#E3B341",
                font=("Segoe UI", 56, "bold"),
                anchor="center"
            )

        # Középre igazítás azonnal és méretezéskor
        self.root.after(10, self._center_splash_now)
        self.canvas.bind("<Configure>", lambda e: self._center_splash_now())

        # 4 mp múlva: logó eltüntetése és szöveg megjelenítése
        self.root.after(4000, self._show_shape_evolution_text)

    def _show_shape_evolution_text(self):
        """Eltünteti a logót, megjeleníti a 'Shape' (kék) + 'Evolution' (zöld) szöveget, majd 2 mp múlva névbekérés."""
        # Logó eltüntetése
        if self.splash_img_id:
            try:
                self.canvas.delete(self.splash_img_id)
            except Exception:
                pass
            self.splash_img_id = None

        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cx, cy = w // 2, h // 2
        offset_y = 0  # pontosan középen
        gap = 10      # kis rés a két szó között

        # Két darab szöveg, középen "összekapcsolva"
        self.splash_shape_text_id = self.canvas.create_text(
            cx - gap, cy + 0 + 0,  # kicsit balra
            text="Shape",
            fill="#3aa0ff",                 # kék
            font=("Segoe UI", 44, "bold"),
            anchor="e"                      # jobb szélhez igazítva
        )
        self.splash_evol_text_id = self.canvas.create_text(
            cx + gap, cy + 0 + 0,  # kicsit jobbra
            text="Evolution",
            fill="#36c26e",                 # zöld
            font=("Segoe UI", 44, "bold"),
            anchor="w"                      # bal szélhez igazítva
        )

        # Biztos ami biztos: középre húzás
        self._center_splash_now()

        # 2 mp múlva névbekérés
        self.root.after(2000, self._ask_name)

    def _center_splash_now(self):
        """Középre helyezi a splash elemeket (logó vagy szövegek)."""
        self.root.update_idletasks()
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cx, cy = w // 2, h // 2

        # Ha még a logó látszik, azt középre tesszük
        if self.splash_img_id:
            self.canvas.coords(self.splash_img_id, cx, cy)

        # Ha már a felirat látszik, azt is középre rendezzük
        gap = 10
        if self.splash_shape_text_id:
            self.canvas.coords(self.splash_shape_text_id, cx - gap, cy)
        if self.splash_evol_text_id:
            self.canvas.coords(self.splash_evol_text_id, cx + gap, cy)

    # ----------- NÉV BEKÉRÉS ----------- #
    def _ask_name(self):
        # Splash elemek törlése a névbekérés és játékindítás előtt
        for eid in (self.splash_img_id, self.splash_shape_text_id, self.splash_evol_text_id):
            if eid:
                try:
                    self.canvas.delete(eid)
                except Exception:
                    pass

        name = simpledialog.askstring("Játékos neve", "Add meg a neved:", parent=self.root) or "Névtelen"
        self.player_var.set(f"Játékban: {name}")
        self.game.player_name = name

        # Induljon el a játék
        self.game.new_level()
        self.refresh_labels()

    # ----------- UI FRISSÍTÉS ----------- #
    def refresh_labels(self):
        self.level_var.set(f"Szint: {self.game.level}/{self.game.level_count}")
        self.hearts_var.set("❤" * self.game.lives)

    # ----------- EGÉR ----------- #
    def on_left_down(self, event):
        self.game.pointer_down(event.x, event.y)
        self.refresh_labels()

    def on_drag(self, event):
        self.game.drag_to(event.x, event.y)

    def on_left_up(self, event):
        self.game.pointer_up(event.x, event.y)

    def on_wheel(self, event):
        delta = getattr(event, 'delta', 0)
        if delta == 0:
            delta = 120 if getattr(event, 'num', 0) == 4 else -120
        factor = 1.04 if delta > 0 else 0.96
        self.scale(factor)

    # ----------- ALAKZAT MŰVELETEK ----------- #
    def rotate(self, deg):
        self.game.rotate_active(deg)

    def scale(self, factor):
        self.game.scale_active(factor)

    def on_check(self):
        ok, msg = self.game.check_alignment_batch()
        if ok is None:
            messagebox.showinfo("Info", msg)
        elif ok:
            if msg:
                messagebox.showinfo("Találat", msg)
            self.refresh_labels()
            if self.game.is_level_cleared():
                if self.game.level >= self.game.level_count:
                    messagebox.showinfo("Gratulálunk!", f"5/5 – Szép volt, {self.game.player_name}!")
                else:
                    self.game.next_level()
                    self.refresh_labels()
        else:
            if self.game.lives <= 0:
                messagebox.showerror("Vége", "Elfogytak az életek. Game Over.")
            else:
                messagebox.showwarning("Nem pontos", msg + "\n(Élet -1)")
            self.refresh_labels()

    def on_next(self):
        if self.game.is_level_cleared():
            if self.game.level >= self.game.level_count:
                messagebox.showinfo("Gratulálunk!", f"5/5 – Szép volt, {self.game.player_name}!")
            else:
                self.game.next_level()
                self.refresh_labels()

    def on_reset(self):
        self.game.reset()
        self.refresh_labels()

    def on_save(self):
        data = self.game.to_dict()
        fname = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if fname:
            lp_save_json(fname, data)
            messagebox.showinfo("Mentve", fname)

    def on_load(self):
        fname = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if fname:
            data = lp_load_json(fname)
            if data:
                self.game.from_dict(data)
                self.game.redraw()
                self.refresh_labels()
                messagebox.showinfo("Betöltve", fname)


# ----------- BELÉPÉSI PONT ----------- #
def run_app():
    root = tk.Tk()
    app = LPApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
