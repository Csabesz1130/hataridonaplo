# esemeny.py
from datetime import datetime, date

class Esemeny:
    """Egy esemény adatainak tárolására szolgáló osztály"""
    def __init__(self, azonosito: int, datum: date, idopont: str, 
                 helyszin: str, nev: str, megjegyzes: str = ""):
        self.azonosito = azonosito
        self.datum = datum
        self.idopont = idopont
        self.helyszin = helyszin
        self.nev = nev
        self.megjegyzes = megjegyzes

    def __str__(self) -> str:
        return (f"[{self.azonosito}] {self.datum} {self.idopont} - "
                f"{self.nev} ({self.helyszin})")

# esemenykezelo.py
from typing import List, Optional
import json
from datetime import datetime, date, timedelta

class EsemenyKezelo:
    """Események kezelését végző osztály"""
    def __init__(self):
        self.esemenyek: List[Esemeny] = []
        self.kovetkezo_azonosito = 1

    def uj_esemeny(self, datum: str, idopont: str, helyszin: str, 
                   nev: str, megjegyzes: str = "") -> bool:
        """Új esemény létrehozása"""
        try:
            # Dátum ellenőrzése és konvertálása
            datum_obj = datetime.strptime(datum, "%Y-%m-%d").date()
            
            esemeny = Esemeny(
                azonosito=self.kovetkezo_azonosito,
                datum=datum_obj,
                idopont=idopont,
                helyszin=helyszin,
                nev=nev,
                megjegyzes=megjegyzes
            )
            self.esemenyek.append(esemeny)
            self.kovetkezo_azonosito += 1
            return True
        except ValueError:
            return False

    def lista_nap(self, datum: date) -> List[Esemeny]:
        """Adott napi események listázása"""
        return [e for e in self.esemenyek if e.datum == datum]

    def mentes_fajlba(self, fajlnev: str) -> bool:
        """Események mentése JSON fájlba"""
        try:
            with open(fajlnev, 'w', encoding='utf-8') as f:
                adatok = []
                for esemeny in self.esemenyek:
                    adatok.append({
                        'azonosito': esemeny.azonosito,
                        'datum': esemeny.datum.isoformat(),
                        'idopont': esemeny.idopont,
                        'helyszin': esemeny.helyszin,
                        'nev': esemeny.nev,
                        'megjegyzes': esemeny.megjegyzes
                    })
                json.dump(adatok, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Hiba a mentés során: {e}")
            return False

    def betoltes_fajlbol(self, fajlnev: str) -> bool:
        """Események betöltése JSON fájlból"""
        try:
            with open(fajlnev, 'r', encoding='utf-8') as f:
                adatok = json.load(f)
            
            self.esemenyek = []
            max_azonosito = 0
            
            for adat in adatok:
                esemeny = Esemeny(
                    azonosito=adat['azonosito'],
                    datum=date.fromisoformat(adat['datum']),
                    idopont=adat['idopont'],
                    helyszin=adat['helyszin'],
                    nev=adat['nev'],
                    megjegyzes=adat['megjegyzes']
                )
                self.esemenyek.append(esemeny)
                max_azonosito = max(max_azonosito, esemeny.azonosito)
            
            self.kovetkezo_azonosito = max_azonosito + 1
            return True
        except Exception as e:
            print(f"Hiba a betöltés során: {e}")
            return False

# main.py
def main():
    kezelo = EsemenyKezelo()
    
    while True:
        print("\nHatáridőnapló - Félkész változat")
        print("1. Új esemény")
        print("2. Mai események")
        print("3. Mentés fájlba")
        print("4. Betöltés fájlból")
        print("5. Kilépés")
        
        valasztas = input("\nVálasszon (1-5): ")
        
        if valasztas == "1":
            print("\nÚj esemény létrehozása")
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            idopont = input("Időpont (ÓÓ:PP): ")
            helyszin = input("Helyszín: ")
            nev = input("Esemény neve: ")
            megjegyzes = input("Megjegyzés: ")
            
            if kezelo.uj_esemeny(datum, idopont, helyszin, nev, megjegyzes):
                print("Esemény sikeresen létrehozva!")
            else:
                print("Hiba történt az esemény létrehozásakor!")
                
        elif valasztas == "2":
            mai_esemenyek = kezelo.lista_nap(date.today())
            if mai_esemenyek:
                print("\nMai események:")
                for esemeny in mai_esemenyek:
                    print(esemeny)
            else:
                print("Nincsenek mai események!")
                
        elif valasztas == "3":
            fajlnev = input("Adja meg a fájlnevet: ")
            if kezelo.mentes_fajlba(fajlnev):
                print("Események sikeresen mentve!")
            else:
                print("Hiba történt a mentés során!")
                
        elif valasztas == "4":
            fajlnev = input("Adja meg a fájlnevet: ")
            if kezelo.betoltes_fajlbol(fajlnev):
                print("Események sikeresen betöltve!")
            else:
                print("Hiba történt a betöltés során!")
                
        elif valasztas == "5":
            break

if __name__ == "__main__":
    main()
