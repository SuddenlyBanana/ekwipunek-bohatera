"""Tekstowy ekwipunek bohatera z limitem wagi i sklepem."""

from dataclasses import dataclass


MAKSYMALNA_WAGA = 20.0


@dataclass(frozen=True)
class Przedmiot:
    """Opis rodzaju przedmiotu dostępnego w grze."""

    nazwa: str
    waga: float
    cena: int
    opis: str
    efekt_uzycia: str


KATALOG = {
    "miecz": Przedmiot(
        "miecz", 4.0, 30, "Podstawowa broń do walki.", "Miecz zużył się w walce."
    ),
    "mikstura": Przedmiot(
        "mikstura", 0.5, 10, "Przywraca punkty życia.", "Odzyskujesz punkty życia."
    ),
    "tarcza": Przedmiot(
        "tarcza", 5.0, 35, "Chroni przed atakami.", "Tarcza pękła, ale ochroniła bohatera."
    ),
    "pochodnia": Przedmiot(
        "pochodnia", 1.0, 5, "Rozświetla ciemne miejsca.", "Pochodnia rozświetla drogę."
    ),
    "chleb": Przedmiot(
        "chleb", 0.4, 4, "Prosty prowiant na wyprawę.", "Zjadasz chleb i odzyskujesz siły."
    ),
}


class Ekwipunek:
    """Przechowuje przedmioty, złoto i pilnuje limitu wagi."""

    def __init__(
        self,
        przedmioty: dict[str, int] | None = None,
        zloto: int = 50,
        maksymalna_waga: float = MAKSYMALNA_WAGA,
    ) -> None:
        self.przedmioty = dict(przedmioty or {})
        self.zloto = zloto
        self.maksymalna_waga = maksymalna_waga

    def aktualna_waga(self) -> float:
        return sum(KATALOG[nazwa].waga * ilosc for nazwa, ilosc in self.przedmioty.items())

    def czy_zmiesci(self, nazwa: str, ilosc: int = 1) -> bool:
        return self.aktualna_waga() + KATALOG[nazwa].waga * ilosc <= self.maksymalna_waga

    def kup(self, nazwa: str) -> tuple[bool, str]:
        przedmiot = KATALOG[nazwa]
        if self.zloto < przedmiot.cena:
            return False, "Nie masz wystarczająco dużo złota."
        if not self.czy_zmiesci(nazwa):
            return False, "Ten przedmiot przekroczyłby maksymalną wagę ekwipunku."

        self.zloto -= przedmiot.cena
        self.przedmioty[nazwa] = self.przedmioty.get(nazwa, 0) + 1
        return True, f"Kupiono: {nazwa}."

    def sprzedaj(self, nazwa: str) -> tuple[bool, str]:
        if self.przedmioty.get(nazwa, 0) == 0:
            return False, "Nie masz takiego przedmiotu."

        cena_sprzedazy = max(1, KATALOG[nazwa].cena // 2)
        self._usun_jeden(nazwa)
        self.zloto += cena_sprzedazy
        return True, f"Sprzedano {nazwa} za {cena_sprzedazy} szt. złota."

    def uzyj(self, nazwa: str) -> tuple[bool, str]:
        if self.przedmioty.get(nazwa, 0) == 0:
            return False, "Nie masz takiego przedmiotu."

        self._usun_jeden(nazwa)
        return True, KATALOG[nazwa].efekt_uzycia

    def _usun_jeden(self, nazwa: str) -> None:
        self.przedmioty[nazwa] -= 1
        if self.przedmioty[nazwa] == 0:
            del self.przedmioty[nazwa]


def pokaz_przedmioty(ekwipunek: Ekwipunek) -> None:
    print("\n--- EKWIPUNEK ---")
    if not ekwipunek.przedmioty:
        print("Ekwipunek jest pusty.")
    else:
        for nazwa, ilosc in sorted(ekwipunek.przedmioty.items()):
            przedmiot = KATALOG[nazwa]
            print(f"- {nazwa}: {ilosc} szt. (waga jednej szt.: {przedmiot.waga:g} kg)")
    print(f"Złoto: {ekwipunek.zloto}")
    print(
        f"Waga: {ekwipunek.aktualna_waga():g}/{ekwipunek.maksymalna_waga:g} kg"
    )


def pokaz_sklep() -> None:
    print("\n--- SKLEP ---")
    for numer, przedmiot in enumerate(KATALOG.values(), start=1):
        print(
            f"{numer}. {przedmiot.nazwa.capitalize()} - {przedmiot.cena} złota, "
            f"{przedmiot.waga:g} kg"
        )


def wybierz_z_katalogu(komunikat: str) -> str | None:
    nazwa = input(komunikat).strip().lower()
    if nazwa not in KATALOG:
        print("Nie ma takiego przedmiotu w katalogu.")
        return None
    return nazwa


def obsluz_sklep(ekwipunek: Ekwipunek) -> None:
    while True:
        pokaz_sklep()
        print(f"Twoje złoto: {ekwipunek.zloto}")
        print("\n1. Kup przedmiot")
        print("2. Sprzedaj przedmiot")
        print("3. Wróć do menu")
        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            nazwa = wybierz_z_katalogu("Podaj nazwę przedmiotu do kupienia: ")
            if nazwa is not None:
                _, komunikat = ekwipunek.kup(nazwa)
                print(komunikat)
        elif wybor == "2":
            if not ekwipunek.przedmioty:
                print("Nie masz nic do sprzedania.")
                continue
            pokaz_przedmioty(ekwipunek)
            nazwa = wybierz_z_katalogu("Podaj nazwę przedmiotu do sprzedania: ")
            if nazwa is not None:
                _, komunikat = ekwipunek.sprzedaj(nazwa)
                print(komunikat)
        elif wybor == "3":
            return
        else:
            print("Nieprawidłowa opcja. Wybierz 1, 2 lub 3.")


def uzyj_przedmiotu(ekwipunek: Ekwipunek) -> None:
    if not ekwipunek.przedmioty:
        print("Ekwipunek jest pusty.")
        return
    pokaz_przedmioty(ekwipunek)
    nazwa = input("Podaj nazwę przedmiotu do użycia: ").strip().lower()
    if nazwa not in KATALOG:
        print("Nie ma takiego przedmiotu.")
        return
    _, komunikat = ekwipunek.uzyj(nazwa)
    print(komunikat)


def sprawdz_przedmiot(ekwipunek: Ekwipunek) -> None:
    nazwa = input("Podaj nazwę przedmiotu do sprawdzenia: ").strip().lower()
    if nazwa not in KATALOG:
        print("Nie ma takiego przedmiotu w katalogu.")
        return

    przedmiot = KATALOG[nazwa]
    ilosc = ekwipunek.przedmioty.get(nazwa, 0)
    print(f"\nNazwa: {przedmiot.nazwa}")
    print(f"Opis: {przedmiot.opis}")
    print(f"Ilość w ekwipunku: {ilosc}")
    print(f"Waga jednej sztuki: {przedmiot.waga:g} kg")
    print(f"Cena w sklepie: {przedmiot.cena} złota")
    print(f"Cena sprzedaży: {max(1, przedmiot.cena // 2)} złota")


def uruchom_gre() -> None:
    # Odpowiednik danych początkowych z zadania:
    # {"miecz": 1, "mikstura": 3, "zloto": 50}
    ekwipunek = Ekwipunek({"miecz": 1, "mikstura": 3}, zloto=50)

    while True:
        print("\n=== EKWIPUNEK BOHATERA ===")
        print("1. Pokaż przedmioty")
        print("2. Dodaj/kup lub sprzedaj przedmiot")
        print("3. Użyj przedmiotu")
        print("4. Sprawdź przedmiot")
        print("5. Wyjdź")
        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            pokaz_przedmioty(ekwipunek)
        elif wybor == "2":
            obsluz_sklep(ekwipunek)
        elif wybor == "3":
            uzyj_przedmiotu(ekwipunek)
        elif wybor == "4":
            sprawdz_przedmiot(ekwipunek)
        elif wybor == "5":
            print("Do zobaczenia!")
            break
        else:
            print("Nieprawidłowa opcja. Wybierz liczbę od 1 do 5.")


if __name__ == "__main__":
    uruchom_gre()
