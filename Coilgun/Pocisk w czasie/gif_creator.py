# gif_creator.py
import imageio
import os
import re

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