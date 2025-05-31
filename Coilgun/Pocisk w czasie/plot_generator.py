# plot_generator.py
import matplotlib.pyplot as plt
import os

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

    ax2_2.plot(times, positions, 'm-', label='Położenie [mm]')
    ax2_2.set_ylabel('Położenie [mm]', color='magenta')
    ax2_2.tick_params(axis='y', labelcolor='magenta')

    ax2_3.spines['right'].set_position(('outward', 60))
    ax2_3.plot(times, accelerations, 'c-', label='Przyspieszenie [m/s^2]')
    ax2_3.set_ylabel('Przyspieszenie [m/s^2]', color='cyan')
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