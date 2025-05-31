import femm as f

def draw_rectangle(center_x, center_y, width, height, group_id=0):
    """
    Rysuje prostokąt w FEMM, podając jego środek, szerokość, wysokość i opcjonalnie group_id.
    Wszystkie węzły tworzące prostokąt zostaną przypisane do podanej grupy.

    Args:
        center_x (float): Współrzędna x środka prostokąta.
        center_y (float): Współrzędna y środka prostokąta.
        width (float): Szerokość prostokąta (w kierunku X/R).
        height (float): Wysokość prostokąta (w kierunku Y/Z).
        group_id (int, optional): Numer grupy, do której zostaną przypisane węzły prostokąta. Domyślnie 0.

    Returns:
        list: Lista krotek (x, y) reprezentujących narożniki prostokąta w kolejności (lewy_dolny, prawy_dolny, prawy_górny, lewy_górny).
    """
    half_width = width / 2
    half_height = height / 2

    # Oblicz współrzędne narożników
    x1 = center_x - half_width
    y1 = center_y - half_height
    x2 = center_x + half_width
    y2 = center_y + half_height

    # Dodaj węzły
    f.mi_addnode(x1, y1)
    f.mi_addnode(x2, y1)
    f.mi_addnode(x2, y2)
    f.mi_addnode(x1, y2)

    # Zaznacz nowo dodane węzły i przypisz im grupę
    f.mi_selectnode(x1, y1)
    f.mi_selectnode(x2, y1)
    f.mi_selectnode(x2, y2)
    f.mi_selectnode(x1, y2)
    
    f.mi_setnodeprop("", group_id) # Ustawienie tylko group_id
    f.mi_clearselected() # Wyczyść zaznaczenie po przypisaniu właściwości

    # Rysuj linie łączące węzły
    f.mi_drawline(x1, y1, x2, y1)
    f.mi_drawline(x2, y1, x2, y2)
    f.mi_drawline(x2, y2, x1, y2)
    f.mi_drawline(x1, y2, x1, y1)
    
    return None

# --- Pozostałe funkcje z poprzedniego kodu, zmodyfikowane do użycia group_id ---

def create_coilgun_geometry(r_tube, R_coil, H_coil, R_el, H_el, H0_el, R_BC, I_current, N_wire, freq, mat="Aluminium, 1100"):
    """
    Tworzy projekt geometrii w FEMM dla coilguna na podstawie podanych wymiarów,
    wykorzystując funkcję draw_rectangle z opcjonalną grupą dla węzłów.

    Args:
        r_tube (float): Promień wewnętrzny cewki (tuby), [mm].
        R_coil (float): Promień zewnętrzny cewki, [mm].
        H_coil (float): Wysokość cewki, [mm].
        R_el (float): Promień pocisku (elementu), [mm].
        H_el (float): Wysokość pocisku (elementu), [mm].
        H0_el (float): Położenie środka pocisku w osi Z, [mm].
        N_turns (int): Całkowita liczba zwojów cewki.
        R_BC (float): Promień zewnętrznej granicy (boundary condition), [mm].
        I_current (float): Prąd w cewce, [A].
        freq (float): Częstotliwość problemu (dla magnetostatyki zazwyczaj 0), [Hz].
    """
    f.openfemm()
    f.newdocument(0)

    f.mi_probdef(freq, "millimeters", "axi", 1e-8)

    mu = 7000

    f.mi_getmaterial("Air")
    f.mi_getmaterial("Copper")
    f.mi_getmaterial("Aluminum, 1100") # Dodane, jeśli nie było
    f.mi_addmaterial("Ideal_Iron", mu, mu,0,0,0,10e6)
    # (’matname’, mu x, mu y, H c, J, Cduct, Lam d, Phi hmax, lam fill,      
    # LamType, Phi hx, Phi hy, nstr, dwire

    f.mi_addcircprop("Coil", I_current, 1)

    # --- Rysowanie Geometrii Cewki ---
    coil_center_r = (r_tube + R_coil) / 2
    coil_center_z = 0
    coil_width = R_coil - r_tube
    coil_height = H_coil
    
    # Cewka nie potrzebuje specjalnej grupy węzłów, więc group_id=0 (domyślny)
    draw_rectangle(coil_center_r, coil_center_z, coil_width, coil_height, group_id=0)

    f.mi_addblocklabel(coil_center_r, coil_center_z)
    f.mi_selectlabel(coil_center_r, coil_center_z)
    f.mi_setblockprop("Copper", 0, 0, "Coil", 0, 0, N_wire)
    f.mi_clearselected()

    # --- Rysowanie Geometrii Pocisku ---
    element_center_r = R_el / 2
    element_center_z = H0_el
    element_width = R_el
    element_height = H_el
    
    draw_rectangle(element_center_r, element_center_z, element_width, element_height, group_id=5) # Pocisk potrzebuje group_id = 5 dla węzłów i bloku

    f.mi_addblocklabel(element_center_r, element_center_z)
    f.mi_selectlabel(element_center_r, element_center_z)
    f.mi_setblockprop(mat, 1, 0, "", 0, 5)
    f.mi_clearselected()

    # --- Rysowanie Geometrii Powietrza (obszar analizy) ---
    air_center = coil_center_z

    f.mi_addnode(air_center, R_BC)
    f.mi_addnode(air_center, -R_BC)
    f.mi_drawline(air_center,-R_BC,air_center,R_BC)
    f.mi_drawarc(air_center,-R_BC,air_center,R_BC,180,1)

    f.mi_addblocklabel(R_BC/2, air_center)
    f.mi_selectlabel(R_BC/2, air_center)
    f.mi_setblockprop("Air", 1, 0, "", 0, 0)
    f.mi_clearselected()

    # --- Definicja warunków brzegowych ---
    f.mi_addboundprop("Mixed", 0, 0, 0, 0, 0, 0, 1/(4*3.141593*1e-7*R_BC*1e-3), 0, 2)
    
    f.mi_selectarcsegment(R_BC, coil_center_z)
    
    f.mi_setarcsegmentprop(1,"Mixed", 0, 0)
    f.mi_clearselected()

    # --- Zapis Pliku ---
    f.mi_saveas("coilgun1.fem")
    f.mi_close()

# --- Przykładowe użycie funkcji do generowania geometrii ---
if __name__ == "__main__":
    r_tube_val = 35/2
    R_coil_val = r_tube_val + 26.25
    H_coil_val = 115

    R_el_val = 30/2
    H_el_val = 45
    H0_el_val = -690/8

    R_BC_val = 3*H_coil_val
    I_current_val = 800
    freq_val = 50
    Nwire = 350

    create_coilgun_geometry(r_tube_val, R_coil_val, H_coil_val, 
                            R_el_val, H_el_val, H0_el_val, 
                            R_BC_val, I_current_val, Nwire, freq_val)

    print("\nPlik 'coilgun1.fem' został utworzony z użyciem funkcji draw_rectangle.")
    print("Otwórz go w FEMM, aby zweryfikować geometrię i grupy węzłów.")