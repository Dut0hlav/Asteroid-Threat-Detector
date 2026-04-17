import customtkinter as ctk
import joblib
import pandas as pd
import math
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AsteroidApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Asteroid Threat Detector")
        self.geometry("450x750")

        aktualni_slozka = os.path.dirname(os.path.abspath(__file__))
        cesta_model = os.path.join(aktualni_slozka, 'hlasovaci_model_asteroidy.pkl')
        cesta_scaler = os.path.join(aktualni_slozka, 'skalovac_asteroidy.pkl')

        self.modely_nacteny = False
        try:
            self.model = joblib.load(cesta_model)
            self.scaler = joblib.load(cesta_scaler)
            self.modely_nacteny = True
        except FileNotFoundError:
            pass

        self.label_hlavni = ctk.CTkLabel(self, text="Vesmírný Detektor", font=("Arial", 24, "bold"))
        self.label_hlavni.pack(pady=20)

        self.entry_mag = self.vytvor_vstup("Absolutní magnituda (zářivost):", "např. 21.5")
        self.entry_dia = self.vytvor_vstup("Max. průměr (metry):", "např. 150")
        self.entry_vel = self.vytvor_vstup("Rychlost (km/h):", "např. 60000")
        self.entry_dst = self.vytvor_vstup("Vzdálenost minutí (km):", "např. 1000000")
        
        self.sentry_var = ctk.BooleanVar()
        self.check_sentry = ctk.CTkCheckBox(self, text="Je na seznamu sledovaných (Sentry)", variable=self.sentry_var)
        self.check_sentry.pack(pady=10)

        self.btn_analyzovat = ctk.CTkButton(self, text="SPUSTIT ANALÝZU", command=self.proved_analyzu, height=40)
        self.btn_analyzovat.pack(pady=15)

        self.result_box = ctk.CTkTextbox(self, width=380, height=220, font=("Consolas", 14))
        self.result_box.pack(pady=10)
        
        if not self.modely_nacteny:
            self.result_box.insert("1.0", "POZOR: Chybí umělá inteligence (.pkl)!\nMusíte spustit trenink.py.")

    def vytvor_vstup(self, text, placeholder):
        label = ctk.CTkLabel(self, text=text)
        label.pack(pady=(5, 0))
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=200)
        entry.pack(pady=(0, 5))
        return entry

    def spocitej_destrukci(self, prumer, rychlost):
        polomer = prumer / 2
        objem = (4/3) * math.pi * (polomer ** 3)
        hmotnost = objem * 3000
        rychlost_ms = rychlost / 3.6
        energie = 0.5 * hmotnost * (rychlost_ms ** 2)
        megatuny = energie / (4.184 * (10 ** 15))
        radius = 1.1 * (megatuny ** (1/3))
        return megatuny, radius

    def proved_analyzu(self):
        self.result_box.delete("1.0", "end")
        
        if not self.modely_nacteny:
            self.result_box.insert("1.0", "CHYBA: Není načtený model!")
            return

        try:
            m = float(self.entry_mag.get())
            d = float(self.entry_dia.get())
            v = float(self.entry_vel.get())
            dist = float(self.entry_dst.get())
            s = 1 if self.sentry_var.get() else 0

            vstupni_data = pd.DataFrame([[m, d, v, dist, s]], 
                                        columns=['absolutni_magnituda', 'prumer_max_metry', 
                                                 'rychlost_km_h', 'vzdalenost_minuti_km', 'je_sentry_objekt'])
            
            vstup_scaled = self.scaler.transform(vstupni_data)

            predikce = self.model.predict(vstup_scaled)[0]
            pravdepodobnost = self.model.predict_proba(vstup_scaled)[0][1]

            mt, rad = self.spocitej_destrukci(d, v)

            status = "NEBEZPEČNÝ!" if predikce == 1 else "BEZPEČNÝ"
            
            vypis = f"=== VÝSLEDEK AI ANALÝZY ===\n"
            vypis += f"Klasifikace: {status}\n"
            vypis += f"Jistota modelu: {pravdepodobnost*100:.1f} %\n\n"
            vypis += f"=== FYZIKÁLNÍ DOPAD ===\n"
            vypis += f"Síla exploze: {mt:.2f} Megatun TNT\n"
            vypis += f"Zóna totální zkázy: {rad:.2f} km\n"
            
            self.result_box.insert("1.0", vypis)

        except ValueError:
            self.result_box.insert("1.0", "CHYBA: Do políček zadávejte pouze čísla!")

if __name__ == "__main__":
    app = AsteroidApp()
    app.mainloop()