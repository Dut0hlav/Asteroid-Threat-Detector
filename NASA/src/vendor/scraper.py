import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os


API_KEY = 'xGj0Ke6bhb4BqE9m62bOfspj6U8uySiuSUPoiHsF'
BASE_URL = 'https://api.nasa.gov/neo/rest/v1/feed'

def ziskej_data_o_asteroidech(pocet_pozadovanych_zaznamu=1600):
    """
    Funkce stahuje data z NASA API týden po týdnu, dokud nenasbírá požadovaný počet záznamů.
    """
    seznam_asteroidu = []
    
    konecne_datum = datetime.today()
    pocet_stazenych = 0
    
    print(f"Začínám stahovat data o asteroidech z NASA API...")

    while pocet_stazenych < pocet_pozadovanych_zaznamu:
        pocatecni_datum = konecne_datum - timedelta(days=7)
        
        start_str = pocatecni_datum.strftime('%Y-%m-%d')
        end_str = konecne_datum.strftime('%Y-%m-%d')
        
        print(f"Stahuji období: {start_str} až {end_str}")
        
        url = f"{BASE_URL}?start_date={start_str}&end_date={end_str}&api_key={API_KEY}"
        
        try:
            odpoved = requests.get(url)
            data = odpoved.json()
            
            if odpoved.status_code != 200:
                print(f"Chyba API: {data.get('error', odpoved.text)}")
                break
            
            objekty_podle_dnu = data.get('near_earth_objects', {})
            
            for den, asteroidy in objekty_podle_dnu.items():
                for ast in asteroidy:
                    try:
                        zaznam = {
                            'id': ast['id'],
                            'nazev': ast['name'],
                            'absolutni_magnituda': ast['absolute_magnitude_h'],
                            'prumer_max_metry': ast['estimated_diameter']['meters']['estimated_diameter_max'],
                            'rychlost_km_h': ast['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                            'vzdalenost_minuti_km': ast['close_approach_data'][0]['miss_distance']['kilometers'],
                            'je_sentry_objekt': ast['is_sentry_object'],
                            'je_nebezpecny': ast['is_potentially_hazardous_asteroid']
                        }
                        seznam_asteroidu.append(zaznam)
                        pocet_stazenych += 1
                        
                    except (KeyError, IndexError):
                        continue
            
            print(f"Zatím staženo záznamů: {pocet_stazenych}")
            
            konecne_datum = pocatecni_datum - timedelta(days=1)
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Došlo k chybě při stahování: {e}")
            break

    df = pd.DataFrame(seznam_asteroidu)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    cesta_k_souboru = 'data/nasbirana_data.csv'
    df.to_csv(cesta_k_souboru, index=False)
    print(f"\nHOTOVO! Staženo {len(df)} záznamů. Uloženo do: {cesta_k_souboru}")

if __name__ == '__main__':
    ziskej_data_o_asteroidech(pocet_pozadovanych_zaznamu=1600)