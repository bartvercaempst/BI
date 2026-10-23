"""
Hierarchical Source Data Model & PPGI Comparison Engine for BI Generator
Niveaus:
  Niveau 1: Bedrijf / Operator (DB Cargo Belgium)
  Niveau 2: Regio (West-Vlaanderen)
  Niveau 3: Zone / Hub (Zeebrugge, Brugge, Oostende, Kortrijk)
  Niveau 4: Deelzone / Moederbundel (Ramskapelle, Pelikaan, Zwankendamme, etc.)
  Niveau 5: Terminal / Private Aansluiting (CRO Brittaniadok, Wallenius Canadakaai, etc.)
"""

import os
import json

LEVEL_1_OPERATOR = {
    "id": "dbc_be",
    "naam": "DB Cargo Belgium",
    "logo_tekst": "DB Cargo",
    "autorisatie_functionaris": "Head of Cargo Management",
    "autorisatie_ingangsdatum": "Onmiddellijk",
    "goedkeuring_systeem": "Digitaal via Zenya",
    "doel": "Het beschrijven van een uniforme en veilige werkwijze voor bedieningen van private spooraansluitingen en bundels.",
    "gebruikersgroep": "Alle medewerkers buitendienst (Treinbestuurders & Rangeerders/Schouwers + omkadering + hulpondernemingen) die de bediening uitvoeren.",
    "contacten": [
        {"dienst": "NOC Shiftleader (Centraal Beheer)", "rol": "Real-time Operations 24/7", "telefoon": "+32 3 545 02 33"}
    ],
    "noodcontacten": [
        {"dienst": "Hulpdiensten (Calamiteiten)", "rol": "Algemeen noodnummer", "telefoon": "112"},
        {"dienst": "Brandweer", "rol": "Noodgeval", "telefoon": "112"},
        {"dienst": "Politie / Spoorwegpolitie", "rol": "Interventie", "telefoon": "101 of 112"},
        {"dienst": "Infrabel Rode Telefoon", "rol": "Noodcentrale Infrabel", "telefoon": "+32 2 525 91 40"},
        {"dienst": "Infrabel Oranje Telefoon", "rol": "RID Incidenten & Meldingen", "telefoon": "+32 2 528 81 50"}
    ],
    "algemene_veiligheidsregels": [
        "Persoonlijke beschermingsmiddelen (PBM): Fluohesje, veiligheidsschoenen S3, veiligheidsbril en werkhandschoenen zijn te allen tijde verplicht.",
        "Stormprotocol: Indien stormweer actief is of aangekondigd wordt, dient men rekening te houden met een minimum hellingswaarde van 6 ‰ voor het berekenen van de immobilisatiekracht. Alle voertuigen moeten onderling gekoppeld zijn.",
        "Kleine bewegingen: Alle bewegingen op aansluitingen en bundels gebeuren in 'kleine beweging' met maximale waakzaamheid.",
        "Wisselbediening: Steeds controleren van tongligging en vergrendeling van handwissels vóór overschrijding."
    ]
}

LEVEL_2_REGIO = {
    "west_vlaanderen": {
        "id": "west_vlaanderen",
        "naam": "West-Vlaanderen (Area North-West)",
        "infrabel_district": "Infrabel Operations Area North-West",
        "permanentie_ito": "+32 50 30 22 23",
        "traffic_officer_nw": "+32 9 241 28 68",
        "ssp_zone": "Zone Brugge / Kust / Kortrijk"
    }
}

LEVEL_3_ZONES = {
    "zeebrugge": {
        "id": "zeebrugge",
        "regio_id": "west_vlaanderen",
        "naam": "Haven Zeebrugge",
        "centraal_seinhuis": "Infrabel Blok 7 Zeebrugge",
        "local_dispatch": {"dienst": "NOC Dispatch Zeebrugge", "rol": "Lokale Rangeer Dispatcher", "telefoon": "+32 50 33 03 25"},
        "seinhuis_contacten": [
            {"dienst": "Traffic Controller (Blok 7)", "rol": "Trein- en rangeerdienst", "telefoon": "+32 50 30 25 11"},
            {"dienst": "Safety Controller (Blok 7)", "rol": "Veiligheid & Buitendienst", "telefoon": "+32 50 30 25 09"},
            {"dienst": "Safety Supervisor (Blok 7)", "rol": "Supervisie Zeebrugge", "telefoon": "+32 50 30 25 00"},
            {"dienst": "Traffic Officer (Blok 6)", "rol": "Bovenlokaal beheer Area NW", "telefoon": "+32 9 241 28 68"},
            {"dienst": "Mailbox Blok 7 Infrabel", "rol": "Schriftelijke overdrachten", "telefoon": "rdc.nw.blok7@infrabel.be"}
        ],
        "havenautoriteit": {
            "naam": "Havenkapiteinsdienst Port of Antwerp-Bruges",
            "telefoon": "+32 50 54 32 40",
            "vhf_kanalen": "VHF 71 (Havenoperaties) / VHF 74 (Sluis & Dokken)"
        },
        "zone_risicos": [
            "Transmigranten: Mogelijke aanwezigheid van transmigranten in het havengebied. Waakzaamheid bij stilstand en spoorpoorten.",
            "Havenverkeer: Intensief vrachtwagen- en terminalverkeer over spooroverwegen.",
            "Zeehavenwind: Verhoogde kans op zware windstoten; strikte controle van wielkeggen en handremmen."
        ],
        "zone_snelheden": {
            "havenlijnen": "Max 20 km/u op havenverbindingslijnen (L202, L202A, L202B)",
            "aansluitingen": "Max 10 km/u op private spooraansluitingen",
            "kaden": "Stapvoets (max 5 km/u) langs laadkaden en in loodsen"
        }
    },
    "brugge": {
        "id": "brugge",
        "regio_id": "west_vlaanderen",
        "naam": "Zone Brugge & Midden-WVL",
        "centraal_seinhuis": "Seinzaal Brugge (FR/B)",
        "local_dispatch": {"dienst": "NOC Dispatch Brugge / Kust", "rol": "Lokale Dispatcher", "telefoon": "+32 50 30 24 11"},
        "seinhuis_contacten": [
            {"dienst": "Traffic Controller Brugge (FR/B)", "rol": "Treindienst L50A / L51 / L66", "telefoon": "+32 50 30 24 11"},
            {"dienst": "Safety Controller Brugge", "rol": "Rangeerdienst & Spoorbezettingsbeheer", "telefoon": "+32 50 30 24 09"},
            {"dienst": "Traffic Officer Area NW", "rol": "Bovenlokaal beheer Area NW", "telefoon": "+32 9 241 28 68"},
            {"dienst": "Mailbox Seinzaal Brugge", "rol": "Schriftelijke overdrachten", "telefoon": "rdc.nw.brugge@infrabel.be"}
        ],
        "havenautoriteit": None,
        "zone_risicos": [
            "Druk reizigers- en goederenverkeer op hoofdlijnen L50A, L51 en L66.",
            "Handwisselbediening en spoorbezetting op verspreide industrieterreinen."
        ],
        "zone_snelheden": {
            "havenlijnen": "Max 20 km/u op bundelsporen",
            "aansluitingen": "Max 10 km/u op aansluitingen",
            "kaden": "Stapvoets"
        }
    },
    "oostende": {
        "id": "oostende",
        "regio_id": "west_vlaanderen",
        "naam": "Zone Oostende",
        "centraal_seinhuis": "Seinzaal Oostende (Blok 4)",
        "local_dispatch": {"dienst": "NOC Dispatch Oostende / Kust", "rol": "Lokale Dispatcher", "telefoon": "+32 59 56 24 11"},
        "seinhuis_contacten": [
            {"dienst": "Traffic Controller Oostende (Blok 4)", "rol": "Treinverkeer L50A Kust", "telefoon": "+32 59 56 24 11"},
            {"dienst": "Safety Controller Oostende", "rol": "Rangeer- en Bundeldienst", "telefoon": "+32 59 56 24 09"},
            {"dienst": "Traffic Officer Area NW", "rol": "Bovenlokaal beheer Area NW", "telefoon": "+32 9 241 28 68"},
            {"dienst": "Mailbox Seinzaal Oostende", "rol": "Schriftelijke overdrachten", "telefoon": "rdc.nw.oostende@infrabel.be"}
        ],
        "havenautoriteit": None,
        "zone_risicos": [
            "Kustwind en zoutafzetting op contactleiding en spoorinfrastructuur.",
            "Wegovergangen en havenbedieningen langs openbare wegen."
        ],
        "zone_snelheden": {
            "havenlijnen": "Max 20 km/u op bundelsporen",
            "aansluitingen": "Max 10 km/u op aansluitingen",
            "kaden": "Stapvoets"
        }
    },
    "kortrijk": {
        "id": "kortrijk",
        "regio_id": "west_vlaanderen",
        "naam": "Zone Kortrijk & Zuidwest-WVL",
        "centraal_seinhuis": "Seinzaal Kortrijk (FR/D)",
        "local_dispatch": {"dienst": "NOC Dispatch Kortrijk (Area Gent/Kortrijk)", "rol": "Lokale Dispatcher", "telefoon": "+32 56 24 24 11"},
        "seinhuis_contacten": [
            {"dienst": "Traffic Controller Kortrijk (FR/D)", "rol": "Treindienst L75 / L69", "telefoon": "+32 56 24 24 11"},
            {"dienst": "Safety Controller Kortrijk", "rol": "Rangeer- en Veiligheidsdienst", "telefoon": "+32 56 24 24 09"},
            {"dienst": "Traffic Officer Area NW", "rol": "Bovenlokaal beheer Area NW", "telefoon": "+32 9 241 28 68"},
            {"dienst": "Mailbox Seinzaal Kortrijk", "rol": "Schriftelijke overdrachten", "telefoon": "rdc.nw.kortrijk@infrabel.be"}
        ],
        "havenautoriteit": None,
        "zone_risicos": [
            "Grensregio verkeer L75 & exploitatie enkelsporig baanvak L69.",
            "Verhoogde waakzaamheid bij handwissels en stootblokken op goederensporen.",
            "Overwegen op enkelsporige baanvakken zonder automatische aankondiging bij rangeren."
        ],
        "zone_snelheden": {
            "havenlijnen": "Max 20 km/u op bundelsporen",
            "aansluitingen": "Max 10 km/u op aansluitingen",
            "kaden": "Stapvoets"
        }
    }
}

LEVEL_4_MOEDERBUNDELS = {
    "ramskapelle": {
        "id": "ramskapelle",
        "zone_id": "zeebrugge",
        "naam": "Bundel Ramskapelle",
        "ppgi_referentie": "PP-321-Brugge (Actiezone Zeebrugge Zuidelijk Insteekdok, Versie 37.0 - 17/10/2025)",
        "ssp_referentie": "SSP Zone Brugge blz. 16 & 17",
        "beseind": True,
        "seinen_info": "Beseinde bundel uitgerust met grote stopseinen (o.a. ND-R.7) en rangeerpaaltjes.",
        "bovenleiding_info": "Hoofdzakelijk uitgerust met volledige bovenleiding. Spoor 844 (Lijn 202B) is maar gedeeltelijk uitgerust met bovenleiding (einde aangeduid met bord).",
        "tankinstallatie": "Spoorfuelinstallatie G&V op spoor 899 (beveiligd door ontspoortong 91AR).",
        "parkeergelegenheid": [
            "Aan de tankinstallatie G&V",
            "Aan de Alfred Ronsestraat",
            "Aan het voormalige kantoor van Lineas",
            "Langs de bundelsporen"
        ],
        "cameras": "24/7 camerabewaking beheerd door Infrabel.",
        "schuifrangering": "Toegelaten richting Brugge via spoor 880 (doodspoor) mits toelating van Blok 7.",
        "bundel_sporen": [
            {"spoor": "Sporen 881 t.e.m. 897", "type": "Beseinde bundelsporen", "beveiliging": "Seinen ND-R"},
            {"spoor": "Spoor 842 & 844", "type": "Verbindingssporen L202B", "beveiliging": "Seinen"},
            {"spoor": "Spoor 880", "type": "Doodspoor schuifrangering", "beveiliging": "Stootjuk"},
            {"spoor": "Spoor 899", "type": "G&V Spoorfuelinstallatie", "beveiliging": "Ontspoortong 91AR"},
            {"spoor": "Spoor 898", "type": "Los- en laadkaaien CdMZ", "beveiliging": "Stuitklamp"},
            {"spoor": "Spoor 843", "type": "Toegang Bundel Cast (Canadakaai)", "beveiliging": "Stuitklamp"},
            {"spoor": "Spoor 872", "type": "Toegang SA C-RO Brittaniadok", "beveiliging": "Stuitklamp 321 + Ontspoortong 10R"},
            {"spoor": "Spoor 879", "type": "Toegang Bundel Toyota", "beveiliging": "Elektrische stuitklamp"}
        ],
        "spooroverzicht": [
            {"spoor": "881", "bovenleiding": "Ja", "ltl": "660 m", "lol": "640 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "882", "bovenleiding": "Ja", "ltl": "660 m", "lol": "640 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "883", "bovenleiding": "Ja", "ltl": "719 m", "lol": "709 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "884", "bovenleiding": "Ja", "ltl": "719 m", "lol": "709 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "885", "bovenleiding": "Ja", "ltl": "724 m", "lol": "704 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "886", "bovenleiding": "Ja", "ltl": "724 m", "lol": "704 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "887", "bovenleiding": "Ja", "ltl": "724 m", "lol": "704 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Ontvangst & vertrek"},
            {"spoor": "888", "bovenleiding": "Ja", "ltl": "746 m", "lol": "726 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor • Maximale lengte"},
            {"spoor": "889", "bovenleiding": "Ja", "ltl": "463 m", "lol": "443 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "890", "bovenleiding": "Ja", "ltl": "425 m", "lol": "405 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "891", "bovenleiding": "Ja", "ltl": "466 m", "lol": "446 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "892", "bovenleiding": "Ja", "ltl": "477 m", "lol": "457 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "893", "bovenleiding": "Ja", "ltl": "442 m", "lol": "422 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "894", "bovenleiding": "Ja", "ltl": "469 m", "lol": "449 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "895", "bovenleiding": "Ja", "ltl": "519 m", "lol": "499 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort bundelspoor • Opstellen wagens"},
            {"spoor": "896", "bovenleiding": "Nee", "ltl": "164 m", "lol": "144 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Niet-geëlektrificeerd rangeerspoor"},
            {"spoor": "897", "bovenleiding": "Nee", "ltl": "255 m", "lol": "235 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Uitwijkspoor beschadigde wagens"},
            {"spoor": "880", "bovenleiding": "Ja", "ltl": "105 m", "lol": "85 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Doodspoor schuifrangering kant Brugge"},
            {"spoor": "842", "bovenleiding": "Nee", "ltl": "41 m", "lol": "21 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kort verbindingsspoor L202B"},
            {"spoor": "844", "bovenleiding": "Deels (55m)", "ltl": "897 m", "lol": "877 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Baanvakspoor L202B naar CRO (let op bovenleidingsgrens!)"},
            {"spoor": "899", "bovenleiding": "Nee", "ltl": "130 m", "lol": "110 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "G&V Spoorfuelinstallatie (ontspoortong 91AR)"}
        ],
        "overwegen_tracé": [
            {"naam": "Overweg 15", "lijn": "L202B", "type": "Automatische overweg", "beveiliging": "Ontspoortong 10R opwaarts"},
            {"naam": "Overweg 17 (Sas)", "lijn": "L202B", "type": "Manueel bediend via slotkast", "beveiliging": "Stuitklamp 321"}
        ]
    },
    "pelikaan": {
        "id": "pelikaan",
        "zone_id": "zeebrugge",
        "naam": "Bundel Pelikaan",
        "ppgi_referentie": "PP-321-Brugge (Actiezone Zeebrugge Zuidelijk Insteekdok, Versie 37.0 - 17/10/2025)",
        "ssp_referentie": "SSP Zone Brugge",
        "beseind": True,
        "seinen_info": "Beseinde bundel sporen 861 t.e.m. 871.",
        "bovenleiding_info": "Volledig uitgerust met bovenleiding.",
        "tankinstallatie": "Geen eigen tankinstallatie; gebruik tankspoor Ramskapelle.",
        "parkeergelegenheid": ["Parkeerzone Pelikaanstraat / Kaai 100-reeks"],
        "cameras": "Infrabel camerabewaking.",
        "schuifrangering": "Rangeerbewegingen via spoor 860 en 875 (doodsporen).",
        "bundel_sporen": [
            {"spoor": "Sporen 861 t.e.m. 871", "type": "Bundelsporen (verlengd v36.0)", "beveiliging": "Seinen"},
            {"spoor": "Spoor 860 & 875", "type": "Doodsporen", "beveiliging": "Stootjuk"},
            {"spoor": "Wissel 521", "type": "Aansluiting SA ICO 1", "beveiliging": "Stuitklamp"},
            {"spoor": "Wissel 502", "type": "Aansluiting SA ICO 2", "beveiliging": "Stuitklamp (koppelslot verplaatst v36.0)"},
            {"spoor": "Wissel 551 & 552", "type": "Aansluiting SA Efico & SA NDQ", "beveiliging": "Stuitklamp"}
        ],
        "spooroverzicht": [
            {"spoor": "861", "bovenleiding": "390m binnenland", "ltl": "980 m", "lol": "960 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Bundelspoor Pelikaan (lengte 960m)"},
            {"spoor": "862", "bovenleiding": "333m binnenland", "ltl": "822 m", "lol": "802 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Bundelspoor Pelikaan (lengte 802m)"},
            {"spoor": "863", "bovenleiding": "Ja", "ltl": "435 m", "lol": "415 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Bundelspoor Pelikaan"},
            {"spoor": "864", "bovenleiding": "Ja", "ltl": "502 m", "lol": "482 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Bundelspoor Pelikaan"},
            {"spoor": "865", "bovenleiding": "Ja", "ltl": "870 m", "lol": "850 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "866", "bovenleiding": "Ja", "ltl": "915 m", "lol": "895 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "867", "bovenleiding": "Ja", "ltl": "885 m", "lol": "865 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "868", "bovenleiding": "Ja", "ltl": "845 m", "lol": "825 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "869", "bovenleiding": "Ja", "ltl": "825 m", "lol": "805 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "870", "bovenleiding": "Ja", "ltl": "852 m", "lol": "832 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Verlengd bundelspoor v36.0"},
            {"spoor": "871", "bovenleiding": "Ja", "ltl": "500 m", "lol": "480 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Nee", "functie": "Bundelspoor Pelikaan"},
            {"spoor": "875", "bovenleiding": "Ja", "ltl": "883 m", "lol": "863 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "functie": "Doodspoor (toegang via wissel 521 linkerstand)"}
        ],
        "overwegen_tracé": []
    },
    "zwankendamme": {
        "id": "zwankendamme",
        "zone_id": "zeebrugge",
        "naam": "Bundel Zwankendamme",
        "ppgi_referentie": "PP-311-Brugge (Actiezone Zeebrugge, Deel 1)",
        "ssp_referentie": "SSP Zeebrugge",
        "beseind": True,
        "seinen_info": "Vormings- en vertrekbundel Zeebrugge.",
        "bovenleiding_info": "Volledig geëlektrificeerd.",
        "tankinstallatie": "Aanwezig in vorming.",
        "parkeergelegenheid": ["Loods Zwankendamme / Stationsomgeving"],
        "cameras": "Infrabel cameratoezicht.",
        "schuifrangering": "Uitgebreide heuvel- en rangeerinstallaties.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "521", "bovenleiding": "Ja", "ltl": "800 m", "lol": "780 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor Bundel A"},
            {"spoor": "522", "bovenleiding": "Ja", "ltl": "750 m", "lol": "730 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor Bundel A"},
            {"spoor": "523", "bovenleiding": "Ja", "ltl": "700 m", "lol": "680 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Lange bundelspoor Bundel A"},
            {"spoor": "524", "bovenleiding": "Ja", "ltl": "610 m", "lol": "590 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Omloop- & bedieningsspoor ECS 1 (BML)"},
            {"spoor": "525", "bovenleiding": "Nee", "ltl": "365 m", "lol": "345 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Doodspoor Bundel A"},
            {"spoor": "526", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Doodspoor Bundel A"},
            {"spoor": "527", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Doodspoor Bundel A"},
            {"spoor": "101-110", "bovenleiding": "Ja", "ltl": "680-740 m", "lol": "660-720 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Vormings- en vertreksporen Zwankendamme"},
            {"spoor": "135", "bovenleiding": "Nee", "ltl": "360 m", "lol": "340 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Sasspoor naar 2XL Blauwe Loods (ontspoortong 96G)"}
        ],
        "overwegen_tracé": []
    },
    "voorhaven_west": {
        "id": "voorhaven_west",
        "zone_id": "zeebrugge",
        "naam": "Bundel Voorhaven-West",
        "ppgi_referentie": "PP-311-Brugge (Actiezone Zeebrugge Voorhaven)",
        "ssp_referentie": "SSP Zeebrugge",
        "beseind": True,
        "seinen_info": "Seinen Voorhaven L202.",
        "bovenleiding_info": "Grotendeels geëlektrificeerd.",
        "tankinstallatie": "Geen.",
        "parkeergelegenheid": ["Kielbankstraat / Kustlaan"],
        "cameras": "Haven- en Infrabel camera's.",
        "schuifrangering": "Rangeerbewegingen via bundelhals.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "Dartline 1", "bovenleiding": "Nee", "ltl": "637 m", "lol": "617 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Opstel- en herstelspoor Dartline"},
            {"spoor": "Dartline 2", "bovenleiding": "Nee", "ltl": "632 m", "lol": "612 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Opstel- en herstelspoor Dartline"},
            {"spoor": "Dartline 3", "bovenleiding": "Nee", "ltl": "643 m", "lol": "623 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Opstel- en herstelspoor Dartline"},
            {"spoor": "Stora 1", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Plaatsingsspoor binnen in loods"},
            {"spoor": "Stora 2", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Uithaalspoor getrokken beweging"},
            {"spoor": "Bundel Voorhaven", "bovenleiding": "Deels", "ltl": "500-600 m", "lol": "480-580 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Kaaibedieningssporen Voorhaven L202"}
        ],
        "overwegen_tracé": []
    },
    "nid": {
        "id": "nid",
        "zone_id": "zeebrugge",
        "naam": "Bundel NID (Noordelijk Insteekdok)",
        "ppgi_referentie": "PP-311-Brugge (Actiezone Zeebrugge, Deel 1)",
        "ssp_referentie": "SSP Zeebrugge",
        "beseind": True,
        "seinen_info": "Beseinde bundel sporen 1 t.e.m. 5.",
        "bovenleiding_info": "Gedeeltelijke bovenleiding.",
        "tankinstallatie": "Geen.",
        "parkeergelegenheid": ["NID Kaaiweg"],
        "cameras": "Havenbewaking.",
        "schuifrangering": "Kleine beweging via Zwankendamme.",
        "bundel_sporen": [
            {"spoor": "Spoor 1", "type": "NID Spoor", "lengte": "354m"},
            {"spoor": "Spoor 2", "type": "NID Spoor", "lengte": "537m"},
            {"spoor": "Spoor 3", "type": "NID Spoor", "lengte": "598m"},
            {"spoor": "Spoor 4", "type": "NID Spoor", "lengte": "507m"},
            {"spoor": "Spoor 5", "type": "NID Spoor", "lengte": "540m"}
        ],
        "spooroverzicht": [
            {"spoor": "1", "bovenleiding": "Nee", "ltl": "374 m", "lol": "354 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "2", "bovenleiding": "Nee", "ltl": "557 m", "lol": "537 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "3", "bovenleiding": "Nee", "ltl": "618 m", "lol": "598 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "4", "bovenleiding": "Nee", "ltl": "527 m", "lol": "507 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "5", "bovenleiding": "Nee", "ltl": "527 m", "lol": "507 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "6", "bovenleiding": "Nee", "ltl": "530 m", "lol": "510 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "7", "bovenleiding": "Nee", "ltl": "498 m", "lol": "478 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "8", "bovenleiding": "Nee", "ltl": "521 m", "lol": "501 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "9", "bovenleiding": "Nee", "ltl": "567 m", "lol": "547 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Achterkaaibundel NID"},
            {"spoor": "10", "bovenleiding": "Nee", "ltl": "644 m", "lol": "624 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Doorgangsspoor naar sporen 11 & 12"},
            {"spoor": "11", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "ICO 3 Laadhelling auto's"},
            {"spoor": "12", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "ICO 3 Laadhelling auto's"},
            {"spoor": "Westerover 4", "bovenleiding": "Nee", "ltl": "574 m", "lol": "554 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "NID Westerover achterkaaispoor"},
            {"spoor": "Westerover 5", "bovenleiding": "Nee", "ltl": "574 m", "lol": "554 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "NID Westerover achterkaaispoor"}
        ],
        "overwegen_tracé": []
    },
    "brugge_vorming": {
        "id": "brugge_vorming",
        "zone_id": "brugge",
        "naam": "Bundels Brugge (Vorming & Bundel M)",
        "ppgi_referentie": "PPGI_1_FR_B_Brugge (Versie 1.0 - 12/06/2026)",
        "ssp_referentie": "SSP Brugge",
        "beseind": True,
        "seinen_info": "Beseinde rangeerbundels L50A / L51.",
        "bovenleiding_info": "Volledig geëlektrificeerd.",
        "tankinstallatie": "Aanwezig te Brugge.",
        "parkeergelegenheid": ["Stationsomgeving Brugge / Spoorwegstraat"],
        "cameras": "Infrabel cameratoezicht.",
        "schuifrangering": "Toegelaten conform seinzaal Brugge.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "651-657", "bovenleiding": "Ja", "ltl": "180-280 m", "lol": "160-260 m", "helling": "0-1 mm/m naar Gent", "doodspoor": "Nee", "functie": "Bundel A Brugge (Reizigers/Vorming)"},
            {"spoor": "681-687", "bovenleiding": "Ja", "ltl": "164-318 m", "lol": "144-298 m", "helling": "0-1 mm/m naar Gent", "doodspoor": "Nee", "functie": "Bundel B Brugge"},
            {"spoor": "661-664", "bovenleiding": "Ja", "ltl": "625-755 m", "lol": "605-735 m", "helling": "2-3 mm/m (naar het midden van de sporen)", "doodspoor": "Nee", "functie": "Bundel U • Goederen- & vormingsbundel"},
            {"spoor": "665-667", "bovenleiding": "Ja", "ltl": "670 m", "lol": "650 m", "helling": "2-3 mm/m (naar het midden van de sporen)", "doodspoor": "Nee", "functie": "Bundel V • Goederenbundel"},
            {"spoor": "675 / 676", "bovenleiding": "Nee", "ltl": "ca. 200 m", "lol": "ca. 180 m", "helling": "Sterke daling naar station Brugge (schaats verplicht!)", "doodspoor": "Ja", "functie": "Aansluiting SA Alstom"}
        ],
        "overwegen_tracé": []
    },
    "plassendale": {
        "id": "plassendale",
        "zone_id": "oostende",
        "naam": "Bundel Plassendale 1",
        "ppgi_referentie": "PP-341-Brugge (Actiezone Oostende, Versie 25.0)",
        "ssp_referentie": "SSP Oostende",
        "beseind": True,
        "seinen_info": "Beseinde bundel L50A.",
        "bovenleiding_info": "Bovenleiding aanwezig.",
        "tankinstallatie": "Oostende.",
        "parkeergelegenheid": ["Industrieterrein Plassendale"],
        "cameras": "Toezicht aanwezig.",
        "schuifrangering": "Kleine beweging.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "3", "bovenleiding": "Nee", "ltl": "498 m", "lol": "478 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Laad- en losspoor goederen Plassendale"},
            {"spoor": "4", "bovenleiding": "Nee", "ltl": "498 m", "lol": "478 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Laad- en losspoor goederen Plassendale"},
            {"spoor": "Tilbury 1 & 2", "bovenleiding": "Nee", "ltl": "330 m", "lol": "310 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Laad- en losspoor goederenoverslag"},
            {"spoor": "Proviron", "bovenleiding": "Nee", "ltl": "300 m", "lol": "280 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Spooraansluiting Chemie Proviron"}
        ],
        "overwegen_tracé": []
    },
    "kortrijk_vorming": {
        "id": "kortrijk_vorming",
        "zone_id": "kortrijk",
        "naam": "Bundels Kortrijk (Vorming, Goederen & Lauwe)",
        "ppgi_referentie": "PPGI_1_FR_D_Kortrijk (Versie 2.0 - 18/09/2026)",
        "ssp_referentie": "SSP Kortrijk",
        "beseind": True,
        "seinen_info": "Seinzaal Kortrijk.",
        "bovenleiding_info": "Geëlektrificeerd L75.",
        "tankinstallatie": "Kortrijk.",
        "parkeergelegenheid": ["Kortrijk Goederenkoer / Stationsomgeving"],
        "cameras": "Infrabel toezicht.",
        "schuifrangering": "Rangeerregels Kortrijk.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "Bundel Kortrijk 1-8", "bovenleiding": "Ja", "ltl": "450-650 m", "lol": "430-630 m", "helling": "0-1 mm/m", "doodspoor": "Nee", "functie": "Vormings- en goederensporen L75"},
            {"spoor": "Lauwe 1 & 2", "bovenleiding": "Ja", "ltl": "500 m", "lol": "480 m", "helling": "0-1 mm/m", "doodspoor": "Nee", "functie": "Vormingsspoor Lauwe"},
            {"spoor": "Aansluiting I-O.3", "bovenleiding": "Ja", "ltl": "380 m", "lol": "360 m", "helling": "0-1 mm/m", "doodspoor": "Ja", "functie": "Industriespoor Kortrijk"}
        ],
        "overwegen_tracé": []
    },
    "lijn69_poperinge": {
        "id": "lijn69_poperinge",
        "zone_id": "kortrijk",
        "naam": "Lijn 69 (Kortrijk – Ieper – Poperinge)",
        "ppgi_referentie": "PPGI_1_FR_D (Spoorlijn 69, Blz. 30 & 38)",
        "ssp_referentie": "SSP Zone Kortrijk / Lijn 69",
        "beseind": False,
        "seinen_info": "Enkelsporig baanvak met goederensporen te Poperinge.",
        "bovenleiding_info": "Volledig geëlektrificeerd (3kV DC).",
        "tankinstallatie": "Kortrijk Vorming.",
        "parkeergelegenheid": ["Europalaan / Stationsomgeving Poperinge"],
        "cameras": "Toezicht Infrabel / NMBS.",
        "schuifrangering": "Bedieningsbeweging op spoor 4 & 5 mits toelating Seinzaal Kortrijk (FR/D).",
        "bundel_sporen": [
            {"spoor": "Spoor 4 (654)", "type": "Goederenspoor Poperinge", "beveiliging": "Stootblok"},
            {"spoor": "Spoor 5 (655)", "type": "Goederenspoor Poperinge", "beveiliging": "Stootblok"}
        ],
        "spooroverzicht": [
            {"spoor": "4 (654)", "bovenleiding": "Ja", "ltl": "322 m", "lol": "302 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Goederenspoor Poperinge"},
            {"spoor": "5 (655)", "bovenleiding": "Ja", "ltl": "322 m", "lol": "302 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Goederenspoor Poperinge"},
            {"spoor": "681", "bovenleiding": "Ja", "ltl": "94 m", "lol": "74 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Doodspoor Poperinge"},
            {"spoor": "121", "bovenleiding": "Ja", "ltl": "308 m", "lol": "288 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Rangeersas L.69 tussen P-O.3 en stopbord"}
        ],
        "overwegen_tracé": []
    },
    "roeselare_bundel": {
        "id": "roeselare_bundel",
        "zone_id": "brugge",
        "naam": "Bundels Roeselare & Lichtervelde (L66)",
        "ppgi_referentie": "PPGI_1_FR_B (Lijn 66 / L73)",
        "ssp_referentie": "SSP Midden-West-Vlaanderen",
        "beseind": True,
        "seinen_info": "Seinzaal Brugge (FR/B).",
        "bovenleiding_info": "Geëlektrificeerd L66.",
        "tankinstallatie": "Brugge Vorming.",
        "parkeergelegenheid": ["Goederenkoer Roeselare"],
        "cameras": "Infrabel cameratoezicht.",
        "schuifrangering": "Conform Seinzaal Brugge.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "Sporen 1-4", "bovenleiding": "Ja", "ltl": "480-550 m", "lol": "460-530 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Goederenbundel Roeselare (L66)"},
            {"spoor": "LCI Lichtervelde", "bovenleiding": "Nee", "ltl": "200 m", "lol": "180 m", "helling": "0-1 mm/m", "doodspoor": "Ja", "functie": "Infrabel Logistiek spoor"}
        ],
        "overwegen_tracé": []
    },
    "kust_bundels": {
        "id": "kust_bundels",
        "zone_id": "brugge",
        "naam": "Bundels Blankenberge & De Panne",
        "ppgi_referentie": "PPGI_1_FR_B (Lijn 51 & Lijn 73)",
        "ssp_referentie": "SSP Zone Kust",
        "beseind": True,
        "seinen_info": "Seinzaal Brugge (FR/B).",
        "bovenleiding_info": "Geëlektrificeerd (L51) / Deels diesel (L73).",
        "tankinstallatie": "Brugge Vorming.",
        "parkeergelegenheid": ["Stationsomgeving"],
        "cameras": "Infrabel toezicht.",
        "schuifrangering": "Conform Seinzaal Brugge.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "Blankenberge Bundel M", "bovenleiding": "Ja", "ltl": "340 m", "lol": "320 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Opstelbundel M Blankenberge"},
            {"spoor": "De Panne Sporen 1-2", "bovenleiding": "Nee", "ltl": "270 m", "lol": "250 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Grenssporen De Panne (L73)"}
        ],
        "overwegen_tracé": []
    },
    "oostende_vorming": {
        "id": "oostende_vorming",
        "zone_id": "oostende",
        "naam": "Bundels Oostende (Vorming, Handelsdok & Tractie)",
        "ppgi_referentie": "PP-341-Brugge (Actiezone Oostende, Versie 25.0)",
        "ssp_referentie": "SSP Zone Oostende",
        "beseind": True,
        "seinen_info": "Seinzaal Oostende (Blok 4).",
        "bovenleiding_info": "Geëlektrificeerd L50A.",
        "tankinstallatie": "Aanwezig te Oostende Tractie.",
        "parkeergelegenheid": ["Oostende Spoorwegcomplex"],
        "cameras": "Infrabel cameratoezicht.",
        "schuifrangering": "Rangeerbewegingen via Seinzaal Oostende.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "114", "bovenleiding": "Ja", "ltl": "600 m", "lol": "580 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Ontvangstspoor goederentreinen Oostende"},
            {"spoor": "117-118", "bovenleiding": "Nee", "ltl": "360 m", "lol": "340 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Laad- en losspoor I-O.3 Oostende Vorming"},
            {"spoor": "Bundel A (400-418)", "bovenleiding": "Ja", "ltl": "270-380 m", "lol": "250-360 m", "helling": "1 mm/m", "doodspoor": "Deels", "functie": "Vormingsbundel Oostende"}
        ],
        "overwegen_tracé": []
    },
    "zeebrugge_kaai": {
        "id": "zeebrugge_kaai",
        "zone_id": "zeebrugge",
        "naam": "Bundels Zeebrugge Kaai (Voorhaven & CHZ)",
        "ppgi_referentie": "PP-311-Brugge (Actiezone Zeebrugge Voorhaven)",
        "ssp_referentie": "SSP Zeebrugge",
        "beseind": True,
        "seinen_info": "Blok 7 Zeebrugge.",
        "bovenleiding_info": "Grotendeels geëlektrificeerd.",
        "tankinstallatie": "Ramskapelle G&V.",
        "parkeergelegenheid": ["Zeebrugge Kaaiweg / CHZ"],
        "cameras": "Haven- en Infrabel camera's.",
        "schuifrangering": "Kleine beweging.",
        "bundel_sporen": [],
        "spooroverzicht": [
            {"spoor": "Zeebrugge Kaai (851)", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "functie": "Havenkaaispoor Zeebrugge (via spoor 851)"},
            {"spoor": "Zweedse Kaai 1-2", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "functie": "Kaaibediening Zweedse Kaai"}
        ],
        "overwegen_tracé": []
    }
}

# Detailed terminal definitions
LEVEL_5_DETAILED_TERMINALS = {
    "cro_brit": {
        "id": "cro_brit",
        "moederbundel_id": "ramskapelle",
        "naam": "C.RO Brittaniadok (SEA-RO)",
        "klant": "C.RO Ports Zeebrugge / SEA-RO",
        "documentcode": "DB Cargo/België/Bedieningsinstructie CRO Brittaniadok Ramskapelle",
        "huidige_versie": "2.2",
        "versie_datum": "08-05-2026",
        "vorige_versies": [
            {"versie": "2.0", "datum": "19-05-2021", "wijziging": "Eerste publicatie van het document conform uniforme lay-out."},
            {"versie": "2.1", "datum": "31-01-2022", "wijziging": "Wijzigen werkwijze poortbediening en aanpassen nieuwe lay-out."},
            {"versie": "2.2", "datum": "08-05-2026", "wijziging": "Inhoudelijke aanpassing na RI&E punten 4.2.2.4 en 7.3.3. Toevoeging: Punt 3 Wat te doen bij calamiteiten."}
        ],
        "auteurs": "Krist Verstraete; Maikel Vanzieleghem / Bart Vercaempst",
        "bron_referentie": "PP-321-Brugge (Zeebrugge Zuidelijk Insteekdok, Versie 37.0) & SSP Zone Brugge",
        "adres": "Gustave Van Nieuwenhuysestraat, Zeebrugge (Kaai 500-reeks)",
        "bereikbaarheid": {
            "trein": "Bereikbaar via L202B, Bundel Ramskapelle, spoor 872",
            "auto": "Gustave Van Nieuwenhuysestraat, Zeebrugge (parkeren aan Ramskapelle of kade)"
        },
        "contacten_klant": [
            {"dienst": "CRO Security / Poort 24/7", "rol": "Poortbediening & Nood sweep", "telefoon": "+32 50 55 78 35"},
            {"dienst": "CRO Kaaiverantwoordelijke", "rol": "Operationeel toezicht", "telefoon": "+32 50 55 78 11"}
        ],
        "infrastructuur": {
            "toegangsspoor": "Spoor 872 via wissel 321 vanaf L202B",
            "terminal_sporen": "Sporen 1 & 2 op kaai Brittaniadok",
            "beveiliging_infrabel": "Stuitklamp 321 met Siemensslot 321FR (Siemenskast nabij OW 17 afgesloten met Wilka G*) + Ontspoortong 10R bij sein ND-R.7",
            "laadkade": "Automotive Ro-Ro kade SEA-RO",
            "richting_lading": "Auto's op treinen moeten volgens order van dispatcher staan (standaard: autolichten kant kust bij plaatsing)."
        },
        "specifieke_risicos": [
            "Bovenleidingsgrens: Spoor 844 L202B is slechts deels geëlektrificeerd. Let op uitschakelbord.",
            "Overweg 17 (Sas): Manueel te bedienen overweg nabij de poort. Steeds stoppen voor bord 'STOP'.",
            "Stuitklamp: Stuitklamp 321 ligt tussen OW 17 en de poort. Vergewis je dat deze ontgrendeld en opengelegd is vóór binnenrijden.",
            "Poortalarm: Poort sluit automatisch na doorgang met voorafgaande zoemer (ongeveer 10 seconden)."
        ],
        "bedieningstijden": "24/7, niet gespecificeerd, op verzoek van de klant.",
        "procedures": {
            "procedure_1_toegang": [
                {"stap": 1, "titel": "Rit aanvragen", "beschrijving": "De bediende DB vraagt bij Infrabel Blok 7 toelating voor een rit van bundel Ramskapelle naar SA C-RO (spoor 872)."},
                {"stap": 2, "titel": "Stilstand voor STOP", "beschrijving": "De beweging rijdt via L202B en stopt vóór het bord 'STOP' opwaarts van overweg 17."},
                {"stap": 3, "titel": "Siemensslot & Stuitklamp", "beschrijving": "Bediende DB begeeft zich naar de slotkast (50m verder), vraagt slot 321FR via de telefoondoorgave aan Blok 7, neemt sleutel 321 uit het Siemensslot en legt stuitklamp 321 open."},
                {"stap": 4, "titel": "Overweg 17 bedienen", "beschrijving": "Bediende activeert manueel overweg 17 via de sleutelkast."},
                {"stap": 5, "titel": "Poort openen", "beschrijving": "Bediende neemt telefonisch contact op met CRO Security (+32 50 55 78 35) om de spoorpoort te openen."},
                {"stap": 6, "titel": "Binnenrijden & Beveiligen", "beschrijving": "Beweging rijdt de terminal binnen. Na binnenkomst stuitklamp 321 terug dichtleggen en vergrendelen. Sleutel 321 terug in het Siemensslot steken en naar rechts draaien om te vergrendelen. Overweg manueel deactiveren. Poort sluit met geluidssignaal."}
            ],
            "procedure_2_rangering_spoor_872": [
                {"stap": 1, "titel": "Toelating & Poort", "beschrijving": "Voor rangeringen van SA C-RO tot op spoor 872 laat de bediende de poort openen door CRO Security."},
                {"stap": 2, "titel": "Slot aanvragen Blok 7", "beschrijving": "Meld je via de slottelefoon aan bij Blok 7 en vraag slot 321FR om rangeringen uit te voeren tussen de terminal en spoor 872. OPGELET: Tijdens rangeringen zijn ritten naar Ramskapelle verboden!"},
                {"stap": 3, "titel": "OW 17 & Stuitklamp", "beschrijving": "Activeer OW 17 en leg stuitklamp 321 open met sleutel 321."},
                {"stap": 4, "titel": "Rangering uitvoeren", "beschrijving": "Voer de rangering uit. Beëindig de rangering ALTIJD op de spooraansluiting C-RO, nooit op spoor 872."},
                {"stap": 5, "titel": "Vergrendeling herstellen", "beschrijving": "Sluit de stuitklamp, vergrendel sleutel 321 in het Siemensslot (naar rechts draaien) en geef slot 321FR terug aan Blok 7."}
            ],
            "procedure_3_verlaten": [
                {"stap": 1, "titel": "Poort laten openen", "beschrijving": "Bediende DB laat de spoorpoort openen door de security van CRO."},
                {"stap": 2, "titel": "Stuitklamp openleggen", "beschrijving": "Vraag slot 321FR bij Blok 7, neem sleutel 321 en leg de stuitklamp open. Activeer OW 17."},
                {"stap": 3, "titel": "Buitenrijden & Hervergrendelen", "beschrijving": "De beweging rijdt de aansluiting buiten. Sluit stuitklamp 321, steek sleutel 321 terug in Siemensslot en draai naar rechts. Deactiveer OW 17."},
                {"stap": 4, "titel": "Aanmelden aan sein ND-R.7", "beschrijving": "Bediende meldt de trein aan bij Blok 7 aan groot stopsein ND-R.7 voor de terugrit naar bundel Ramskapelle."}
            ]
        }
    },
    "wal_can": {
        "id": "wal_can",
        "moederbundel_id": "ramskapelle",
        "naam": "Wallenius Canadakaai (CAST)",
        "klant": "Wallenius Wilhelmsen Solutions / CAST",
        "documentcode": "DB Cargo/België/Cast (Canadakaai/Wallenius)",
        "huidige_versie": "2.2",
        "versie_datum": "05-03-2025",
        "vorige_versies": [
            {"versie": "1.0", "datum": "28-10-2021", "wijziging": "Eerste publicatie van het document."},
            {"versie": "1.1", "datum": "29-10-2021", "wijziging": "Redactionele aanpassingen."},
            {"versie": "2.0", "datum": "01-10-2022", "wijziging": "Plaatsen elektrische stuitklamp bundel Cast."},
            {"versie": "2.1", "datum": "06-09-2023", "wijziging": "Aanpassen spoorbezetting en contactgegevens."},
            {"versie": "2.2", "datum": "05-03-2025", "wijziging": "Update veiligheidsmaatregelen en poortprocedure Canadakaai."}
        ],
        "auteurs": "Bart VERCAEMPST Teamleader DBC.BE",
        "bron_referentie": "PP-321-Brugge (Zeebrugge Zuidelijk Insteekdok) & SSP Zone Brugge",
        "adres": "Canadakaai, Zeebrugge (Kaai 100-reeks)",
        "bereikbaarheid": {
            "trein": "Bereikbaar via L202B, Bundel Ramskapelle, spoor 843",
            "auto": "Canadakaai, Zeebrugge"
        },
        "contacten_klant": [
            {"dienst": "Wallenius Dispatch / Terminal", "rol": "Kaaiplanning", "telefoon": "+32 50 54 22 11"},
            {"dienst": "Wallenius Security", "rol": "Poort & Bewaking", "telefoon": "+32 50 54 22 22"}
        ],
        "infrastructuur": {
            "toegangsspoor": "Spoor 843 (Bundel Cast)",
            "terminal_sporen": "Sporen 1 t.e.m. 4",
            "beveiliging_infrabel": "Stuitklamp spoor 843",
            "laadkade": "Automotive terminal Wallenius",
            "richting_lading": "Auto's conform opgave van dispatcher."
        },
        "specifieke_risicos": [
            "Aanrijden poort Canadakaai: Poort moet visueel gecontroleerd worden op volledige opening.",
            "Gevaar ontsporing einde bediening op kop van de bundel.",
            "Autoverkeer tussen sporen 2 & 3: Veelvuldige verplaatsing van auto's over de sporen door kade-arbeiders."
        ],
        "bedieningstijden": "24/7 op aanvraag van klant.",
        "procedures": {
            "procedure_1_toegang": [
                {"stap": 1, "titel": "Rit aanvragen", "beschrijving": "Rit aanvragen bij Blok 7 van Ramskapelle naar spoor 843."},
                {"stap": 2, "titel": "Stuitklamp & Poort", "beschrijving": "Stuitklamp ontgrendelen en poort openen in samenspraak met Wallenius security."},
                {"stap": 3, "titel": "Plaatsen wagens", "beschrijving": "Wagens plaatsen op aangewezen spoor (1 t.e.m. 4), ontkoppelen en immobiliseren."}
            ]
        }
    },
    "dartline": {
        "id": "dartline",
        "moederbundel_id": "voorhaven_west",
        "naam": "Herstelspoor Dartline",
        "klant": "CLDN / Dartline Herstelsporen",
        "documentcode": "DB Cargo/België/Bedieningsinstructie Herstelsporen Dartline v1.1",
        "huidige_versie": "1.1",
        "versie_datum": "14-04-2026",
        "vorige_versies": [
            {"versie": "1.0", "datum": "20-01-2020", "wijziging": "Aanmaak bedieningsinstructie."},
            {"versie": "1.1", "datum": "14-04-2026", "wijziging": "Nieuwe opmaak + volledige herinventarisering van de risico's."}
        ],
        "auteurs": "Stephane VERSCHUEREN; Bart VERCAEMPST; Maikel VANZIELEGHEM",
        "bron_referentie": "Plaatselijk Protocol 311 - Deel 1 - Zeebrugge (NID)",
        "adres": "Kielbankstraat / Kustlaan, Zeebrugge",
        "bereikbaarheid": {
            "trein": "Bereikbaar via L202, Bundel Voorhaven-West",
            "auto": "Kielbankstraat, Zeebrugge"
        },
        "contacten_klant": [
            {"dienst": "CLDN Werkplaats / Dartline", "rol": "Herstelspoor Verantwoordelijke", "telefoon": "+32 50 55 92 11"}
        ],
        "infrastructuur": {
            "toegangsspoor": "Spoor Voorhaven-West",
            "terminal_sporen": "Herstelsporen 1 & 2",
            "beveiliging_infrabel": "Handwissels en stopblokken",
            "laadkade": "Wagonherstelplaats met mobiele hefvijzels",
            "richting_lading": "NVT (Wagonherstellingen)"
        },
        "specifieke_risicos": [
            "Einde van het spoor: Let op stootblokken.",
            "Overweg 3de categorie: Verplicht beveiligen.",
            "Mobiele hefvijzels: Vergewis je van vrije doorgang en profielruimte.",
            "Mogelijke aanwezigheid van transmigranten rond de werkplaats."
        ],
        "bedieningstijden": "Dagdienst / op afroep.",
        "procedures": {
            "procedure_1_toegang": [
                {"stap": 1, "titel": "Toegang & Vrijgave", "beschrijving": "Afstemmen met werkleider Dartline en spoorprofiel controleren."},
                {"stap": 2, "titel": "Plaatsen defecte wagens", "beschrijving": "Wagens voorzichtig opduwen, klemmen plaatsen en ontkoppelen."}
            ]
        }
    },
    "nid_ico": {
        "id": "nid_ico",
        "moederbundel_id": "nid",
        "naam": "NID ICO Northern Inlet Terminal",
        "klant": "International Car Operators (ICO)",
        "documentcode": "DB Cargo/België/Bedieningsinstructie Zeebrugge NID ICO Northern Inlet Terminal V2.0",
        "huidige_versie": "2.0",
        "versie_datum": "19-02-2026",
        "vorige_versies": [
            {"versie": "1.0", "datum": "12-04-2021", "wijziging": "Aanmaak bedieningsinstructie."},
            {"versie": "2.0", "datum": "19-02-2026", "wijziging": "Aanpassing 5.4.1 t.e.m. 5.4.3 op basis van wijzigingen PPGI v29.0."}
        ],
        "auteurs": "Bart VERCAEMPST Teamleader DBC.BE",
        "bron_referentie": "PP-311-Brugge (Actiezone Zeebrugge NID)",
        "adres": "Westeroever / NID, Zeebrugge",
        "bereikbaarheid": {
            "trein": "Bereikbaar vanaf Bundel Zwankendamme via spoor 382 naar Bundel NID",
            "auto": "Kaai 100-reeks, Zeebrugge"
        },
        "contacten_klant": [
            {"dienst": "ICO Dispatch NID", "rol": "Kaaiplanning", "telefoon": "+32 50 54 39 11"},
            {"dienst": "ICO Security Poort NID", "rol": "Toegangscontrole", "telefoon": "+32 50 54 39 20"}
        ],
        "infrastructuur": {
            "toegangsspoor": "Spoor 382 vanaf Zwankendamme",
            "terminal_sporen": "Sporen 4 & 5 (lengte 507m en 540m) of 11 & 12",
            "beveiliging_infrabel": "Ontspoortong en beweegbare brug",
            "laadkade": "Automotive Terminal Westeroever",
            "richting_lading": "Autolichten dienen kant KUST te staan bij vertrek vanuit Zwankendamme!"
        },
        "specifieke_risicos": [
            "Druk bereden overweg NID.",
            "Ontspoortong en beweegbare brug.",
            "Vertrek ALTIJD vanuit bundel Zwankendamme, NOOIT vanuit de vorming!"
        ],
        "bedieningstijden": "24/7 volgens dispatcher planning.",
        "procedures": {
            "procedure_1_toegang": [
                {"stap": 1, "titel": "Vertrek Zwankendamme", "beschrijving": "Elke beweging voor NID vertrekt vanuit bundel Zwankendamme. Autolichten controleren: moeten kant KUST staan."},
                {"stap": 2, "titel": "Spoorverificatie", "beschrijving": "Vergewis je op welke sporen de trein geplaatst moet worden (sporen 4&5 of 11&12)."},
                {"stap": 3, "titel": "Beweegbare brug & Ontspoortong", "beschrijving": "Controleer de seinstand en brugvergrendeling alvorens op te rijden."}
            ]
        }
    }
}



# ============================================================
# LEVEL 5 TERMINAL TRACK OVERVIEWS (SPOOROVERZICHT, LENGTES, HELLING)
# ============================================================
LEVEL_5_TERMINAL_TRACK_OVERVIEWS = {
    "cro_brit": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Containers SEA-RO", "bovenleiding": "Nee (diesel)", "ltl": "540 m", "lol": "520 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk aan kadezijde"},
            {"spoor": "Spoor 2", "bestemming": "Containers SEA-RO", "bovenleiding": "Nee (diesel)", "ltl": "540 m", "lol": "520 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk aan kadezijde"},
            {"spoor": "Spoor 3", "bestemming": "Containers SEA-RO", "bovenleiding": "Nee (diesel)", "ltl": "585 m", "lol": "565 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk aan kadezijde"},
            {"spoor": "Spoor 4", "bestemming": "Containers SEA-RO", "bovenleiding": "Nee (diesel)", "ltl": "585 m", "lol": "565 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk aan kadezijde"},
            {"spoor": "Spoor 5", "bestemming": "Automotive (Auto's)", "bovenleiding": "Nee (diesel)", "ltl": "335 m", "lol": "315 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Neuzen gericht naar zee (kust) bij plaatsing"},
            {"spoor": "Spoor 6", "bestemming": "Automotive (Auto's)", "bovenleiding": "Nee (diesel)", "ltl": "335 m", "lol": "315 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Neuzen gericht naar zee (kust) bij plaatsing"},
            {"spoor": "Spoor 7", "bestemming": "Automotive (Auto's)", "bovenleiding": "Nee (diesel)", "ltl": "392 m", "lol": "372 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Neuzen gericht naar zee (kust) bij plaatsing"},
            {"spoor": "Spoor 8", "bestemming": "Automotive (Auto's)", "bovenleiding": "Nee (diesel)", "ltl": "444 m", "lol": "424 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Neuzen gericht naar zee (kust) bij plaatsing"}
        ]
    },
    "wal_can": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Automotive / Ro-Ro", "bovenleiding": "Nee", "ltl": "438 m", "lol": "418 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Kaai 107-108"},
            {"spoor": "Spoor 2", "bestemming": "Automotive / Ro-Ro", "bovenleiding": "Nee", "ltl": "400 m", "lol": "380 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Kaai 107-108"},
            {"spoor": "Spoor 3", "bestemming": "Automotive / Ro-Ro", "bovenleiding": "Nee", "ltl": "370 m", "lol": "350 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Kaai 107-108"},
            {"spoor": "Spoor 4", "bestemming": "Automotive / Ro-Ro", "bovenleiding": "Nee", "ltl": "370 m", "lol": "350 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Kaai 107-108"}
        ]
    },
    "cdmz": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Car Delivery & Maintenance", "bovenleiding": "Nee", "ltl": "380 m", "lol": "360 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via spoor 898"},
            {"spoor": "Spoor 2", "bestemming": "Car Delivery & Maintenance", "bovenleiding": "Nee", "ltl": "380 m", "lol": "360 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via spoor 898"}
        ]
    },
    "ico_toy": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Hanze Toyota Automotive", "bovenleiding": "Nee", "ltl": "345 m", "lol": "325 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Hanze Kaai 100-reeks"},
            {"spoor": "Spoor 2", "bestemming": "Hanze Toyota Automotive", "bovenleiding": "Nee", "ltl": "345 m", "lol": "325 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Hanze Kaai 100-reeks"},
            {"spoor": "Spoor 3", "bestemming": "Hanze Toyota Automotive", "bovenleiding": "Nee", "ltl": "345 m", "lol": "325 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Hanze Kaai 100-reeks"},
            {"spoor": "Spoor 879", "bestemming": "Aansluitingsspoor Toyota", "bovenleiding": "Deels", "ltl": "292 m", "lol": "272 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Elektrische stuitklamp"}
        ]
    },
    "ico1": {
        "hellingsgraad": "0-1 ‰ (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 21", "bestemming": "Automotive Bastenakenkaai 1", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 521"},
            {"spoor": "Spoor 22", "bestemming": "Automotive Bastenakenkaai 1", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 521"},
            {"spoor": "Spoor 23", "bestemming": "Automotive Bastenakenkaai 1", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 521"},
            {"spoor": "Spoor 24", "bestemming": "Automotive Bastenakenkaai 1", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 521"}
        ]
    },
    "ico2": {
        "hellingsgraad": "0-1 ‰ (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor A", "bestemming": "Automotive Bastenakenkaai 2", "bovenleiding": "Nee", "ltl": "620 m", "lol": "600 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 502"},
            {"spoor": "Spoor B", "bestemming": "Automotive Bastenakenkaai 2", "bovenleiding": "Nee", "ltl": "580 m", "lol": "560 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 502"},
            {"spoor": "Spoor C", "bestemming": "Automotive Bastenakenkaai 2", "bovenleiding": "Nee", "ltl": "520 m", "lol": "500 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 502"},
            {"spoor": "Spoor D", "bestemming": "Automotive Bastenakenkaai 2", "bovenleiding": "Nee", "ltl": "450 m", "lol": "430 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Toegang via wissel 502"}
        ]
    },
    "efico": {
        "hellingsgraad": "0-1 ‰ (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Koffieterminal Efico", "bovenleiding": "Nee", "ltl": "260 m", "lol": "240 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Wissel 551"},
            {"spoor": "Spoor 2", "bestemming": "Koffieterminal Efico", "bovenleiding": "Nee", "ltl": "260 m", "lol": "240 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Wissel 551"}
        ]
    },
    "ndq": {
        "hellingsgraad": "0-1 ‰ (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "NDQ Logistics", "bovenleiding": "Nee", "ltl": "280 m", "lol": "260 m", "helling": "0-1 ‰ (vlak)", "doodspoor": "Ja", "opmerkingen": "Wissel 552"}
        ]
    },
    "spoorfuel": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 899", "bestemming": "G&V Spoorfuel Tankinstallatie", "bovenleiding": "Nee", "ltl": "130 m", "lol": "110 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Beveiligd met ontspoortong 91AR"}
        ]
    },
    "ecs_bl": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 358", "bestemming": "ECS 2XL Blauwe Loods", "bovenleiding": "Nee", "ltl": "360 m", "lol": "340 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Binnenbediening loods"},
            {"spoor": "Spoor 135", "bestemming": "Sasspoor naar Blauwe Loods", "bovenleiding": "Nee", "ltl": "360 m", "lol": "340 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Ontspoortong 96G"}
        ]
    },
    "2xl_bml": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 460", "bestemming": "2XL BML / ECS 1", "bovenleiding": "Nee", "ltl": "380 m", "lol": "360 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk"},
            {"spoor": "Wissel 524", "bestemming": "Omloopspoor ECS 1", "bovenleiding": "Ja", "ltl": "610 m", "lol": "590 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Omlooplocomotief"}
        ]
    },
    "nid_ico": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 10", "bestemming": "Aanvoerspoor NID", "bovenleiding": "Nee", "ltl": "644 m", "lol": "624 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Doorgang naar kophelling"},
            {"spoor": "Spoor 11", "bestemming": "ICO 3 Laadhelling", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Laadhelling auto's"},
            {"spoor": "Spoor 12", "bestemming": "ICO 3 Laadhelling", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Laadhelling auto's"}
        ]
    },
    "stora": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Stora Enso / PSA Breakbulk (binnen)", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Plaatsingsspoor binnen loods"},
            {"spoor": "Spoor 2", "bestemming": "Stora Enso (buiten)", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Uithaalspoor getrokken beweging"}
        ]
    },
    "dartline": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Dartline 1", "bestemming": "Herstelspoor Dartline", "bovenleiding": "Nee", "ltl": "637 m", "lol": "617 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Herstelling en opstelling"},
            {"spoor": "Dartline 2", "bestemming": "Herstelspoor Dartline", "bovenleiding": "Nee", "ltl": "632 m", "lol": "612 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Herstelling en opstelling"},
            {"spoor": "Dartline 3", "bestemming": "Herstelspoor Dartline", "bovenleiding": "Nee", "ltl": "643 m", "lol": "623 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Herstelling en opstelling"}
        ]
    },
    "alstom": {
        "hellingsgraad": "Sterke daling naar station Brugge (ca. 4-5 mm/m)",
        "helling_waarschuwing": "⚠️ KRITIEK VEILIGHEIDSVOORSCHRIFT: De aansluitingssporen van Alstom hellen sterk af in de richting van het reizigersstation Brugge! Bij het ontkoppelen en plaatsen van spoorvoertuigen moeten de schroefremmen krachtig worden aangedraaid én is het plaatsen van een wielblockschaats (schaats) aan de afwaartse zijde WETTELIJK VERPLICHT om ontlopen van materieel te verhinderen!",
        "sporen": [
            {"spoor": "Spoor 675", "bestemming": "SA Alstom Fabrieksspoor", "bovenleiding": "Nee", "ltl": "ca. 200 m", "lol": "ca. 180 m", "helling": "Sterke daling naar station Brugge", "doodspoor": "Ja", "opmerkingen": "Schaats en handremmen verplicht tegen ontlopen!"},
            {"spoor": "Spoor 676", "bestemming": "SA Alstom Testspoor", "bovenleiding": "Nee", "ltl": "ca. 180 m", "lol": "ca. 160 m", "helling": "Sterke daling naar station Brugge", "doodspoor": "Ja", "opmerkingen": "Schaats verplicht"}
        ]
    },
    "poperinge": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 4 (654)", "bestemming": "Goederenoverslag Poperinge", "bovenleiding": "Ja (3kV)", "ltl": "322 m", "lol": "302 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Vrije laadkoer"},
            {"spoor": "Spoor 5 (655)", "bestemming": "Goederenoverslag Poperinge", "bovenleiding": "Ja (3kV)", "ltl": "322 m", "lol": "302 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Vrije laadkoer"},
            {"spoor": "Spoor 681", "bestemming": "Kopspoor Poperinge", "bovenleiding": "Ja (3kV)", "ltl": "94 m", "lol": "74 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootjuk"},
            {"spoor": "Spoor 121", "bestemming": "Rangeersas L69", "bovenleiding": "Ja (3kV)", "ltl": "308 m", "lol": "288 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Sas tussen P-O.3 en stopbord"}
        ]
    },
    "plassendale": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 3", "bestemming": "Laad- en losspoor Plassendale", "bovenleiding": "Nee", "ltl": "498 m", "lol": "478 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Industrieterrein"},
            {"spoor": "Spoor 4", "bestemming": "Laad- en losspoor Plassendale", "bovenleiding": "Nee", "ltl": "498 m", "lol": "478 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Industrieterrein"}
        ]
    },
    "tilbury": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Tilbury Goederenoverslag", "bovenleiding": "Nee", "ltl": "330 m", "lol": "310 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootblok"},
            {"spoor": "Spoor 2", "bestemming": "Tilbury Goederenoverslag", "bovenleiding": "Nee", "ltl": "330 m", "lol": "310 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Stootblok"}
        ]
    },
    "proviron": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Proviron Spoor", "bestemming": "Chemicaliën overslag Proviron", "bovenleiding": "Nee", "ltl": "300 m", "lol": "280 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Veiligheidsafsluiting chemie"}
        ]
    },
    "bundel_roeselare": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1", "bestemming": "Vorming Roeselare", "bovenleiding": "Ja", "ltl": "520 m", "lol": "500 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Seinzaal Brugge"},
            {"spoor": "Spoor 2", "bestemming": "Vorming Roeselare", "bovenleiding": "Ja", "ltl": "500 m", "lol": "480 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Seinzaal Brugge"},
            {"spoor": "Spoor 3", "bestemming": "Vorming Roeselare", "bovenleiding": "Ja", "ltl": "480 m", "lol": "460 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Seinzaal Brugge"},
            {"spoor": "Spoor 4", "bestemming": "Vorming Roeselare", "bovenleiding": "Ja", "ltl": "480 m", "lol": "460 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Seinzaal Brugge"}
        ]
    },
    "bundel_blankenberge": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Bundel M", "bestemming": "Opstelbundel M Blankenberge", "bovenleiding": "Ja", "ltl": "340 m", "lol": "320 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "L51"}
        ]
    },
    "bundel_depanne": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1 & 2", "bestemming": "Grenssporen De Panne", "bovenleiding": "Nee", "ltl": "270 m", "lol": "250 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "L73"}
        ]
    },
    "lauwe": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1 & 2", "bestemming": "Vormingsspoor Lauwe", "bovenleiding": "Ja", "ltl": "500 m", "lol": "480 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "L75"}
        ]
    },
    "io3_kortrijk": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor I-O.3", "bestemming": "Bedieningsspoor I-O.3 Kortrijk", "bovenleiding": "Ja", "ltl": "380 m", "lol": "360 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Industriespoor"}
        ]
    },
    "kortrijk_vorming": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Bundelsporen 1-8", "bestemming": "Goederenbundel Kortrijk", "bovenleiding": "Ja", "ltl": "450-650 m", "lol": "430-630 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Seinzaal Kortrijk"}
        ]
    },
    "oostende_vorming": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 114", "bestemming": "Ontvangstspoor goederen", "bovenleiding": "Ja", "ltl": "600 m", "lol": "580 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Ontvangst treinen"},
            {"spoor": "Spoor 117-118", "bestemming": "I-O.3 Oostende Vorming", "bovenleiding": "Nee", "ltl": "360 m", "lol": "340 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Laad- en losspoor"}
        ]
    },
    "whv_oostende": {
        "hellingsgraad": "1 mm/m",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Bundel WET", "bestemming": "WHV Oostende & Bundel WET", "bovenleiding": "Ja", "ltl": "280-350 m", "lol": "260-330 m", "helling": "1 mm/m", "doodspoor": "Deels", "opmerkingen": "Werkplaatssporen"}
        ]
    },
    "cro_albert": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Kaaisporen Albert II Dok", "bestemming": "C.RO Albert II Dok Ro-Ro", "bovenleiding": "Nee", "ltl": "450 m", "lol": "430 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Haven Zeebrugge"}
        ]
    },
    "csp_term": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Cosco Sporen", "bestemming": "CSP Terminal Containerkade", "bovenleiding": "Nee", "ltl": "600 m", "lol": "580 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Haven Zeebrugge"}
        ]
    },
    "psa_zb": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "PSA Sporen", "bestemming": "PSA Zeebrugge Containertracks", "bovenleiding": "Nee", "ltl": "550 m", "lol": "530 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Haven Zeebrugge"}
        ]
    },
    "psa_hnn": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "PSA HNN Sporen", "bestemming": "PSA HNN Kaaisporen", "bovenleiding": "Nee", "ltl": "500 m", "lol": "480 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Haven Zeebrugge"}
        ]
    },
    "po_ferries": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "P&O Sporen", "bestemming": "P&O Ferries (501 / Zuid)", "bovenleiding": "Nee", "ltl": "380 m", "lol": "360 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Voorhaven Kaai 501"}
        ]
    },
    "po_nsf": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "NSF Sporen", "bestemming": "North Sea Ferries Kade", "bovenleiding": "Nee", "ltl": "350 m", "lol": "330 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Haven Zeebrugge"}
        ]
    },
    "zb_kaai": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 851", "bestemming": "Zeebrugge Kaai (Infrabel)", "bovenleiding": "Nee", "ltl": "340 m", "lol": "320 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Nee", "opmerkingen": "Havenkaaispoor"}
        ]
    },
    "zweedse_kaai": {
        "hellingsgraad": "<1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "Spoor 1 & 2", "bestemming": "Zweedse Kaai", "bovenleiding": "Nee", "ltl": "320 m", "lol": "300 m", "helling": "<1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Kaaibediening"}
        ]
    },
    "lci_brugge": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "LCI Sporen 1-2", "bestemming": "Infrabel Logistiek Centrum Brugge", "bovenleiding": "Nee", "ltl": "220 m", "lol": "200 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Infrabel logistiek materieel"}
        ]
    },
    "otwd_brugge": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "OTWD Werkplaatssporen", "bestemming": "Infrabel Werkplaats Brugge", "bovenleiding": "Deels", "ltl": "250 m", "lol": "230 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "Werkplaats"}
        ]
    },
    "lci_lichtervelde": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "LCI Spoor", "bestemming": "Infrabel Logistiek Lichtervelde", "bovenleiding": "Nee", "ltl": "200 m", "lol": "180 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "L66"}
        ]
    },
    "lci_kortrijk": {
        "hellingsgraad": "0-1 mm/m (vlak)",
        "helling_waarschuwing": None,
        "sporen": [
            {"spoor": "LCI Spoor", "bestemming": "Infrabel Logistiek Kortrijk", "bovenleiding": "Nee", "ltl": "220 m", "lol": "200 m", "helling": "0-1 mm/m (vlak)", "doodspoor": "Ja", "opmerkingen": "L75"}
        ]
    }
}


def get_all_terminal_summaries():
    """Load all 39 locations from locs_gps.json and enrich them with hierarchical mappings."""
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(workspace_dir, "locs_gps.json")
    if not os.path.exists(json_path):
        json_path = os.path.expandvars(r"%TEMP%\locs_gps.json")
    
    with open(json_path, encoding="utf-8") as f:
        locs_data = json.load(f)

    terminals = []
    for loc in locs_data["locations"]:
        lid = loc["id"]
        zone_code = loc.get("zone", "")
        cluster = (loc.get("cluster") or "").lower()
        mb_name = (loc.get("moederbundel") or "").lower()

        # Strict zonal and mother bundle classification
        if zone_code == "FR/D" or cluster in ["kortrijk", "zuidwest"]:
            if "poperinge" in lid or "69" in mb_name:
                mb_key = "lijn69_poperinge"
            else:
                mb_key = "kortrijk_vorming"
        elif zone_code == "FR/B" or cluster in ["brugge", "centraal", "kust"]:
            if "roeselare" in mb_name or "lichtervelde" in mb_name:
                mb_key = "roeselare_bundel"
            elif "blankenberge" in mb_name or "panne" in mb_name:
                mb_key = "kust_bundels"
            else:
                mb_key = "brugge_vorming"
        elif zone_code == "PP-341" or cluster == "oostende":
            if "plassendale" in mb_name:
                mb_key = "plassendale"
            else:
                mb_key = "oostende_vorming"
        else: # Zeebrugge PP-321 and PP-311
            if "ramskapelle" in mb_name:
                mb_key = "ramskapelle"
            elif "pelikaan" in mb_name:
                mb_key = "pelikaan"
            elif "voorhaven" in mb_name:
                mb_key = "voorhaven_west"
            elif "nid" in mb_name:
                mb_key = "nid"
            elif "kaai" in mb_name or "chz" in mb_name:
                mb_key = "zeebrugge_kaai"
            else:
                mb_key = "zwankendamme"

        terminals.append({
            "id": lid,
            "naam": loc["name"],
            "cluster": loc.get("cluster"),
            "zone": loc.get("zone"),
            "moederbundel_id": mb_key,
            "moederbundel_naam": loc.get("moederbundel"),
            "sporen": loc.get("sporen"),
            "adres": loc.get("adres"),
            "toegang_weg": loc.get("toegang_weg"),
            "beveiliging": loc.get("beveiliging"),
            "ppgi_ref": loc.get("ppgi_ref"),
            "has_bi": loc.get("has_bi"),
            "bi_version": loc.get("bi_version"),
            "is_detailed": lid in LEVEL_5_DETAILED_TERMINALS
        })
    return terminals


def resolve_bi(terminal_id):
    """
    Assemble complete uniform BI by cascading levels:
    Level 1 (Operator) -> Level 2 (Regio) -> Level 3 (Zone) -> Level 4 (Moederbundel) -> Level 5 (Terminal)
    """
    operator = LEVEL_1_OPERATOR
    regio = LEVEL_2_REGIO["west_vlaanderen"]

    # Check if we have an explicit detailed terminal
    if terminal_id in LEVEL_5_DETAILED_TERMINALS:
        terminal = LEVEL_5_DETAILED_TERMINALS[terminal_id]
        moederbundel = LEVEL_4_MOEDERBUNDELS.get(terminal["moederbundel_id"], LEVEL_4_MOEDERBUNDELS["ramskapelle"])
        zone = LEVEL_3_ZONES.get(moederbundel.get("zone_id", "zeebrugge"), LEVEL_3_ZONES["zeebrugge"])
    else:
        # Resolve dynamically from locs_gps.json
        summaries = {t["id"]: t for t in get_all_terminal_summaries()}
        loc = summaries.get(terminal_id)
        if not loc:
            return None
        
        moederbundel = LEVEL_4_MOEDERBUNDELS.get(loc["moederbundel_id"], LEVEL_4_MOEDERBUNDELS["zwankendamme"])
        zone = LEVEL_3_ZONES.get(moederbundel.get("zone_id", "zeebrugge"), LEVEL_3_ZONES["zeebrugge"])
        
        terminal = {
            "id": loc["id"],
            "moederbundel_id": loc["moederbundel_id"],
            "naam": loc["naam"],
            "klant": loc["naam"],
            "documentcode": f"DB Cargo/België/Bedieningsinstructie {loc['naam']}",
            "huidige_versie": loc.get("bi_version") or "1.0",
            "versie_datum": "23-10-2026",
            "vorige_versies": [
                {"versie": loc.get("bi_version") or "1.0", "datum": "23-10-2026", "wijziging": "Generatie conform uniforme hiërarchische structuur."}
            ],
            "auteurs": "Bart VERCAEMPST Teamleader DBC.BE",
            "bron_referentie": f"{loc.get('ppgi_ref') or moederbundel.get('ppgi_referentie')} & {moederbundel.get('ssp_referentie')}",
            "adres": loc.get("adres") or f"{loc['naam']}, West-Vlaanderen",
            "bereikbaarheid": {
                "trein": f"Bereikbaar via {moederbundel.get('naam')} ({loc.get('sporen')})",
                "auto": loc.get("toegang_weg") or loc.get("adres")
            },
            "contacten_klant": [
                {"dienst": f"Verantwoordelijke {loc['naam']}", "rol": "Operationeel toezicht", "telefoon": "Ter plaatse / via Dispatcher"}
            ],
            "infrastructuur": {
                "toegangsspoor": f"Toegangsspoor vanaf {moederbundel.get('naam')}",
                "terminal_sporen": loc.get("sporen") or "Bedieningssporen",
                "beveiliging_infrabel": loc.get("beveiliging") or "Handbediende wissels en/of stootblokken",
                "laadkade": "Bedienings- en laadsporen",
                "richting_lading": "Conform planning van rangeerploeg / dispatcher."
            },
            "specifieke_risicos": [
                f"Beveiliging: {loc.get('beveiliging') or 'Wissels en beveiliging controleren vóór berijden.'}",
                "Profielruimte: Let op obstakels en laadkaden langs de bedieningssporen."
            ],
            "bedieningstijden": "Op aanvraag van de klant.",
            "procedures": {
                "procedure_1_toegang": [
                    {"stap": 1, "titel": "Rit aanvragen", "beschrijving": f"Rit aanvragen bij {zone.get('centraal_seinhuis')} naar de bedieningssporen van {loc['naam']}."},
                    {"stap": 2, "titel": "Beveiliging verifiëren", "beschrijving": f"Beveiliging ({loc.get('beveiliging') or 'wisselligging en stopblokken'}) verifiëren en spoor controleren op vrije profielruimte."},
                    {"stap": 3, "titel": "Plaatsen wagens", "beschrijving": "Wagens plaatsen op aangewezen spoor, afkoppelen en immobiliseren met schroefremmen/spieën."}
                ],
                "procedure_3_verlaten": [
                    {"stap": 1, "titel": "Koppelen & Beveiliging", "beschrijving": "Wagens controleren, koppelen en alle immobilisatiemiddelen verwijderen."},
                    {"stap": 2, "titel": "Toelating vertrek", "beschrijving": f"Toelating voor de terugrit aanvragen bij {zone.get('centraal_seinhuis')}."},
                    {"stap": 3, "titel": "Vertrek naar bundel", "beschrijving": f"De beweging rijdt via het toegangsspoor terug naar {moederbundel.get('naam')}."}
                ]
            }
        }

    # Aggregate contacts hierarchically
    all_realtime_contacts = []
    # Level 1: Operator
    for c in operator.get("contacten", []):
        all_realtime_contacts.append({**c, "niveau": "Niveau 1: Operator (DB Cargo)"})
    # Level 3: Lokale Dispatch voor DEZE zone
    if zone.get("local_dispatch"):
        all_realtime_contacts.append({**zone["local_dispatch"], "niveau": f"Niveau 3: Lokale Dispatch ({zone.get('naam')})"})
    # Level 3: Seinhuis voor DEZE zone
    for c in zone.get("seinhuis_contacten", []):
        all_realtime_contacts.append({**c, "niveau": f"Niveau 3: Seinhuis ({zone.get('centraal_seinhuis')})"})
    # Level 3: Havenautoriteit
    if zone.get("havenautoriteit"):
        ha = zone["havenautoriteit"]
        all_realtime_contacts.append({"dienst": ha["naam"], "rol": "Havenautoriteit", "telefoon": f"{ha['telefoon']} ({ha['vhf_kanalen']})", "niveau": "Niveau 3: Zone Haven"})
    # Level 5: Terminal
    for c in terminal.get("contacten_klant", []):
        all_realtime_contacts.append({**c, "niveau": f"Niveau 5: Terminal ({terminal['naam']})"})

    # Aggregate emergency contacts
    all_noodcontacten = []
    for c in operator.get("noodcontacten", []):
        all_noodcontacten.append({**c, "niveau": "Niveau 1: Landelijk / Operator"})
    if regio.get("permanentie_ito"):
        all_noodcontacten.append({"dienst": "Permanentie I-TO Infrabel Area NW", "rol": "Infrabel Noodopvolging", "telefoon": regio["permanentie_ito"], "niveau": "Niveau 2: Regio West-Vlaanderen"})

    # Aggregate risks
    all_risicos = []
    for r in operator.get("algemene_veiligheidsregels", []):
        all_risicos.append({"type": "Bedrijfsvoorschrift", "omschrijving": r, "bron": "Niveau 1: DB Cargo Belgium"})
    for r in zone.get("zone_risicos", []):
        all_risicos.append({"type": "Zonerisico", "omschrijving": r, "bron": f"Niveau 3: Zone {zone.get('naam')}"})
    for r in terminal.get("specifieke_risicos", []):
        all_risicos.append({"type": "Terminal-specifiek risico", "omschrijving": r, "bron": f"Niveau 5: {terminal.get('naam')}"})

    # Terminal spooroverzicht resolution
    term_tracks_info = LEVEL_5_TERMINAL_TRACK_OVERVIEWS.get(terminal["id"])
    if not term_tracks_info:
        # Fallback dynamic generator
        term_tracks_info = {
            "hellingsgraad": "0-1 mm/m (vlak)",
            "helling_waarschuwing": None,
            "sporen": [
                {"spoor": terminal.get("infrastructuur", {}).get("terminal_sporen", "Bedieningsspoor"),
                 "bestemming": terminal["naam"],
                 "bovenleiding": "Nee",
                 "ltl": "Nader te bepalen",
                 "lol": "Nader te bepalen",
                 "helling": "0-1 mm/m (vlak)",
                 "doodspoor": "Ja",
                 "opmerkingen": terminal.get("infrastructuur", {}).get("beveiliging_infrabel", "Standaard beveiliging")}
            ]
        }
    
    if "infrastructuur" in terminal:
        terminal["infrastructuur"]["spooroverzicht"] = term_tracks_info["sporen"]
        terminal["infrastructuur"]["hellingsgraad"] = term_tracks_info["hellingsgraad"]
        terminal["infrastructuur"]["helling_waarschuwing"] = term_tracks_info["helling_waarschuwing"]

    assembled_bi = {
        "terminal_id": terminal["id"],
        "metadata": {
            "documentcode": terminal["documentcode"],
            "titel": f"Bedieningsinstructie {terminal['naam']}",
            "terminal_naam": terminal["naam"],
            "moederbundel_naam": moederbundel.get("naam", ""),
            "zone_naam": zone.get("naam", ""),
            "regio_naam": regio.get("naam", ""),
            "huidige_versie": terminal["huidige_versie"],
            "versie_datum": terminal["versie_datum"],
            "auteurs": terminal["auteurs"],
            "autorisatie_functionaris": operator["autorisatie_functionaris"],
            "autorisatie_ingangsdatum": operator["autorisatie_ingangsdatum"],
            "goedkeuring_systeem": operator["goedkeuring_systeem"],
            "bron_referentie": terminal["bron_referentie"],
            "gebruikersgroep": operator["gebruikersgroep"]
        },
        "hierarchie_levels": {
            "level_1_operator": {"naam": operator["naam"], "code": operator["id"]},
            "level_2_regio": {"naam": regio["naam"], "code": regio["id"]},
            "level_3_zone": {"naam": zone["naam"], "code": zone["id"], "seinhuis": zone.get("centraal_seinhuis")},
            "level_4_moederbundel": {"naam": moederbundel["naam"], "code": moederbundel["id"], "ppgi": moederbundel.get("ppgi_referentie")},
            "level_5_terminal": {"naam": terminal["naam"], "code": terminal["id"]}
        },
        "versiebeheer": terminal.get("vorige_versies", []),
        "contactpersonen": {
            "realtime": all_realtime_contacts,
            "calamiteiten": all_noodcontacten
        },
        "installaties": {
            "situering": {
                "adres": terminal["adres"],
                "bereikbaarheid": terminal["bereikbaarheid"]
            },
            "moederbundel": {
                "naam": moederbundel.get("naam"),
                "ppgi_referentie": moederbundel.get("ppgi_referentie"),
                "ssp_referentie": moederbundel.get("ssp_referentie"),
                "beseind": moederbundel.get("beseind"),
                "seinen_info": moederbundel.get("seinen_info"),
                "bovenleiding_info": moederbundel.get("bovenleiding_info"),
                "tankinstallatie": moederbundel.get("tankinstallatie"),
                "parkeergelegenheid": moederbundel.get("parkeergelegenheid"),
                "sporen": moederbundel.get("bundel_sporen", []),
                "spooroverzicht": moederbundel.get("spooroverzicht", []),
                "overwegen": moederbundel.get("overwegen_tracé", [])
            },
            "terminal": terminal.get("infrastructuur", {})
        },
        "veiligheid_en_risicos": all_risicos,
        "plaatselijke_regelgeving": {
            "snelheden": {
                "bundel": zone.get("zone_snelheden", {}).get("havenlijnen", "Max 20 km/u"),
                "aansluiting": zone.get("zone_snelheden", {}).get("aansluitingen", "Max 10 km/u"),
                "laadkade": zone.get("zone_snelheden", {}).get("kaden", "Stapvoets")
            },
            "bedieningstijden": terminal.get("bedieningstijden", "24/7 op aanvraag"),
            "immobilisatie": "Minimum 6 ‰ hellingswaarde hanteren bij aangekondigd stormweer. Voertuigen onderling gekoppeld.",
            "remproeven": "Volledige remproef na samenstelling, vereenvoudigde remproef na afhaling/aangroei."
        },
        "infrastructuur": terminal.get("infrastructuur", {}),
        "procedures": terminal.get("procedures", {})
    }
    return assembled_bi


# ============================================================
# PPGI vs BI REVIEWER & AUDIT PROPOSAL ENGINE
# ============================================================
PPGI_REVIEW_PROPOSALS = [
    {
        "id": "PROP-2026-001",
        "titel": "Formalisering van 3 afzonderlijke procedures C-RO (spoor 872)",
        "urgentie": "HOOG",
        "urgentie_badge": "danger",
        "bron_document": "PP-321-Brugge (Zeebrugge Zuidelijk Insteekdok, Versie 37.0 - 17/10/2025)",
        "bron_sectie": "Rubriek 1.3.3.2: Bediening SA C-RO, blz. 30-32 (wijziging v36.0 & v37.0)",
        "niveau": "Niveau 5: Terminal (CRO Brittaniadok)",
        "huidige_waarde_bi": "De huidige BI v2.2 combineert de toegang en uithaling in een algemeen stappenplan, maar benoemt de specifieke tussentijdse rangeringen op spoor 872 niet als formele procedure.",
        "voorgestelde_waarde_ppgi": "Infrabel schrijft in v37.0 strikt 3 afzonderlijke procedures voor: 1. Toegang tot SA C-RO, 2. Rangering van/naar C-RO tot op spoor 872, 3. Verlaten van SA C-RO.",
        "motivering": "Na een veiligheidsincident op spoor 872 heeft Infrabel in v36.0 en v37.0 de rangeringen formeel gereglementeerd. De BI moet hier 100% mee stroken om sancties of onveilige situaties te vermijden.",
        "status": "Aanbevolen voor implementatie in v2.3",
        "toegepast": False
    },
    {
        "id": "PROP-2026-002",
        "titel": "Rijverbod naar Ramskapelle tijdens rangeringen spoor 872",
        "urgentie": "HOOG",
        "urgentie_badge": "danger",
        "bron_document": "PP-321-Brugge Versie 37.0 (17/10/2025)",
        "bron_sectie": "Rubriek 1.3.3.2, blz. 32",
        "niveau": "Niveau 5: Terminal (CRO Brittaniadok)",
        "huidige_waarde_bi": "Geen expliciet verbod op gelijktijdige ritten van/naar Ramskapelle vermeld in Hoofdstuk 5 of 7.",
        "voorgestelde_waarde_ppgi": "Voeg verplichte waarschuwing toe: 'Opgelet! Tijdens het uitvoeren van rangeringen van/naar C-RO tot op spoor 872 zijn ritten van en naar Bundel Ramskapelle niet toegelaten.' En: 'De rangering moet altijd beëindigd worden op de spooraansluiting, NOOIT op het spoor 872.'",
        "motivering": "Essentiële Infrabel-veiligheidsclausule om flankaanrijdingen en onbedoelde rijweginschakelingen te voorkomen.",
        "status": "Aanbevolen voor implementatie in v2.3",
        "toegepast": False
    },
    {
        "id": "PROP-2026-003",
        "titel": "Verplichte Siemensslot hervergrendeling (naar rechts draaien)",
        "urgentie": "MEDIUM",
        "urgentie_badge": "warning",
        "bron_document": "PP-321-Brugge Versie 37.0",
        "bron_sectie": "Rubriek 1.3.3.2, Stappenplan blz. 31 & 32",
        "niveau": "Niveau 4: Moederbundel Ramskapelle & Niveau 5",
        "huidige_waarde_bi": "BI vermeldt 'sleutel 321 terug vergrendelen in slotkast'.",
        "voorgestelde_waarde_ppgi": "Specificeer exact: 'Sleutel 321 terugplaatsen in het Siemensslot en naar RECHTS draaien. Dit vergrendelt de sleutel, waarna Blok 7 het slot 321FR terugkrijgt.'",
        "motivering": "Voorkomt dat machinisten of rangeerders de sleutel insteken zonder naar rechts te draaien, waardoor Blok 7 de seinvergrendeling niet kan vrijgeven.",
        "status": "Aanbevolen voor implementatie in v2.3",
        "toegepast": False
    },
    {
        "id": "PROP-2026-004",
        "titel": "Toevoeging officiële Mailbox Blok 7 & Slottelefoons POC",
        "urgentie": "MEDIUM",
        "urgentie_badge": "warning",
        "bron_document": "PP-321-Brugge Versie 34.0 & 35.0",
        "bron_sectie": "Rubriek 1.4.1 & 1.9, blz. 4 & 48",
        "niveau": "Niveau 3: Zone Zeebrugge (Gedeeld voor ALLE BI's)",
        "huidige_waarde_bi": "Alleen vaste telefoonnummers van Blok 7 opgenomen; geen e-mailadres voor formele wagenoverdrachten.",
        "voorgestelde_waarde_ppgi": "Toevoegen van mailbox 'rdc.nw.blok7@infrabel.be' en specifieke POC voor slotcommunicatie aan Niveau 3 brongegevens.",
        "motivering": "Infrabel eist dat schriftelijke meldingen en documenten over wagenoverdracht (template bijlage 1.11) digitaal worden verzonden.",
        "status": "Aanbevolen voor implementatie op Zoneniveau",
        "toegepast": False
    },
    {
        "id": "PROP-2026-005",
        "titel": "Opname Ontspoortong 10R bij sein ND-R.7",
        "urgentie": "INFO",
        "urgentie_badge": "info",
        "bron_document": "PP-321-Brugge Versie 37.0",
        "bron_sectie": "Rubriek 1.3.3.2, blz. 30",
        "niveau": "Niveau 4: Moederbundel Ramskapelle",
        "huidige_waarde_bi": "Alleen stuitklamp 321 vermeld als beveiligingstoestel.",
        "voorgestelde_waarde_ppgi": "Infrastructuurfiche aanvullen met: 'Tussen groot stopsein ND-R.7 en OW15, L202B, ligt ontspoortong 10R.'",
        "motivering": "Verhoogt het situatiebewustzijn van treinbestuurders bij het naderen van sein ND-R.7 bij de terugrit.",
        "status": "Aanbevolen voor implementatie op Moederbundelniveau",
        "toegepast": False
    }
]
