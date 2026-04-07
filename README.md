Plant Care Lite
===============
A custom Home Assistant integration for tracking plant watering schedules.
Version: 2026.4.1
Author: @kamil-michalski
Repository: https://github.com/kamil-michalski/plant_care_lite

-------------------------------------------------------------------------------

ABOUT
-----
Plant Care Lite helps you keep track of when to water your houseplants.
It automatically adjusts watering intervals based on the current season,
reminding you when each plant is due for watering.

The "Lite" in the name reflects the intentional scope of this integration.
It does not use any hardware sensors such as soil moisture probes, light
sensors, or temperature sensors. Watering schedules are based solely on
the current season (determined by the calendar month) and predefined
intervals for each plant group.

A full-featured "Plant Care" version with sensor support may be developed
in the future.

-------------------------------------------------------------------------------

REQUIREMENTS
------------
- Home Assistant 2026.4 or newer
- HACS (Home Assistant Community Store)

-------------------------------------------------------------------------------

INSTALLATION
------------
1. Open HACS in your Home Assistant instance.
2. Go to "Integrations" and click the menu in the top right corner.
3. Select "Custom repositories".
4. Add the following URL as an Integration:
   https://github.com/kamil-michalski/plant_care_lite
5. Find "Plant Care Lite" in HACS and click "Download".
6. Restart Home Assistant.
7. Go to Settings -> Devices & Services -> Add Integration.
8. Search for "Plant Care Lite" and follow the setup steps.

-------------------------------------------------------------------------------

ADDING A PLANT
--------------
Each plant is added as a separate config entry.

1. Go to Settings -> Devices & Services -> Plant Care Lite.
2. Click "Add entry".
3. Enter the plant name (e.g. "Ficus").
4. Select the plant group from the dropdown.
5. Click "Submit". No restart required.

-------------------------------------------------------------------------------

PLANT GROUPS
------------
Each plant must be assigned to one of the following groups.
Watering intervals are defined per group for each season.

Group              | Season         | Interval
-------------------|----------------|----------
Succulents/Cacti   | Summer         | 14 days
                   | Winter         | 30 days
-------------------|----------------|----------
Drought Tolerant   | Summer         | 10 days
                   | Winter         | 21 days
-------------------|----------------|----------
Tropical           | Summer         |  7 days
                   | Winter         | 14 days
-------------------|----------------|----------
Climbing Plants    | Summer         |  7 days
                   | Winter         | 14 days
-------------------|----------------|----------
Ferns / Moisture   | Summer         |  3 days
                   | Winter         |  5 days

Plants included in each group:

- Succulents/Cacti:  Succulent, Cactus, Desert Rose, Snake Plant
- Drought Tolerant:  ZZ Plant, Peperomia
- Tropical:          Ficus Benjamina, Ficus Salicifolia, Monstera, Croton,
                     Dracaena Fragrans, Golden Pothos, Polyscias, Chamaedorea,
                     Ivy
- Climbing Plants:   Bougainvillea
- Ferns / Moisture:  Fern, Peace Lily

-------------------------------------------------------------------------------

SEASONS
-------
The integration uses two seasons based on calendar month:

- Summer (active growth): April through September
- Winter (dormancy):      October through March

No external entities or sensors are required. The season is determined
automatically from the system date. This makes the integration fully portable
and ready to use on any Home Assistant instance without any additional setup.

-------------------------------------------------------------------------------

ENTITIES (per plant)
--------------------
For each plant entry, the following entities are created:

sensor.{name}_watering_interval
  Current recommended watering interval in days, based on season and group.

sensor.{name}_last_watered
  Timestamp of the last time the plant was watered.
  This value is persisted to storage and survives Home Assistant restarts.

sensor.{name}_status
  Current watering status. Possible values:
  - ok    : The plant has been watered within the required interval.
  - water : The plant is due for watering.

  The status updates daily at the same time of day as the last watering,
  and immediately after pressing the "Water now" button.
  If the plant has never been watered, the status is "water" by default.

button.{name}_water_now
  Press to record the current timestamp as the last watering time.
  This resets the status to "ok" and schedules the next status check.

-------------------------------------------------------------------------------

KNOWN LIMITATIONS
-----------------
- Watering intervals are fixed per group and season. There is no per-plant
  customization of intervals without modifying the source code.
- No integration with soil moisture sensors, light sensors, or thermometers.
- No push notifications. Use Home Assistant automations to send alerts
  based on the sensor.{name}_status entity if needed.

-------------------------------------------------------------------------------

LICENSE
-------
MIT License. See LICENSE file for details.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------


Plant Care Lite
===============
Niestandardowa integracja Home Assistant do śledzenia harmonogramów podlewania
roślin.
Wersja: 2026.4.1
Autor: @kamil-michalski
Repozytorium: https://github.com/kamil-michalski/plant_care_lite

-------------------------------------------------------------------------------

O INTEGRACJI
------------
Plant Care Lite pomaga śledzic, kiedy podlewac rosliny domowe.
Automatycznie dostosowuje czestotliwosc podlewania do aktualnej pory roku
i przypomina, kiedy kazda roslina wymaga podlania.

Czlon "Lite" w nazwie odzwierciedla swiadomy zakres integracji.
Nie wykorzystuje zadnych czujnikow sprzetowych, takich jak sondy wilgotnosci
gleby, czujniki swiatla czy temperatury. Harmonogramy podlewania sa oparte
wylacznie na aktualnej porze roku (wyznaczanej na podstawie miesiaca
kalendarzowego) oraz predefiniowanych interwalach dla kazdej grupy roslin.

Pelnowymiarowa wersja "Plant Care" z obsluga czujnikow moze zostac
opracowana w przyszlosci.

-------------------------------------------------------------------------------

WYMAGANIA
---------
- Home Assistant 2026.4 lub nowszy
- HACS (Home Assistant Community Store)

-------------------------------------------------------------------------------

INSTALACJA
----------
1. Otworz HACS w swojej instancji Home Assistant.
2. Przejdz do sekcji "Integracje" i kliknij menu w prawym gornym rogu.
3. Wybierz "Niestandardowe repozytoria".
4. Dodaj ponizszy adres URL jako Integracje:
   https://github.com/kamil-michalski/plant_care_lite
5. Znajdz "Plant Care Lite" w HACS i kliknij "Pobierz".
6. Uruchom ponownie Home Assistant.
7. Przejdz do Ustawienia -> Urzadzenia i uslugi -> Dodaj integracje.
8. Wyszukaj "Plant Care Lite" i wykonaj kroki konfiguracji.

-------------------------------------------------------------------------------

DODAWANIE ROSLINY
-----------------
Kazda roslina jest dodawana jako osobny wpis konfiguracji.

1. Przejdz do Ustawienia -> Urzadzenia i uslugi -> Plant Care Lite.
2. Kliknij "Dodaj wpis".
3. Wprowadz nazwe rosliny (np. "Fikus").
4. Wybierz grupe rosliny z listy rozwijanej.
5. Kliknij "Zatwierdz". Restart nie jest wymagany.

-------------------------------------------------------------------------------

GRUPY ROSLIN
------------
Kazda roslina musi byc przypisana do jednej z ponizszych grup.
Interwaly podlewania sa zdefiniowane dla kazdej grupy i pory roku.

Grupa              | Pora roku      | Interwal
-------------------|----------------|----------
Sukulenty i kaktusy| Lato           | 14 dni
                   | Zima           | 30 dni
-------------------|----------------|----------
Sucholubne         | Lato           | 10 dni
                   | Zima           | 21 dni
-------------------|----------------|----------
Tropikalne         | Lato           |  7 dni
                   | Zima           | 14 dni
-------------------|----------------|----------
Pnacza             | Lato           |  7 dni
                   | Zima           | 14 dni
-------------------|----------------|----------
Paprocie/Wilgociol.| Lato           |  3 dni
                   | Zima           |  5 dni

Rosliny w poszczegolnych grupach:

- Sukulenty i kaktusy: Sukulent, Kaktus, Roza pustyni, Wezownica
- Sucholubne:          Zamiokulkas, Peperomia
- Tropikalne:          Fikus Beniamina, Fikus wierzbolistny, Monstera, Kroton,
                       Dracena wonna, Epipremnum zlociste, Polyscias, Chamedora,
                       Bluszcz
- Pnacza:              Bugenwilla
- Paprocie/Wilgociol.: Paproc, Skrzydlokwiat

-------------------------------------------------------------------------------

PORY ROKU
---------
Integracja rozroznia dwie pory roku na podstawie miesiaca kalendarzowego:

- Lato (intensywny wzrost): Kwiecien - Wrzesien
- Zima (odpoczynek):        Pazdziernik - Marzec

Nie sa wymagane zadne zewnetrzne encje ani czujniki. Pora roku jest
wyznaczana automatycznie na podstawie daty systemowej. Dzieki temu
integracja jest w pelni przenosna i gotowa do uzycia na dowolnej instancji
Home Assistant bez zadnej dodatkowej konfiguracji.

-------------------------------------------------------------------------------

ENCJE (per roslina)
-------------------
Dla kazdego wpisu rosliny tworzone sa nastepujace encje:

sensor.{nazwa}_watering_interval
  Aktualny zalecany interwal podlewania w dniach, na podstawie pory roku
  i grupy.

sensor.{nazwa}_last_watered
  Znacznik czasu ostatniego podlewania rosliny.
  Wartosc jest zapisywana trwale i przezywa restarty Home Assistant.

sensor.{nazwa}_status
  Aktualny status podlewania. Mozliwe wartosci:
  - OK     : Roslina zostala podlana w wymaganym interwale.
  - Podlej : Roslina wymaga podlania.

  Status aktualizuje sie codziennie o tej samej godzinie co ostatnie
  podlewanie oraz natychmiast po nacisnieciu przycisku "Podlej teraz".
  Jesli roslina nigdy nie byla podlewana, status domyslnie wynosi "Podlej".

button.{nazwa}_water_now
  Nacisnij, aby zapisac aktualny znacznik czasu jako czas ostatniego
  podlewania. Resetuje status do "OK" i planuje nastepny check statusu.

-------------------------------------------------------------------------------

ZNANE OGRANICZENIA
------------------
- Interwaly podlewania sa stale dla grupy i pory roku. Brak mozliwosci
  dostosowania interwalow per roslina bez modyfikacji kodu zrodlowego.
- Brak integracji z czujnikami wilgotnosci gleby, swiatla ani temperatury.
- Brak powiadomien push. W razie potrzeby uzyj automatyzacji Home Assistant
  opartych na encji sensor.{nazwa}_status.

-------------------------------------------------------------------------------

LICENCJA
--------
Licencja MIT. Szczegoly w pliku LICENSE.

-------------------------------------------------------------------------------
