import femm as f
import math
import datetime

f.openfemm()
mydir = "./"
file = "coilgun1.fem"
f.opendocument(mydir + file) # Otwórz plik projektu FEMM (podaj nazwę własnego projektu)
f.mi_saveas(mydir + "temp.fem") # Zapisz projekt jako plik tymczasowy

# Parametry edytowalne
m = 0.2  # [kg] masa pocisku
Im = 800  # [A] prąd maksymalny
tau = 0.05  # [s] stała czasowa tłumienia prądu
fn = 100  # [Hz] częstotliwość prądu
dt = 0.0005  # [s] krok czasowy obliczeń - dobrać eksperymentalnie
steps = 40  # [-] liczba kroków obliczeń - dobrać eksperymentalnie

# Generuj unikalną nazwę pliku dla wyników z datą i czasem
current_time = datetime.datetime.now().strftime("%d_%m_%y_%H_%M")
file_name = f"coilgun_wyniki_{current_time}_{fn}Hz"

# Otwórz plik i zapisz nagłówek
with open(mydir + file_name + ".txt", "w") as fp:
    fp.write("Czas[s]\tPrad[A]\tSilaZ[N]\tPrzyspieszenie[m/s/s]\tPredkosc[m/s]\tPolozenie[cm]\n")

vp = 0  # prędkość początkowa [m/s]
zp = 0  # położenie początkowe [cm]

# Wybór grupy 5 (pocisk) i wyczyszczenie zaznaczenia
f.mi_selectgroup(5)
f.mi_clearselected()

# Definicja czasu oraz prądu cewki (początkowy czas t=0)
t = 0
I = 0  # Prąd początkowy ustawiony na 0

# Zmiana parametru obwodu 'Coil' (prąd całkowity)
# propnum 1 oznacza "Total current" (prąd całkowity)
f.mi_modifycircprop("Coil", 1, I)

# Pętla obliczeń
data = {}  # Słownik na wyniki obliczeń
for k in range(steps + 1):
    t = k * dt
    # Oblicz prąd zgodnie z falą sinusoidalną z wykładniczym zanikiem
    I = Im * math.sin(2 * math.pi * fn * t) * math.exp(-t / tau)
    f.mi_modifycircprop("Coil", 1, I)  # Zaktualizuj prąd w cewce FEMM

    print(f"{k}/{steps}")  # Monitorowanie kroku obliczeń

    f.mi_createmesh() # Odkomentować, jeśli siatka ma być tworzona w każdym kroku
    f.mi_analyze()  # Uruchom obliczenia
    f.mi_loadsolution()  # Wczytaj wyniki (postprocesor)

    # Wybierz bloki z grupy 5 (pocisk)
    f.mo_groupselectblock(5)
    F = f.mo_blockintegral(19)  # Wyznaczanie siły działającej na pocisk (typ całki 19 dla siły)

    a = F / m  # przyspieszenie
    v = vp + a * dt  # prędkość chwilowa (całkowanie metodą prostokątów)
    z = zp + v * dt * 100  # obliczanie kolejnego położenia pocisku (+ przeliczenie na centymetry)
    dz = v * dt * 100  # względne przesunięcie pocisku do następnej pozycji (w centymetrach!)

    # Zapisz wyniki dla bieżącego kroku
    data[k] = {
        "time": t,
        "current": I,
        "force": F,
        "acceleration": a,
        "velocity": v,
        "position": zp  # Położenie (ale musi być z chwili wcześniejszej, jak w oryginalnym kodzie)
    }

    vp = v  # Przypisanie wyników do chwili wcześniejszej (dla kolejnego kroku)
    # ap = a # Nieużywane w oryginalnym kodzie
    zp = z  # Aktualizuj położenie początkowe dla kolejnego kroku
    # Fp = F # Nieużywane w oryginalnym kodzie

    # Przesunięcie pocisku do nowego położenia
    f.mi_selectgroup(5)  # Wybór grupy 5 - pocisk
    f.mi_movetranslate(0, dz)  # Przesunięcie o (dr=0,dz) grupy elementów
    f.mi_clearselected()

    # Zapis do pliku
    with open(mydir + file_name + ".txt", "a") as fp:
        fp.write(f"{data[k]['time']}\t{data[k]['current']}\t{data[k]['force']}\t{data[k]['acceleration']}\t{data[k]['velocity']}\t{data[k]['position']}\n")

    # Zapis bitmapy
    f.mi_clearselected()
    f.mo_clearblock()
    Bmax = 2  # [T] maksymalna indukcja - dobrać eksperymentalnie
    f.mo_showdensityplot(1, 0, Bmax, 0, "bmag") # Pokaż mapę gęstości strumienia magnetycznego
    f.mo_hidepoints()  # Ukryj siatkę
    # f.mo_showvectorplot(2,5) # Odkomentuj, aby pokazać plot wektorowy
    # f.mo_hidecontourplot() # Odkomentuj, aby ukryć plot konturowy
    f.mo_savebitmap(mydir + f"{file_name}_pic_{k}.bmp")

