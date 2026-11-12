from random import randint

ekwipunek = {"miecz": 1, "mikstura": 3}
zloto = 50
maks_waga = 20

sklep = {
    "miecz": [4, 30],
    "mikstura": [0.5, 10],
    "tarcza": [5, 35],
    "pochodnia": [1, 5],
    "chleb": [0.4, 4]
}


def oblicz_wage():
    suma = 0
    for nazwa, ilosc in ekwipunek.items():
        suma += sklep[nazwa][0] * ilosc
    return suma


def pokaz_przedmioty():
    print("\n--- EKWIPUNEK ---")

    if not ekwipunek:
        print("Ekwipunek jest pusty.")

    for nazwa, ilosc in ekwipunek.items():
        print(f"{nazwa}: {ilosc} szt.")

    print(f"Złoto: {zloto}")
    print(f"Waga: {oblicz_wage():g}/{maks_waga} kg")


def dodaj_przedmiot():
    global zloto

    print("\n--- SKLEP ---")
    for nazwa, dane in sklep.items():
        print(f"{nazwa} - {dane[1]} złota, {dane[0]} kg")

    print("\n1. Kup przedmiot")
    print("2. Sprzedaj przedmiot")
    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        nazwa = input("Co chcesz kupić? ").lower().strip()

        if not nazwa:
            print("Nie podano nazwy przedmiotu.")
            return

        if nazwa not in sklep:
            waga = randint(1, 5)
            cena = randint(10, 20)
            sklep[nazwa] = [waga, cena]
            print(f"Nowy przedmiot: {nazwa}")
            print(f"Waga: {waga} kg, cena: {cena} złota")

        waga, cena = sklep[nazwa]

        if zloto < cena:
            print("Nie masz wystarczająco dużo złota.")
        elif oblicz_wage() + waga > maks_waga:
            print("Przekroczono maksymalną wagę!")
        else:
            ekwipunek[nazwa] = ekwipunek.get(nazwa, 0) + 1
            zloto -= cena
            print(f"Kupiono {nazwa}!")

    elif wybor == "2":
        nazwa = input("Co chcesz sprzedać? ").lower().strip()

        if ekwipunek.get(nazwa, 0) > 0:
            cena = max(1, sklep[nazwa][1] // 2)
            ekwipunek[nazwa] -= 1
            zloto += cena

            if ekwipunek[nazwa] == 0:
                del ekwipunek[nazwa]

            print(f"Sprzedano {nazwa} za {cena} złota.")
        else:
            print("Nie masz takiego przedmiotu.")

    else:
        print("Nieprawidłowa opcja.")


def uzyj_przedmiotu():
    pokaz_przedmioty()
    nazwa = input("Jakiego przedmiotu chcesz użyć? ").lower().strip()

    if ekwipunek.get(nazwa, 0) > 0:
        ekwipunek[nazwa] -= 1
        print(f"Użyto przedmiotu: {nazwa}")

        if ekwipunek[nazwa] == 0:
            del ekwipunek[nazwa]
    else:
        print("Nie masz takiego przedmiotu.")


def sprawdz_przedmiot():
    nazwa = input("Podaj nazwę przedmiotu: ").lower().strip()

    if ekwipunek.get(nazwa, 0) > 0:
        print(f"Masz {ekwipunek[nazwa]} szt. przedmiotu {nazwa}.")
        print(f"Waga: {sklep[nazwa][0]} kg")
        print(f"Wartość: {sklep[nazwa][1]} złota")
    else:
        print("Nie masz takiego przedmiotu.")


while True:
    print("\n=== EKWIPUNEK BOHATERA ===")
    print("1. Pokaż przedmioty")
    print("2. Dodaj przedmiot / Sklep")
    print("3. Użyj przedmiotu")
    print("4. Sprawdź przedmiot")
    print("5. Wyjdź")

    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        pokaz_przedmioty()
    elif wybor == "2":
        dodaj_przedmiot()
    elif wybor == "3":
        uzyj_przedmiotu()
    elif wybor == "4":
        sprawdz_przedmiot()
    elif wybor == "5":
        print("Koniec gry!")
        break
    else:
        print("Nieprawidłowa opcja.")
