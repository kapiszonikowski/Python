showconsole();

mydir="./";
file="Skin_blank.fem";
open(mydir .. "Skin_blank.fem") -- podać nazwę własnego projektu
mi_saveas(mydir .. "skin_temp.fem")

--Parametry edytowalne
faz=0; -- [] parametr sterujacy modelem (0 - model jednego drutu, 1 - model trojfazowy)

R=3; -- [mm] promien preta
Im=141; -- [A] prad (wartosc szczytowa)
f=5000; --[Hz] częstotliwosc pradu
d=8; -- [mm] odleglosc miedzy srodkami pretow w modelu trojfazowym
phi=0; -- [deg] dodatkowy poczatkowy kat fazowy wymuszenia pradowego

pi = 3.141593;

mi_getmaterial('Air');  -- pobranie materialow z biblioteki
mi_getmaterial('Copper');             
mi_getmaterial('Aluminum, 6061-T6');  
mi_getmaterial('Aluminum, 1100');     

mi_addboundprop('open',0,0,0,0,0,0,1/(4*pi*1E-7)/(10*(3*R+d)),0,2);  -- utworzenie warunkow brzegowych otwartych
-------------------------------------------------------------------------------
mi_probdef(f,'millimeters','planar',1E-8,0,30,1);   -- definicja parametrow w zakladce problem

I1=Im*cos(phi*pi/180)+I*Im*sin(phi*pi/180);     -- wyznaczenie wartosci pradow w pretach (zespolonych)
I2=Im*cos(phi*pi/180+2/3*pi)+I*Im*sin(phi*pi/180+2/3*pi);
I3=Im*cos(phi*pi/180-2/3*pi)+I*Im*sin(phi*pi/180-2/3*pi);

-------------------------------------------------------------------------------
mi_addcircprop('I1', I1, 1);    -- utworzenie nowych obwodow 'circuit'
mi_addcircprop('I2', I2, 1);
mi_addcircprop('I3', I3, 1);
-------------------------------------------------------------------------------
-- RYSOWANIE MODELU
-------------------------------------------------------------------------------
mi_clearselected();
mi_addnode(0,10*(3*R+d)); -- rysowanie warunkow brzegowych
mi_addnode(0,-10*(3*R+d));
mi_addarc(0,10*(3*R+d),0,-10*(3*R+d),180,1);
mi_addarc(0,-10*(3*R+d),0,10*(3*R+d),180,1);
mi_selectarcsegment(10*(3*R+d),0);
mi_selectarcsegment(-10*(3*R+d),0);
mi_setarcsegmentprop(1,'open',0,0);
mi_clearselected();
mi_addblocklabel(0,(10-1)*(3*R+d));
mi_selectlabel(0,(10-1)*(3*R+d));
mi_setblockprop('Air',1,0,'<None>',0,0,0);
mi_clearselected();

mi_addnode(0,R); -- rysowanie przekroju preta srodkowego
mi_addnode(0,-R);
mi_addnode(R,0);
mi_addnode(-R,0);
mi_addarc(0,R,0,-R,180,1);
mi_addarc(0,-R,0,R,180,1);
mi_addblocklabel(0,0);
mi_selectlabel(0,0);
mi_setblockprop('Copper',1,0,'I1',0,0,0);   -- nalezy wybrac odpowiedni material
if(faz==1) then
    mi_setblockprop('Copper',1,0,'I2',0,0,0);   -- nalezy wybrac odpowiedni material
    end
mi_clearselected();

if(faz==1) then
    mi_addnode(-d,R); -- rysowanie przekroju preta z lewej
    mi_addnode(-d,-R);
    mi_addarc(-d,R,-d,-R,180,1);
    mi_addarc(-d,-R,-d,R,180,1);
    mi_addblocklabel(-d,0);
    mi_selectlabel(-d,0);
    mi_setblockprop('Copper',1,0,'I1',0,0,0);   -- nalezy wybrac odpowiedni material
    mi_clearselected();
    end
if(faz==1) then
    mi_addnode(d,R); -- rysowanie przekroju preta z prawej
    mi_addnode(d,-R);
    mi_addarc(d,R,d,-R,180,1);
    mi_addarc(d,-R,d,R,180,1);
    mi_addblocklabel(d,0);
    mi_selectlabel(d,0);
    mi_setblockprop('Copper',1,0,'I3',0,0,0);   -- nalezy wybrac odpowiedni material
    mi_clearselected();
    end

mi_analyze(0);  -- uruchomienie obliczen (siatka generuje sie automatycznie)
mi_loadsolution();  -- wczytanie wynikow w postprocesorze