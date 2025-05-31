# main.py
import os
import femm
from simulation_runner import run_multiple_simulations
from analysis_and_plotting import save_results_to_txt, plot_results

def main():
    # --- 1. Parametry Coilguna (z Twojego kodu) ---
    # Jednostki: milimetry
    coilgun_parameters = {
        'r_tube': 35/2,
        'R_coil': (35/2) + 26.25,
        'H_coil': 115,
        'R_el': 30/2,
        'H_el': 45,
        'R_BC': 3 * 115, # Promień obszaru powietrza
        'I_current': 800,
        'N_wire': 350, # Liczba zwojów
        'freq': 50 # Częstotliwość (dla magnetostatyki zazwyczaj 0, ale tutaj 50)
    }

    H0_start = -120
    H0_end = 120
    num_points = 40 # Liczba punktów do symulacji
    H0_positions = [H0_start + i * (H0_end - H0_start) / (num_points - 1) for i in range(num_points)]
    print(H0_positions)

    # --- 3. Materiały do testowania ---
    materials_to_test = ["Ideal_Iron", "Copper"]

    # --- 4. Uruchomienie Symulacji ---
    simulation_results = run_multiple_simulations(H0_positions, coilgun_parameters, materials_to_test)

    # --- 5. Zapis Wyników i Wykresy ---
    output_directory = "coilgun_simulation_results"
    save_results_to_txt(simulation_results, output_directory)
    plot_results(simulation_results, output_directory)

    print(f"\nKompletna analiza zakończona. Wyniki zapisane w folderze: {output_directory}")

if __name__ == "__main__":   
    main()