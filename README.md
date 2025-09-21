# LP Games - Shape Evolution

##  Leírás
A **Shape Evolution** egy kirakós játék, ahol a cél, hogy a kék színű alakzatokat mozgatással, forgatással és méretezéssel pontosan a zöld célalakzatokkal fedésbe hozd.  
A játék a **Python** és a **Tkinter** könyvtár segítségével készült.

Ez a projekt egy tanulási és fejlesztési célú alkalmazás, amely jól példázza a GUI programozást, interaktív grafikus elemek kezelését, valamint a játéklogika megvalósítását.

---

##  Játékmenet
- **Egér**: alakzat mozgatása
- **Egér görgő**: méretezés
- **A/D billentyű**: forgatás ±2°
- **Shift + A/D**: forgatás ±10°
- **Enter**: ellenőrzés (helyes pozíció ellenőrzése)
- **Space**: következő szint
- **S**: játékállás mentése
- **L**: játékállás betöltése
- **M**: statisztika megtekintése
- **R**: új játék indítása

Célod, hogy minden szinten az összes kék alakzatot pontosan illeszd a zöld célhoz, mielőtt elfogynának az életeid.

---

## Projekt felépítése
| Fájlnév / Mappa                  | Leírás                                            |
| -------------------------------- | ------------------------------------------------- |
| **LP_Games_Shape_Evolution/**    | A teljes projekt gyökérkönyvtára                  |
| ├── **main.py**                  | A fő belépési pont, innen indul az alkalmazás     |
| ├── **lp_app.py**                | A fő alkalmazás és a GUI logika                   |
| ├── **lp_game.py**               | A játék logikája és a szintek kezelése            |
| ├── **lp_shapes.py**             | Alakzatok definíciói és kirajzolása               |
| ├── **lp_stats.py**              | A játék statisztikáinak kezelése                  |
| ├── **lp_utils.py**              | Segédfüggvények (matematikai és egyéb számítások) |
| └── **assets/**                   | Képek és egyéb fájlok, pl. `logo.png`             |

---

##  Telepítés és futtatás

### 1. Python telepítése
A projekt Python 3.10+ verzióval működik.  
[Python letöltése](https://www.python.org/downloads/)

---

### 2. Függőségek telepítése
A projekt nem igényel sok extra csomagot, de a **Tkinter** könyvtárnak telepítve kell lennie.  
Windows esetén ez általában alapból telepítve van.  
Ha hiányzik:
```bash
pip install tk
```
### 3. Futtatás
Navigálj a projekt mappájába, majd futtasd:
python main.py

##  Mentés és betöltés
- S billentyű – Játékállás mentése JSON fájlba.
- L billentyű – Előzőleg mentett állás betöltése.
-A JSON fájl hordozható, így más gépen is folytatható a játék.

##  Statisztikák
- A játék nyomon követi:
- hány szintet játszottál le,
- hány sikeres és sikertelen próbálkozásod volt,
- szintek teljesítési idejét,
- összesített eredményeidet.
- A statisztika megnyitása: M billentyű.

##  Játék célja
- Illeszd az összes kék alakzatot a zöld célalakzatokra.
- Ha elég közel vagy, a program automatikusan SNAP funkcióval igazítja a helyére.
- Minden hibás ellenőrzés életet von le.
- Ha az életeid elfogynak → Game Over.

##  Fejlesztő
**Broforce2002**
- A projekt célja a Python és Tkinter alaposabb megismerése, valamint a játékfejlesztési alapok gyakorlása.

##  Licenc
- Ez a projekt személyes és tanulási célokra készült.
- Kereskedelmi felhasználása kizárólag a fejlesztő engedélyével lehetséges.
