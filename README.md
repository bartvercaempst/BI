# Satellietkaart Bedieningen & Moederbundels (West-Vlaanderen)

Interactieve satellietkaart en inventaris van alle 40 private aansluitingen / terminals en 9 Infrabel rangeerbundels (moederbundels) in West-Vlaanderen.

Ontwikkeld om de creatie en het up-to-date houden van **Bedieningsinstructies (BI's)** voor machinisten en rangeerders te stroomlijnen op basis van de Infrabel **Plaatselijke Protocollen voor het gebruik van de infrastructuur (PPGI's)**.

---

## 🌟 Functionaliteiten

- 🛰️ **Hoge Resolutie Satellietbeelden**: ESRI World Imagery toont exacte terminalsporen, havenbekkens, laadkaaien en rangeerterreinen.
- 🚆 **OpenRailwayMap Spoorlaag**: Schakelbare overlay met de officiële Infrabel spoorlijnen, wissels en seinstructuren.
- 🏷️ **Labels & Tags**: Alle bedrijfsnamen en rangeerbundels direct zichtbaar op de satellietkaart.
- 🟢 **BI-Status Inzicht**:
  - **14 Reeds een BI**: Gemarkeerd met groene checkmarks en versienummers.
  - **26 Nog GEEN BI**: Gemarkeerd met rode attentie-markers.
  - **9 Moederbundels**: Infrabel vormingsstations en wisselbundels.
- 🎯 **Interactieve GPS-Coördinaten Correctie**:
  - Versleep pins direct op de satellietfoto of klik op de kaart.
  - Wijzigingen worden automatisch lokaal bewaard (`localStorage`).
  - Eén-klik export naar `locs_gps.json` of complete bijgewerkte HTML.

---

## 🚀 Lokaal Gebruiken

1. **Direct in de browser openen**:
   - Dubbelklik op `index.html` (of `kaart_bedieningen.html`) om de kaart direct in Microsoft Edge of Google Chrome te bekijken.
2. **Optioneel met lokale Python synchronisatieserver**:
   ```bash
   python server.py
   ```
   Open `http://localhost:8055/` in je browser. Elke aanpassing van coördinaten via de kaart wordt direct weggeschreven naar `locs_gps.json` en de HTML-bestanden.

---

## 🌐 Publiceren op GitHub Pages

Deze repository is geconfigureerd met `index.html` in de hoofdmap.

1. Maak een repository aan op [GitHub](https://github.com/new).
2. Voer de volgende commando's uit in deze map:
   ```bash
   git init
   git add .
   git commit -m "Eerste versie interactieve satellietkaart DB Cargo"
   git branch -M main
   git remote add origin https://github.com/<GEBRUIKERSNAAM>/<REPO-NAAM>.git
   git push -u origin main
   ```
3. Ga in GitHub naar **Settings** > **Pages** en stel de bron in op **Deploy from a branch** (`main` / root `/`).
4. Binnen 1 minuut is je kaart live bereikbaar via:
   `https://<GEBRUIKERSNAAM>.github.io/<REPO-NAAM>/`
