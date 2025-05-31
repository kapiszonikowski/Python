import femm as f
import math
import datetime
import os
import matplotlib.pyplot as plt
import imageio
import re

def setup_simulation_environment(mydir, fem_file_name, fn_freq):
    """
    Konfiguruje środowisko FEMM, tworzy strukturę folderów dla wyników
    i otwiera plik projektu FEMM.

    Args:
        mydir (str): Ścieżka do katalogu roboczego.
        fem_file_name (str): Nazwa pliku projektu FEMM.
        fn_freq (int): Częstotliwość prądu (używana w nazwie folderu).

    Returns:
        tuple: (full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file)
    """
    f.openfemm()
    
    # Generuj unikalną nazwę folderu na wyniki na podstawie daty i czasu
    current_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    simulation_run_folder = f"coilgun_sim_{current_time_str}_{fn_freq}Hz"
    full_results_path = os.path.join(mydir, simulation_run_folder)

    # Utwórz główny folder na wyniki
    os.makedirs(full_results_path, exist_ok=True)
    print(f"Utworzono główny folder na wyniki: {full_results_path}")

    # Utwórz podfolder na zdjęcia bitmap
    bitmaps_folder_path = os.path.join(full_results_path, "zdjecia_symulacji")
    os.makedirs(bitmaps_folder_path, exist_ok=True)
    print(f"Utworzono podfolder na zdjęcia symulacji: {bitmaps_folder_path}")

    # Pełne ścieżki do plików w nowo utworzonych folderach
    results_txt_file = os.path.join(full_results_path, f"coilgun_wyniki_{fn_freq}Hz.txt")
    gif_output_file = os.path.join(full_results_path, f"coilgun_animacja_{fn_freq}Hz.gif")

    # Otwórz plik projektu FEMM i zapisz jako tymczasowy
    f.opendocument(os.path.join(mydir, fem_file_name))
    f.mi_saveas(os.path.join(mydir, "temp.fem"))

    # Otwórz plik z danymi i zapisz nagłówek
    with open(results_txt_file, "w") as fp:
        fp.write("Czas[s]\tPrad[A]\tSilaZ[N]\tPrzyspieszenie[m/s/s]\tPredkosc[m/s]\tPolozenie[cm]\n")
    
    return full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file

def run_calculation_loop(params, paths):
    """
    Wykonuje pętlę obliczeniową FEMM, zbiera dane i zapisuje bitmapy.

    Args:
        params (dict): Słownik parametrów symulacji (m, Im, tau, fn, dt, steps).
        paths (tuple): Ścieżki do folderów i plików (full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file).

    Returns:
        tuple: (times, currents, forces, accelerations, velocities, positions) - zebrane dane z symulacji.
    """
    m, Im, tau, fn, dt, steps = params['m'], params['Im'], params['tau'], params['fn'], params['dt'], params['steps']
    full_results_path, bitmaps_folder_path, results_txt_file, _ = paths

    vp = 0  # prędkość początkowa [m/s]
    zp = 0  # położenie początkowe [cm]

    f.mi_selectgroup(5) # Wybór grupy 5 (pocisk)
    f.mi_clearselected() # Wyczyszczenie zaznaczenia

    t = 0 # Czas początkowy
    I = 0 # Prąd początkowy
    f.mi_modifycircprop("Coil", 1, I) # Ustaw prąd początkowy w cewce

    # Listy do przechowywania danych do wykresów
    times = []
    currents = []
    forces = []
    accelerations = []
    velocities = []
    positions = []
    
    print("\nRozpoczynam symulację...")
    for k in range(steps + 1):
        t = k * dt
        I = Im * math.sin(2 * math.pi * fn * t) * math.exp(-t / tau)
        f.mi_modifycircprop("Coil", 1, I)

        print(f"Krok: {k}/{steps}")

        f.mi_createmesh() # Tworzenie siatki
        f.mi_analyze()    # Uruchomienie analizy
        f.mi_loadsolution() # Wczytanie wyników

        f.mo_groupselectblock(5)
        F = f.mo_blockintegral(19) # Obliczenie siły

        a = F / m
        v = vp + a * dt
        z = zp + v * dt * 100 # Przeliczenie na centymetry
        dz = v * dt * 100     # Przesunięcie w cm

        # Zapis danych do list
        times.append(t)
        currents.append(I)
        forces.append(F)
        accelerations.append(a)
        velocities.append(v)
        positions.append(zp) # Zapisujemy położenie z PRZED przesunięcia

        vp = v
        zp = z

        f.mi_selectgroup(5)
        f.mi_movetranslate(0, dz) # Przesunięcie pocisku
        f.mi_clearselected()

        # Zapis do pliku tekstowego
        with open(results_txt_file, "a") as fp:
            fp.write(f"{t}\t{I}\t{F}\t{a}\t{v}\t{positions[-1]}\n")

        # Zapis bitmapy
        f.mi_clearselected()
        f.mo_clearblock()
        Bmax = 2
        f.mo_showdensityplot(1, 0, Bmax, 0, "bmag")
        f.mo_hidepoints()
        
        bitmap_filename = os.path.join(bitmaps_folder_path, f"pic_{k:04d}.bmp")
        f.mo_savebitmap(bitmap_filename)
    
    f.closefemm() # Zamknij instancję FEMM
    print("Symulacja zakończona.")
    
    return times, currents, forces, accelerations, velocities, positions

def generate_plots(times, currents, forces, accelerations, velocities, positions, full_results_path):
    """
    Generuje i zapisuje wykresy danych z symulacji.

    Args:
        times (list): Lista czasów.
        currents (list): Lista wartości prądu.
        forces (list): Lista wartości siły.
        accelerations (list): Lista wartości przyspieszenia.
        velocities (list): Lista wartości prędkości.
        positions (list): Lista wartości położenia.
        full_results_path (str): Ścieżka do głównego folderu wyników.
    """
    print("\nGenerowanie wykresów...")

    # Wykres 1: Prąd i Siła
    fig1, ax1_1 = plt.subplots(figsize=(12, 7))
    ax1_2 = ax1_1.twinx()
    
    ax1_1.plot(times, currents, 'b-', label='Prąd [A]')
    ax1_2.plot(times, forces, 'r-', label='Siła Z [N]')

    ax1_1.set_xlabel('Czas [s]')
    ax1_1.set_ylabel('Prąd [A]', color='blue')
    ax1_2.set_ylabel('Siła Z [N]', color='red')
    
    ax1_1.tick_params(axis='y', labelcolor='blue')
    ax1_2.tick_params(axis='y', labelcolor='red')

    lines1, labels1 = ax1_1.get_legend_handles_labels()
    lines2, labels2 = ax1_2.get_legend_handles_labels()
    ax1_1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    fig1.suptitle('Przebieg Prądu i Siły od Czasu')
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(full_results_path, 'wykres_prad_sila.png'))
    plt.close(fig1)

    # Wykres 2: Prędkość, Położenie i Przyspieszenie
    fig2, ax2_1 = plt.subplots(figsize=(12, 7))
    ax2_2 = ax2_1.twinx()
    ax2_3 = ax2_1.twinx()

    ax2_1.plot(times, velocities, 'g-', label='Prędkość [m/s]')
    ax2_1.set_xlabel('Czas [s]')
    ax2_1.set_ylabel('Prędkość [m/s]', color='green')
    ax2_1.tick_params(axis='y', labelcolor='green')

    ax2_2.plot(times, positions, 'm-', label='Położenie [cm]')
    ax2_2.set_ylabel('Położenie [cm]', color='magenta')
    ax2_2.tick_params(axis='y', labelcolor='magenta')

    ax2_3.spines['right'].set_position(('outward', 60))
    ax2_3.plot(times, accelerations, 'c-', label='Przyspieszenie [m/s/s]')
    ax2_3.set_ylabel('Przyspieszenie [m/s/s]', color='cyan')
    ax2_3.tick_params(axis='y', labelcolor='cyan')

    lines1, labels1 = ax2_1.get_legend_handles_labels()
    lines2, labels2 = ax2_2.get_legend_handles_labels()
    lines3, labels3 = ax2_3.get_legend_handles_labels()
    ax2_1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper left')

    fig2.suptitle('Przebieg Prędkości, Położenia i Przyspieszenia od Czasu')
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(full_results_path, 'wykres_predkosc_polozenie_przyspieszenie.png'))
    plt.close(fig2)
    
    print("Wykresy zostały zapisane.")

def create_gif(bitmaps_folder_path, gif_output_file, fps=10):
    """
    Tworzy plik GIF z serii obrazów BMP.

    Args:
        bitmaps_folder_path (str): Ścieżka do folderu zawierającego pliki BMP.
        gif_output_file (str): Pełna ścieżka do pliku wyjściowego GIF.
        fps (int): Liczba klatek na sekundę dla GIF-a.
    """
    print("\nGenerowanie GIF-a...")
    images = []
    filepaths = []

    pattern = re.compile(r"pic_(\d{4})\.bmp$")

    for filename in os.listdir(bitmaps_folder_path):
        if filename.endswith(".bmp"):
            match = pattern.match(filename)
            if match:
                step_number = int(match.group(1))
                filepaths.append((step_number, os.path.join(bitmaps_folder_path, filename)))

    filepaths.sort(key=lambda x: x[0])

    for _, filepath in filepaths:
        try:
            images.append(imageio.imread(filepath))
        except Exception as e:
            print(f"Błąd podczas wczytywania {filepath}: {e}")
            continue

    if images:
        imageio.mimsave(gif_output_file, images, fps=fps)
        print(f"GIF '{gif_output_file}' został utworzony.")
    else:
        print("Brak obrazów BMP do utworzenia GIF-a. Sprawdź ścieżkę i nazwy plików.")

def main():
    """Główna funkcja koordynująca całą symulację i analizę."""
    # --- Parametry edytowalne ---
    simulation_parameters = {
        'm': 0.2,     # [kg] masa pocisku
        'Im': 800,    # [A] prąd maksymalny
        'tau': 0.05,  # [s] stała czasowa tłumienia prądu
        'fn': 100,    # [Hz] częstotliwość prądu
        'dt': 0.0005, # [s] krok czasowy obliczeń
        'steps': 40   # [-] liczba kroków obliczeń
    }

    # --- Ustawienia plików ---
    mydir = "./"
    fem_file = "coilgun1.fem"

    # --- 1. Konfiguracja środowiska i folderów ---
    full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file = \
        setup_simulation_environment(mydir, fem_file, simulation_parameters['fn'])

    # --- 2. Pętla obliczeń FEMM ---
    times, currents, forces, accelerations, velocities, positions = \
        run_calculation_loop(simulation_parameters, (full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file))

    # --- 3. Generowanie wykresów ---
    generate_plots(times, currents, forces, accelerations, velocities, positions, full_results_path)

    # --- 4. Generowanie GIF-a ---
    create_gif(bitmaps_folder_path, gif_output_file)

    print("\nProces zakończony sukcesem!")

if __name__ == "__main__":
    main()