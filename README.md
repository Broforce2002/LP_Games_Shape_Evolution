# Hallgatói adatok

**Hallgató:** Laczi Péter  
**Neptun kód:** R9SAAO  
**Projekt neve:** LP Games – Shape Evolution  
**Fejlesztett modulok:** `lp_app.py`, `lp_game.py`, `lp_shapes.py`, `lp_stats.py`, `lp_utils.py`  
**Főprogram:** `main.py`

---

# LP Games - Shape Evolution

## Leírás
A **Shape Evolution** egy logikai kirakós játék, amelyben a cél, hogy a kék alakzatokat mozgatással, forgatással és méretezéssel pontosan fedésbe hozd a zöld célalakzatokkal.  

A játék **Python** és **Tkinter** alapokon készült, demonstrálva a GUI programozást, interaktív grafika kezelését és játéklogika megvalósítását.

Ez a projekt tanulási és fejlesztési célú alkalmazás, amely jól bemutatja a grafikus programozást, a felhasználói interakciók és a játékmechanika megvalósítását.

---
## Logó
A projekt logója **egyedi, saját készítésű grafikai elem**, amelyet **Figma** segítségével terveztem és hoztam létre.  
A logó a játék indulásakor megjelenik splash képernyőként is.  
A vizuális arculat célja a modern, tiszta, játékos hangulat megteremtése, amely támogatja a projekt esztétikai értékét és felismerhetőségét.

- **Tervező:** Laczi Péter  
- **Eszköz:** Figma  
- **Felhasználás:** kizárólag oktatási és portfólió célra  
- **Szerzői jog:** csak a fejlesztő engedélyével használható fel

---

## Játékmenet – irányítás
| Művelet | Billentyű / Egér |
|--------|----------------|
| Alakzat mozgatása | Egérrel húzva |
| Méretezés | Egér görgő |
| Forgatás | A / D = ±2°, Shift + A / D = ±10° |
| Ellenőrzés | Enter |
| Következő szint | Space |
| Mentés | S |
| Betöltés | L |
| Statisztika | M |
| Új játék | R |
| Kilépés | ESC |

**Cél:** minden kék alakzatot tökéletesen illeszteni a megfelelő zöld célalakzatra az életek elfogyása előtt.

---

## Projekt felépítése
| Fájlnév / Mappa | Leírás |
|-----------------|--------|
| `main.py` | A fő belépési pont, innen indul a program |
| `lp_app.py` | A felhasználói felület és eseménykezelés |
| `lp_game.py` | A játék működése, szintek és logika |
| `lp_shapes.py` | Alakzatok kezelése és kirajzolása |
| `lp_stats.py` | Statisztikák kezelése és grafikon |
| `lp_utils.py` | Segédfüggvények (matematika, JSON mentés) |
| `assets/` | Logó és egyéb grafikus elemek |

---

## Használt fő függvények

| Modul | Függvény | Leírás |
|-------|----------|--------|
| **main.py** | `run_app()` | Az alkalmazás indítása, teljes képernyős ablak megnyitása |
| **lp_app.py** | `show_splash_and_ask_name()` | Indító képernyő és névkérő ablak |
| | `_ask_difficulty()` | Nehézségi szint kiválasztása |
| | `refresh_labels()` | Szint és életek kijelzésének frissítése |
| | `on_check()` | Illesztés ellenőrzése |
| | `on_next()` | Következő szint betöltése |
| | `on_reset()` | Teljes játék újraindítása |
| | `on_save()` | Játékállás mentése JSON fájlba |
| | `on_load()` | Korábban mentett állás betöltése |
| | `on_exit()` | Kilépés az alkalmazásból |
| | `on_left_down(event)` | Alakzat kiválasztása egérrel |
| | `on_drag(event)` | Alakzat mozgatása |
| | `on_wheel(event)` | Alakzat méretezése görgővel |
| | `rotate(deg)` | Kijelölt alakzat forgatása |
| | `scale(factor)` | Kijelölt alakzat méretezése |
| **lp_game.py** | `new_level()` | Új szint generálása, alakzatok létrehozása |
| | `next_level()` | Következő szint betöltése |
| | `reset()` | Játékállapot teljes újraindítása |
| | `is_level_cleared()` | Ellenőrzés, elkészült-e a szint |
| | `required_batch()` | Egyszerre illesztendő alakzatok száma |
| | `check_alignment_batch()` | Illesztés, forgatás és méret ellenőrzése |
| | `redraw()` | Teljes canvas újrarajzolása |
| | `redraw_shapes()` | Alakzatok kirajzolása |
| | `pointer_down()` / `drag_to()` / `pointer_up()` | Egér interakciók |
| | `to_dict()` | Mentés objektummá |
| | `from_dict(data)` | Játékállás betöltése |
| **lp_shapes.py** | `polygon()` | Alakzat pontjainak meghatározása |
| | `contains(x,y)` | Kattintás alakzaton belül |
| | `lp_draw_shape()` | Aktív alakzat kirajzolása |
| | `lp_draw_ghost_shape()` | Cél alakzat kirajzolása szaggatottan |
| **lp_stats.py** | `start_level()` | Időmérés indítása |
| | `finish_level()` | Szintidő kiszámítása |
| | `lp_show_stats_window()` | Eredmények grafikonon |
| **lp_utils.py** | `lp_deg_norm()` | Szög normalizálása |
| | `lp_distance()` | Távolság számítása |
| | `lp_save_json()` | JSON mentés |
| | `lp_load_json()` | JSON betöltése |

---

## Telepítés és futtatás

### 1. Python telepítése
A projekt **Python 3.10+** verzióval működik.  
Letöltés: https://www.python.org/downloads/

---

### 2. Függőségek telepítése
A projekt nem igényel sok extra csomagot.  
A **Tkinter** könyvtárnak telepítve kell lennie.

Windows alatt általában automatikusan települ.  
Ha hiányzik:

```bash
pip install tk
```

### 3. Futtatás
Nyisd meg a projekt mappáját, majd futtasd:
python main.py

---

## Mentés és betöltés
| Művelet | Billentyű |
|--------|-----------|
| Mentés JSON-be | **S** |
| Betöltés | **L** |

---

## 📊 Statisztikák
A játék nyomon követi:
- szintek idejét,
- próbálkozások számát,
- összesített eredményt.

Megnyitás: **M**

---

## Játék célja
- Illeszd az összes kék alakzatot a megfelelő zöld célalakzatra.
- Minden hibás ellenőrzés életet von el.
- Életek elfogyása → **Game Over**.

---

## Fejlesztő
**Broforce2002 / Laczi Péter**

---

## Licenc
- A projekt oktatási célra készült.
- Kereskedelmi felhasználás kizárólag a szerző engedélyével.
