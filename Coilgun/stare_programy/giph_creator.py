import imageio
import os
import re # Moduł do wyrażeń regularnych

def create_gif_from_bitmaps(output_gif_name, folder_path="./", fps=10):
    """
    Tworzy plik GIF z serii obrazów BMP.

    Args:
        output_gif_name (str): Nazwa pliku wyjściowego GIF (np. "coilgun_animacja.gif").
        folder_path (str): Ścieżka do folderu zawierającego pliki BMP.
        fps (int): Liczba klatek na sekundę dla GIF-a (wpływa na szybkość animacji).
    """
    images = []
    filepaths = []

    # Wzorzec do wyszukania plików BMP z numerem kroku
    # Zakładamy format nazwy: coilgun_wyniki_DD_MM_RR_HH_MM_XXXHz_pic_KROK.bmp
    # Gdzie KROK to liczba, np. _pic_0.bmp, _pic_1.bmp itd.
    pattern = re.compile(r".*_pic_(\d+)\.bmp$")

    for filename in os.listdir(folder_path):
        if filename.endswith(".bmp"):
            match = pattern.match(filename)
            if match:
                # Wyodrębnij numer kroku do sortowania
                step_number = int(match.group(1))
                filepaths.append((step_number, os.path.join(folder_path, filename)))

    # Sortuj pliki według numeru kroku, aby animacja była w odpowiedniej kolejności
    filepaths.sort(key=lambda x: x[0])

    # Wczytaj obrazy
    for _, filepath in filepaths:
        images.append(imageio.imread(filepath))

    # Zapisz jako GIF
    imageio.mimsave(output_gif_name, images, fps=fps)
    print(f"GIF '{output_gif_name}' został utworzony.")

if __name__ == "__main__":
    # Przykład użycia:
    # Upewnij się, że output_gif_name pasuje do nazwy plików bmp, które generujesz
    # np. jeśli w oryginalnym skrypcie masz file_name="coilgun_wyniki_...", to tutaj też użyj tego.
    # Upewnij się, że folder_path jest prawidłowy (domyślnie './' czyli bieżący folder)
    
    # Przykładowe użycie, dostosuj `output_gif_name` i `folder_path` do swoich potrzeb
    # Nazwa pliku GIF powinna być unikalna i nie kolidować z nazwami Twoich bitmap.
    
    # Zakładając, że Twój skrypt FEMM generował pliki np. "coilgun_wyniki_27_05_25_12_30_100Hz_pic_0.bmp" itd.
    # Warto, aby nazwa GIF-a zawierała też pewne informacje, ale była prosta.
    
    # Możesz przekazać konkretną nazwę, np. bazując na tym, co było w skrypcie FEMM:
    # W oryginalnym kodzie file_name="coilgun_wyniki_" .. date("%d_%m_%y_%H_%M") .. "_" .. fn .. "Hz";
    # Musisz wiedzieć, jaka data i fn zostały użyte w ostatniej symulacji, aby stworzyć spójną nazwę.
    
    # Prostszym sposobem jest zdefiniowanie stałej nazwy dla GIF-a:
    create_gif_from_bitmaps("animacja_coilgun.gif", folder_path="./", fps=10)
    
    # Jeśli masz konkretną nazwę pliku z symulacji (np. z datetime):
    # current_time_str = datetime.datetime.now().strftime("%d_%m_%y_%H_%M") # Musi być ta sama co w symulacji
    # fn_sim = 100 # Musi być ta sama co w symulacji
    # base_file_name_sim = f"coilgun_wyniki_{current_time_str}_{fn_sim}Hz"
    # create_gif_from_bitmaps(f"{base_file_name_sim}_animacja.gif", folder_path="./", fps=10)