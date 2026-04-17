DOKUMENTACE PROJEKTU: Systém pro analýzu a predikci nebezpečných asteroidů (ATA)
1. Účel a reálné využití softwaru

Aplikace "Asteroid Threat Analyst" (ATA) slouží k predikci rizikovosti blízkozemních objektů (NEO - Near Earth Objects). Aplikace má reálné využití v oblasti planetární obrany a astronomické osvěty. Na základě pěti klíčových fyzikálních a astronomických parametrů dokáže klasifikovat, zda objekt představuje potenciální hrozbu pro Zemi (Potentially Hazardous Asteroid). Součástí softwaru je i fyzikální nadstavba, která na základě zadaných parametrů v reálném čase počítá odhadovanou kinetickou energii dopadu (v Megatunách TNT) a poloměr zóny totální zkázy.
2. Původ dat a jejich získávání (Vlastní sběr)

V projektu není použit žádný předzpracovaný dataset z platforem jako Kaggle apod.
Data si aplikace sbírá zcela autonomně pomocí vlastního skriptu (Data Crawler/API Fetcher), který komunikuje s oficiálním REST API americké vesmírné agentury NASA (rozhraní NeoWs - Near Earth Object Web Service).

    Skript se v cyklech dotazuje serverů NASA na historická data o průletech asteroidů.

    Výsledkem je lokálně vygenerovaný soubor nasbirana_data.csv, který obsahuje více než 1500 unikátních záznamů.

3. Struktura dat a předzpracování

Každý záznam v datasetu obsahuje 5 nezávislých atributů (features) a 1 závislou proměnnou (target):

    absolutni_magnituda (zářivost objektu, koreluje s hmotností)

    prumer_max_metry (odhadovaný maximální průměr tělesa)

    rychlost_km_h (relativní rychlost vůči Zemi)

    vzdalenost_minuti_km (jak daleko objekt Zemi mine)

    je_sentry_objekt (boolean - zda je na sledovacím seznamu rizikových těles Sentry)

    Cíl (Target): je_nebezpecny (boolean klasifikace)

Proces předzpracování (Data Preprocessing):

    Čištění dat (Data Cleaning): Z odstranění neúplných záznamů, které API vrátilo s chybějícími hodnotami (pomocí funkce dropna()).

    Transformace: Převod textových/boolean hodnot na numerické (0 a 1) pro kompatibilitu s ML algoritmy.

    Škálování (Scaling): Protože data mají diametrálně odlišné řády (rychlosti ve statisících vs. magnituda v desítkách), je na vstupní data aplikován StandardScaler (Z-score normalizace). Tento škálovač je serializován (skalovac_asteroidy.pkl) pro transformaci budoucích uživatelských vstupů.

4. Model strojového učení

Projekt nevyužívá pouze jeden model, ale pokročilou architekturu tzv. Ansámblového učení (Ensemble Learning). Jde o klasifikační model vytvořený pomocí knihovny scikit-learn.

    Jádrem je VotingClassifier, který sdružuje tři umělé neuronové sítě (MLPClassifier), každou s odlišnou topologií skrytých vrstev (široká, hluboká a trychtýřová).

    Sítě hlasují o konečném výsledku (tzv. "soft voting" na základě pravděpodobností).

    Dokumentace tréninku a testování: Kompletní analytický postup, včetně rozdělení na trénovací/testovací sadu (80/20), evaluace metrik a vykreslení grafů (Loss curve, Confusion Matrix, Heatmapa) je zdokumentován a doložen v přiloženém souboru Muj_Colab_Postup.ipynb.

    Finální produkční model je po natrénování uložen do souboru hlasovaci_model_asteroidy.pkl.

5. Architektura projektu a oddělení kódu

Projekt striktně dodržuje požadavky na oddělení vlastního a převzatého/pomocného kódu. Složková struktura:

    Složka /UI: Zde se nachází autorský kód uživatelského rozhraní (Aplikace.py), finální aplikace a lokální skript pro vygenerování produkčního modelu z nasbíraných dat (trenink.py).

    Složka /vendor: Zde je umístěn pomocný kód třetí strany / API rozhraní (nasa_downloader.py), který zajišťuje stažení surových dat z internetu. Vlastní analytická a ML část je na něm nezávislá.

6. Návod k nasazení (Deployment bez IDE)

Aplikace je navržena pro spuštění na jakémkoliv školním PC s OS Windows a nainstalovaným základním interpretem jazyka Python, a to zcela bez nutnosti vývojového prostředí (IDE) nebo administrátorských práv.

Postup nasazení:

    Překopírujte celou složku projektu (NASA_Projekt) na libovolné místo v PC (Plocha, Flash disk).

    Dvakrát klikněte na dávkový soubor SPUSTIT_PROJEKT.bat.

    Tento soubor automaticky (na pozadí):

        Vytvoří izolované virtuální prostředí (venv), čímž obchází nutnost administrátorských práv na školním PC.

        Nainstaluje všechny potřebné knihovny ze souboru requirements.txt.

        Spustí grafické uživatelské rozhraní aplikace.

7. Uživatelský manuál (Základní funkce)

    Po spuštění aplikace se zobrazí formulář.

    Uživatel do textových polí zadá parametry zaznamenaného tělesa. Lze využít tyto vzorové parametry masivního a nebezpečného asteroidu:

        Absolutní magnituda: 18.5

        Max průměr (m): 1000

        Rychlost (km/h): 85000

        Vzdálenost (km): 500000

        Sentry objekt: Zaškrtnuto

    Stiskněte tlačítko SPUSTIT ANALÝZU.

    Následně proběhne transformace vstupů (Scaler), inference umělou inteligencí (Model) a fyzikální kalkulace. Výsledek se zobrazí v textovém terminálu ve spodní části okna. Aplikaci lze používat opakovaně bez nutnosti restartu.
