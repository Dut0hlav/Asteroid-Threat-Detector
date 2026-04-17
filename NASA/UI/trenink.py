import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
import joblib
import os


aktualni_slozka = os.path.dirname(os.path.abspath(__file__))
cesta_csv = os.path.join(aktualni_slozka, 'data.csv')

df = pd.read_csv(cesta_csv).dropna()

parametry = ['absolutni_magnituda', 'prumer_max_metry', 'rychlost_km_h', 'vzdalenost_minuti_km', 'je_sentry_objekt']
X = df[parametry]
y = df['je_nebezpecny'].astype(int)

#škálování dat
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#trenovani dat
sit_A = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=1)
sit_B = MLPClassifier(hidden_layer_sizes=(30, 30, 30), max_iter=1000, random_state=2)
sit_C = MLPClassifier(hidden_layer_sizes=(64, 32, 16), max_iter=1000, random_state=3)

hlasovaci_model = VotingClassifier(
    estimators=[('A', sit_A), ('B', sit_B), ('C', sit_C)],
    voting='soft'
)
hlasovaci_model.fit(X_scaled, y)

#ukládání modelu
joblib.dump(hlasovaci_model, os.path.join(aktualni_slozka, 'hlasovaci_model_asteroidy.pkl'))
joblib.dump(scaler, os.path.join(aktualni_slozka, 'skalovac_asteroidy.pkl'))
print("uloženo")