# Studiums-Dashboard: B.Sc. Angewandte Künstliche Intelligenz

Ein interaktives Dashboard zur Visualisierung des Studienfortschritts im B.Sc. Angewandte Künstliche Intelligenz. Das Dashboard wurde mit Flask, Dash, Plotly, SQLAlchemy und SQLite entwickelt.

## Funktionen

- Übersicht über alle absolvierten, laufenden und geplanten Module
- Visualisierung des Studienfortschritts in ECTS-Punkten
- Notenentwicklung und Durchschnittsberechnung
- Modulverteilung nach Semestern
- Detaillierte Tabelle aller Module mit Filterfunktionen

## Voraussetzungen

- Python 3.12 oder höher
- pip (Python-Paketmanager)
- Virtuelle Umgebung (empfohlen)

## Installation

siehe `INSTALLATION.md`

## Datenbankinitialisierung

Die Anwendung initialisiert automatisch eine SQLite-Datenbank mit Beispieldaten aus dem Studienablaufplan der IU für den B.Sc. Angewandte Künstliche Intelligenz. Die Datenbank wird im `instance`-Verzeichnis unter dem Namen `curriculum.db` erstellt.

## Anpassung

Um das Dashboard an einen anderen Studiengang anzupassen, können die Modelldaten in `database.py` geändert werden. Die Struktur der Datenbank und das Dashboard-Layout sind flexibel genug, um verschiedene Studiengänge abzubilden.

## Weitere Überlegungen

Das ist nur ein Proof of Concept. In der finalen Version, welche ich tatsächlich plane, für mich selbst fertigzustellen würden noch folgende Features implementiert werden

- Dialoge zum Hinzufügen anderer Studiengänge über die UI
- Dialoge zum Hinzufügen, Bearbeiten und Entfernen von Modulen eines Studenten
- Berechnung der erforderlichen Prüfungsleistung um eine gegebene Abschlussnote zu erreichen
- Verwaltung für mehrere Studenten
- Login und OAuth Anbindung für meine Infrastruktur (HomeLab)
- weiteres tbd.