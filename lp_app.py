# CREATED BY Laczi Péter - R9SAAO

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
        self.root.geometry("1920x1080")
        self.root.minsize(1200, 700)

        self.stats = LPStats(total_levels=5)
        self.game = LPGame(width=1600, height=900, level_count=5, stats=self.stats)

        self.left = ttk.Frame(self.root)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right = ttk.Frame(self.root, width=260)
        self.right.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.left, bg="#0f1115", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.game.attach_canvas(self.canvas)

        self.header = tk.Frame(self.right, bg="black")
        self.header.pack(fill=tk.X)
        self.player_var = tk.StringVar(value="Játékban: -")
        tk.Label(self.header, textvariable=self.player_var, fg="white", bg="black",
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=8, pady=6)
        self.hearts_var = tk.StringVar(value="")
        tk.Label(self.header, textvariable=self.hearts_var, fg="#ff4d4f", bg="black",
                 font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=8, pady=6)

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

        ttk.Button(self.right, text="Kilépés (ESC)", command=self.on_exit).pack(pady=4, fill=tk.X, padx=8)

        ttk.Separator(self.right).pack(fill=tk.X, pady=8)
        ttk.Button(self.right, text="Statisztika (M)",
                   command=lambda: lp_show_stats_window(self.root, self.stats)).pack(pady=4, fill=tk.X, padx=8)

        ttk.Separator(self.right).pack(fill=tk.X, pady=8)
        ttk.Button(self.right, text="Eredmény mentése (S)", command=self.on_save).pack(pady=4, fill=tk.X, padx=8)
        ttk.Button(self.right, text="Eredmény betöltése (L)", command=self.on_load).pack(pady=4, fill=tk.X, padx=8)

        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Mentés", command=self.on_save)
        filemenu.add_command(label="Betöltés", command=self.on_load)
        menubar.add_cascade(label="Fájl", menu=filemenu)
        self.root.config(menu=menubar)

        self.canvas.bind("<Button-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<MouseWheel>", self.on_wheel)
        self.canvas.bind("<Button-4>", self.on_wheel)
        self.canvas.bind("<Button-5>", self.on_wheel)

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
        self.root.bind("<Escape>", lambda e: self.on_exit())

        self.show_splash_and_ask_name()

    def _find_logo_path(self) -> str | None:
        here = Path(__file__).resolve().parent
        cwd = Path.cwd()
        names = ["logo.png", "Logo.png", "logo.PNG", "Logo.PNG"]
        for base in (here, here / "assets", cwd, cwd / "assets"):
            for n in names:
                p = base / n
                if p.exists():
                    return str(p)
        return None

    def show_splash_and_ask_name(self):
        self.canvas.delete("all")
        self.root.update_idletasks()
        w = self.canvas.winfo_width() or self.game.width
        h = self.canvas.winfo_height() or self.game.height
        self.canvas.create_rectangle(0, 0, w, h, fill="#0f1115", outline="")
        self.splash_img_id = None
        self.splash_shape_text_id = None
        self.splash_evol_text_id = None
        self.logo_img = None
        path = self._find_logo_path()
        if path:
            try:
                img = tk.PhotoImage(file=path)
                img = img.subsample(3, 3)
                self.logo_img = img
                self.splash_img_id = self.canvas.create_image(0, 0, image=self.logo_img, anchor="center")
            except tk.TclError:
                self.splash_img_id = None
        if not self.splash_img_id:
            self.splash_img_id = self.canvas.create_text(
                w // 2, h // 2, text="LP Games", fill="#E3B341",
                font=("Segoe UI", 56, "bold"), anchor="center"
            )
        self.root.after(10, self._center_splash_now)
        self.canvas.bind("<Configure>", lambda e: self._center_splash_now())
        self.root.after(4000, self._show_shape_evolution_text)

    def _show_shape_evolution_text(self):
        if self.splash_img_id:
            try:
                self.canvas.delete(self.splash_img_id)
            except:
                pass
            self.splash_img_id = None
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cx, cy = w // 2, h // 2
        gap = 10
        self.splash_shape_text_id = self.canvas.create_text(
            cx - gap, cy, text="Shape", fill="#3aa0ff",
            font=("Segoe UI", 44, "bold"), anchor="e"
        )
        self.splash_evol_text_id = self.canvas.create_text(
            cx + gap, cy, text="Evolution", fill="#36c26e",
            font=("Segoe UI", 44, "bold"), anchor="w"
        )
        self._center_splash_now()
        self.root.after(2000, self._ask_name)

    def _center_splash_now(self):
        self.root.update_idletasks()
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cx, cy = w // 2, h // 2
        gap = 10
        if self.splash_img_id:
            self.canvas.coords(self.splash_img_id, cx, cy)
        if self.splash_shape_text_id:
            self.canvas.coords(self.splash_shape_text_id, cx - gap, cy)
        if self.splash_evol_text_id:
            self.canvas.coords(self.splash_evol_text_id, cx + gap, cy)

    def _ask_name(self):
        for eid in (self.splash_img_id, self.splash_shape_text_id, self.splash_evol_text_id):
            if eid:
                try:
                    self.canvas.delete(eid)
                except:
                    pass
        name = simpledialog.askstring("Játékos neve", "Add meg a neved:", parent=self.root) or "Névtelen"
        self.player_var.set(f"Játékban: {name}")
        self.game.player_name = name
        self._ask_difficulty()
        self.game.new_level()
        self.refresh_labels()

    def _ask_difficulty(self):
        win = tk.Toplevel(self.root)
        win.title("Nehézségi szint")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Válaszd ki a nehézségi szintet:", font=("Segoe UI", 11, "bold")).pack(padx=12, pady=(10, 6))

        var = tk.StringVar(value="normal")
        frm = tk.Frame(win)
        frm.pack(padx=12, pady=4, fill=tk.X)

        tk.Radiobutton(frm, text="Könnyű", variable=var, value="easy", anchor="w").pack(fill=tk.X, pady=2)
        tk.Radiobutton(frm, text="Közepes", variable=var, value="normal", anchor="w").pack(fill=tk.X, pady=2)
        tk.Radiobutton(frm, text="Nehéz", variable=var, value="hard", anchor="w").pack(fill=tk.X, pady=2)

        def on_ok():
            self.game.set_difficulty(var.get())
            win.destroy()

        btn = ttk.Button(win, text="OK", command=on_ok)
        btn.pack(pady=(8, 12))

        win.bind("<Return>", lambda e: on_ok())
        win.protocol("WM_DELETE_WINDOW", on_ok)

        self.root.wait_window(win)

    def refresh_labels(self):
        self.level_var.set(f"Szint: {self.game.level}/{self.game.level_count}")
        self.hearts_var.set("❤" * self.game.lives)

    def on_left_down(self, event):
        self.game.pointer_down(event.x, event.y)
        self.refresh_labels()

    def on_drag(self, event):
        self.game.drag_to(event.x, event.y)

    def on_left_up(self, event):
        self.game.pointer_up(event.x, event.y)

    def on_wheel(self, event):
        delta = getattr(event, "delta", 0)
        if delta == 0:
            delta = 120 if getattr(event, "num", 0) == 4 else -120
        factor = 1.04 if delta > 0 else 0.96
        self.scale(factor)

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

    def on_exit(self):
        self.root.destroy()


def run_app():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = LPApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
