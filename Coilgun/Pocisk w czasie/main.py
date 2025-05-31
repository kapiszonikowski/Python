import Geometry
import simulation_core
import plot_generator
import gif_creator
import os

# Definiuj WSZYSTKIE parametry symulacji i geometrii na poziomie modułu
DEFAULT_SIMULATION_PARAMETERS = {
    # Parametry symulacji
    'm': 0.2,     # [kg] masa pocisku
    'Im': 800,    # [A] prąd maksymalny
    'tau': 0.05,  # [s] stała czasowa tłumienia prądu
    'fn': 20,     # [Hz] częstotliwość prądu
    'dt': 0.0005, # [s] krok czasowy obliczeń
    'steps': 40,  # [-] liczba kroków obliczeń
    'Nwire' : 350, # liczna zwojów cewki

    # Parametry geometryczne
    'r_tube_val': 35/2, # [mm] promień rury (wewnętrzny promień cewki)
    # R_coil_val będzie obliczane na podstawie r_tube_val,
    # Możesz dodać tutaj offset, jeśli jest stały
    'R_coil_offset': 26.25, # [mm] przesunięcie dla zewnętrznego promienia cewki
    'H_coil_val': 115,  # [mm] wysokość cewki

    'R_el_val': 30/2,   # [mm] promień elementu (pocisku)
    'H_el_val': 45,     # [mm] wysokość elementu (pocisku)
    # H0_el_val będzie obliczane
    'R_BC_factor': 4    # Współczynnik dla promienia Boundary Condition
}

def run_single_simulation(sim_params, simulation_id="default"):
    """
    Wykonuje pojedynczą symulację z podanymi parametrami.
    Args:
        sim_params (dict): Słownik zawierający parametry dla tej konkretnej symulacji.
        simulation_id (str): Unikalny identyfikator dla tej symulacji, używany do nazewnictwa folderów.
    """
    print(f"\n--- Rozpoczynanie symulacji: {simulation_id} ---")
    print(f"Parametry: {sim_params}")

    # --- Obliczanie zależnych parametrów geometrycznych ---
    # Wszystkie wartości bazowe pochodzą teraz z sim_params
    r_tube_val = sim_params['r_tube_val']
    H_coil_val = sim_params['H_coil_val']
    H_el_val = sim_params['H_el_val']

    # Obliczenia bazujące na wartościach z sim_params
    R_coil_val = r_tube_val + sim_params['R_coil_offset']
    H0_el_val = -(H_coil_val + H_el_val) / 2
    R_BC_val = sim_params['R_BC_factor'] * H_coil_val

    # --- Tworzenie Geometrii ---
    # Upewnij się, że Geometry.create_coilgun_geometry przyjmuje odpowiednie parametry
    Geometry.create_coilgun_geometry(
        r_tube_val, R_coil_val, H_coil_val,
        sim_params['R_el_val'], H_el_val, H0_el_val, R_BC_val,
        sim_params['Im'], sim_params['Nwire'], sim_params['fn']
    )

    # --- Ustawienia plików i ścieżek ---
    mydir = "./"
    fem_file = "coilgun1.fem"

    # --- 1. Konfiguracja środowiska i folderów ---
    full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file = \
        simulation_core.setup_simulation_environment(mydir, fem_file, sim_params['fn'])

    # --- 2. Pętla obliczeń FEMM ---
    times, currents, forces, accelerations, velocities, positions = \
        simulation_core.run_calculation_loop(sim_params,
                                             (full_results_path, bitmaps_folder_path, results_txt_file, gif_output_file))

    # --- 3. Generowanie wykresów ---
    plot_generator.generate_plots(times, currents, forces,
                                  accelerations, velocities, positions,
                                  full_results_path)

    # --- 4. Generowanie GIF-a ---
    gif_creator.create_gif(bitmaps_folder_path, gif_output_file)

    print(f"--- Symulacja {simulation_id} zakończona sukcesem! ---")

# Reszta kodu (funkcja main) pozostaje bez większych zmian,
# ponieważ pracuje już na ujednoliconym słowniku parametrów.
def main():
    """
    Główna funkcja koordynująca uruchamianie wielu symulacji.
    """
    print("--- Rozpoczynanie serii symulacji ---")

    # PRZYKŁAD: Loopowanie po masie i promieniu rury
    # Zmieniamy masę 'm' i promień rury 'r_tube_val'
    freqs = [20, 50, 100]

    for f in freqs:
        current_params = DEFAULT_SIMULATION_PARAMETERS.copy()
        current_params['fn'] = f
        
        # Możesz dodać unikalny identyfikator do nazwy folderu
        simulation_id = ""
        run_single_simulation(current_params, simulation_id)

    print("\nWSZYSTKIE SYMULACJE ZAKOŃCZONE!")

if __name__ == "__main__":
    main()