# analysis_and_plotting.py
import matplotlib.pyplot as plt
import os
import datetime

def save_results_to_txt(results, output_dir="results"):
    """
    Zapisuje wyniki symulacji do plików tekstowych.

    Args:
        results (dict): Słownik wyników z run_multiple_simulations.
        output_dir (str): Katalog wyjściowy dla wyników.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    current_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for material, data in results.items():
        # Usuń znaki problematyczne z nazwy materiału dla nazwy pliku
        safe_material_name = material.replace(", ", "_").replace(" ", "_")
        filename = os.path.join(output_dir, f"force_vs_position_{safe_material_name}_{current_time_str}.txt")
        with open(filename, "w") as f:
            f.write("Położenie H0_el [mm]\tSiła [N]\n")
            for h0, force in data:
                f.write(f"{h0}\t{force}\n")
        print(f"Wyniki dla {material} zapisano do: {filename}")

def plot_results(results, output_dir="results"):
    """
    Generuje i zapisuje wykresy siły w zależności od położenia.

    Args:
        results (dict): Słownik wyników z run_multiple_simulations.
        output_dir (str): Katalog wyjściowy dla wykresów.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    current_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    plt.figure(figsize=(10, 6))
    for material, data in results.items():
        h0_values = [d[0] for d in data]
        force_values = [d[1] for d in data]
        plt.plot(h0_values, force_values, marker='o', linestyle='-', label=f'Materiał: {material}')

    plt.xlabel('Położenie środka rzutki H0_el [mm]')
    plt.ylabel('Siła [N]')
    plt.title('Siła oddziaływania na rzutkę w zależności od położenia')
    plt.grid(True)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8) # Linia dla 0 N
    plt.legend()
    plt.tight_layout()
    
    plot_filename = os.path.join(output_dir, f"force_vs_position_plot_{current_time_str}.png")
    plt.savefig(plot_filename)
    print(f"Wykres zapisano do: {plot_filename}")
    plt.show()