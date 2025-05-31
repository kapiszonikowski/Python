# simulation_core.py
import femm as f
import math
import os
import datetime

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
    
    current_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    simulation_run_folder = f"coilgun_sim_{current_time_str}_{fn_freq}Hz"
    full_results_path = os.path.join(mydir, simulation_run_folder)

    os.makedirs(full_results_path, exist_ok=True)
    print(f"Utworzono główny folder na wyniki: {full_results_path}")

    bitmaps_folder_path = os.path.join(full_results_path, "zdjecia_symulacji")
    os.makedirs(bitmaps_folder_path, exist_ok=True)
    print(f"Utworzono podfolder na zdjęcia symulacji: {bitmaps_folder_path}")

    results_txt_file = os.path.join(full_results_path, f"coilgun_wyniki_{fn_freq}Hz.txt")
    gif_output_file = os.path.join(full_results_path, f"coilgun_animacja_{fn_freq}Hz.gif")

    f.opendocument(os.path.join(mydir, fem_file_name))
    f.mi_saveas(os.path.join(mydir, "temp.fem"))

    with open(results_txt_file, "w") as fp:
        fp.write("Czas[s]\tPrad[A]\tSilaZ[N]\tPrzyspieszenie[m/s^2]\tPredkosc[m/s]\tPolozenie[mm]\n")
    
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

    f.mi_selectgroup(5)
    f.mi_clearselected()

    t = 0
    I = 0
    f.mi_modifycircprop("Coil", 1, I)

    times = []
    currents = []
    forces = []
    accelerations = []
    velocities = []
    positions = []
    
    print("\nRozpoczynam symulację...")
    a = 0
    
    for k in range(steps + 1):
        t = k * dt
        I = Im * math.sin(2 * math.pi * fn * t) * math.exp(-t / tau)
        #if a >= 0 : 
        #    I = Im * math.sin(2 * math.pi * fn * t) * math.exp(-t / tau)
        #elif a < 0:
        #    I = 0

        f.mi_modifycircprop("Coil", 1, I)

        print(f"Krok: {k}/{steps}")

        f.mi_createmesh()
        f.mi_analyze()
        f.mi_loadsolution()

        f.mo_groupselectblock(5)
        F = f.mo_blockintegral(19)

        a = F / m
        v = vp + a * dt
        z = zp + v * dt * 1e3
        dz = v * dt * 1e3

        times.append(t)
        currents.append(I)
        forces.append(F)
        accelerations.append(a)
        velocities.append(v)
        positions.append(zp)

        vp = v
        zp = z

        f.mi_selectgroup(5)
        f.mi_movetranslate(0, dz)
        print(dz)
        f.mi_clearselected()

        with open(results_txt_file, "a") as fp:
            fp.write(f"{t}\t{I}\t{F}\t{a}\t{v}\t{positions[-1]}\n")

        f.mi_clearselected()
        f.mo_clearblock()
        Bmax = 2
        f.mo_showdensityplot(1, 0, Bmax, 0, "bmag")
        f.mo_hidepoints()
        
        bitmap_filename = os.path.join(bitmaps_folder_path, f"pic_{k:04d}.bmp")
        f.mo_savebitmap(bitmap_filename)
        #print(accelerations,"\n")
        #print(min(accelerations))
        #a = min(accelerations)
    
    f.closefemm()
    print("Symulacja zakończona.")
    
    return times, currents, forces, accelerations, velocities, positions