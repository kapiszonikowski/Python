# simulation_runner.py
import femm as f
import os
import datetime
from geometry_creator import create_coilgun_geometry # Importuj funkcję do tworzenia geometrii

def run_single_simulation(coilgun_params, current_H0_el, material_el):
    """
    Uruchamia pojedynczą symulację FEMM dla danego położenia pocisku i materiału.
    Zwraca wyliczoną siłę.
    """
    mydir = "./"
    fem_file_name = "coilgun1.fem" # Tymczasowy plik do symulacji

    # 1. Stwórz geometrię dla bieżącego H0_el i materiału
    create_coilgun_geometry(
        coilgun_params['r_tube'],
        coilgun_params['R_coil'],
        coilgun_params['H_coil'],
        coilgun_params['R_el'],
        coilgun_params['H_el'],
        current_H0_el, # Zmieniamy H0_el
        coilgun_params['R_BC'],
        coilgun_params['I_current'],
        coilgun_params['N_wire'],
        coilgun_params['freq'],
        material_el # Zmieniamy materiał
    )

    # 2. Otwórz FEMM, załaduj plik
    f.openfemm()
    f.opendocument(os.path.join(mydir, fem_file_name))

    # 3. Utwórz siatkę, przeprowadź analizę, załaduj rozwiązanie
    f.mi_createmesh()
    f.mi_analyze()
    f.mi_loadsolution()

    # 4. Oblicz siłę na grupie 5 (pocisk)
    f.mo_groupselectblock(5)
    force = f.mo_blockintegral(19) # Integral 19 to force in Z direction

    # 5. Zamknij okno postprocesora i FEMM
    f.mo_close()
    f.closefemm()

    # 6. Usuń tymczasowy plik FEMM i jego rozwiązanie
    if os.path.exists(os.path.join(mydir, fem_file_name)):
        os.remove(os.path.join(mydir, fem_file_name))
    if os.path.exists(os.path.join(mydir, fem_file_name.replace(".fem", ".ans"))):
        os.remove(os.path.join(mydir, fem_file_name.replace(".fem", ".ans")))

    return force

def run_multiple_simulations(H0_range, coilgun_params, materials):
    """
    Przeprowadza serię symulacji dla różnych położeń pocisku i materiałów.

    Args:
        H0_range (list): Lista położeń H0_el (współrzędne Z środka pocisku) [mm].
        coilgun_params (dict): Słownik z parametrami cewki i pocisku.
        materials (list): Lista nazw materiałów do testowania (np. ["Ideal_Iron", "Aluminum, 1100"]).

    Returns:
        dict: Słownik wyników, gdzie kluczem jest nazwa materiału, a wartością lista krotek (H0_el, force).
    """
    results = {mat: [] for mat in materials}

    print("\n--- Rozpoczynanie serii symulacji ---")
    for material in materials:
        print(f"\nSymulacja dla materiału: {material}")
        for h0 in H0_range:
            print(f"  Symulacja dla H0_el = {h0} mm...")
            force = run_single_simulation(coilgun_params, h0, material)
            results[material].append((h0, force))
            print(f"    Siła wyznaczona: {force:.4f} N")
    print("\n--- Symulacje zakończone ---")
    return results