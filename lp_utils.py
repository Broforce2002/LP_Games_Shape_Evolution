import json
import math

def lp_deg_norm(deg: float) -> float:
    deg = deg % 360.0
    if deg < 0:
        deg += 360.0
    return deg

def lp_distance(p1, p2) -> float:
    (x1, y1), (x2, y2) = p1, p2
    return math.hypot(x1 - x2, y1 - y2)

def lp_save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def lp_load_json(path: str) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
