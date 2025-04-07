from models import db, Modul, Wahlpflichtbereich, Student, StudentFortschritt
from datetime import datetime, date, timedelta
import random

studenten_name = "Pascal Brieger"
matrikel_nummer = "IU14711293"
studien_beginn = datetime(2024, 5, 1)

def create_tables():
    """Erstellt alle Tabellen in der Datenbank."""
    db.create_all()
    print("Datenbanktabellen wurden erstellt.")


def seed_modules():
    """Befüllt die Datenbank mit den Modulen aus dem Studienablaufplan."""

    # Überprüfen, ob Daten bereits existieren
    if Modul.query.count() > 0:
        print("Module bereits in der Datenbank vorhanden.")
        return

    # Liste der Module aus dem Studienablaufplan
    # Semester empfohlen richtet sich hier nach dem Teilzeitmodel 1 (TZ1), 4 Jahre.
    # Entnommen aus dem PDF: sap_ba_angewandte_kuenstliche_intelligence_180_FS_BAAKI_de_fs_yqt3ld.pdf
    # siehe Ordner "resources"
    module_data = [
        # 1. Semester
        {"kurscode": "DLBDSEAIS01_D", "name": "Artificial Intelligence", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 1},
        {"kurscode": "DLBWIRITT01", "name": "Einführung in das wissenschaftliche Arbeiten für IT und Technik",
         "ects": 5, "pruefungsform": "Advanced Workbook", "semester_empfohlen": 1},
        {"kurscode": "DLBDSIPWP01_D", "name": "Einführung in die Programmierung mit Python", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 1},
        {"kurscode": "DLBBIMD01", "name": "Mathematik: Analysis", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 1},
        {"kurscode": "DLBKA01", "name": "Kollaboratives Arbeiten", "ects": 5, "pruefungsform": "Fachpräsentation",
         "semester_empfohlen": 1},

        # 2. Semester
        {"kurscode": "DLBDSSPDS01_D", "name": "Statistik - Wahrscheinlichkeit und deskriptive Statistik", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 2},
        {"kurscode": "DLBDSOOFPP01_D", "name": "Objektorientierte und funktionale Programmierung mit Python", "ects": 5,
         "pruefungsform": "Portfolio", "semester_empfohlen": 2},
        {"kurscode": "DLBBIM01", "name": "Mathematik: Lineare Algebra", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 2},
        {"kurscode": "DLBIHK01", "name": "Interkulturelle und ethische Handlungskompetenz", "ects": 5,
         "pruefungsform": "Fallstudie", "semester_empfohlen": 2},

        # 3. Semester
        {"kurscode": "DLBDSSIS01_D", "name": "Statistik - Induktive Statistik", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 3},
        {"kurscode": "DLBDSCC01_D", "name": "Cloud Computing", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 3},
        {"kurscode": "DLBSEPCP01_D", "name": "Projekt: Cloud Programming", "ects": 5, "pruefungsform": "Portfolio",
         "semester_empfohlen": 3},
        {"kurscode": "DLBDSMLSL01_D", "name": "Maschinelles Lernen - Supervised Learning", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 3},
        {"kurscode": "DLBDSMLUSL01_D", "name": "Maschinelles Lernen - Unsupervised Learning und Feature Engineering",
         "ects": 5, "pruefungsform": "Fallstudie", "semester_empfohlen": 3},

        # 4. Semester
        {"kurscode": "DLBDSNNDL01_D", "name": "Neuronale Netze und Deep Learning", "ects": 5,
         "pruefungsform": "Fachpräsentation", "semester_empfohlen": 4},
        {"kurscode": "DLBAIICV01_D", "name": "Einführung in Computer Vision", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 4},
        {"kurscode": "DLBAIPCV01_D", "name": "Projekt: Computer Vision", "ects": 5, "pruefungsform": "Projektbericht",
         "semester_empfohlen": 4},
        {"kurscode": "DLBAIIRL01_D", "name": "Einführung in das Reinforcement Learning", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 4},

        # 5. Semester
        {"kurscode": "DLBAIINLP01_D", "name": "Einführung in NLP", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 5},
        {"kurscode": "DLBAIPNLP01_D", "name": "Projekt: NLP", "ects": 5, "pruefungsform": "Projektbericht",
         "semester_empfohlen": 5},
        {"kurscode": "DLBISIC01", "name": "Einführung in Datenschutz und IT-Sicherheit", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 5},
        {"kurscode": "DLBDSDSSE01_D", "name": "Data Science Software Engineering", "ects": 5,
         "pruefungsform": "Klausur", "semester_empfohlen": 5},
        {"kurscode": "DLBDSMTP01_D", "name": "Projekt: Vom Modell zum Produktivsystem", "ects": 5,
         "pruefungsform": "Projektpräsentation", "semester_empfohlen": 5},

        # 6. Semester
        {"kurscode": "DLBDSSECDS01_D", "name": "Seminar: Ethische Fragen der Data Science", "ects": 5,
         "pruefungsform": "Seminararbeit", "semester_empfohlen": 6},
        {"kurscode": "DLBMIUEX01", "name": "User Experience", "ects": 5, "pruefungsform": "Klausur",
         "semester_empfohlen": 6},
        {"kurscode": "DLBMIUEX02", "name": "UX-Projekt", "ects": 5, "pruefungsform": "Projektbericht",
         "semester_empfohlen": 6},
        {"kurscode": "DLBAIPEAI01_D", "name": "Projekt: Edge AI", "ects": 5, "pruefungsform": "Projektbericht",
         "semester_empfohlen": 6},
        {"kurscode": "DLBROIR01_D", "name": "Einführung in die Robotik", "ects": 5, "pruefungsform": "Hausarbeit",
         "semester_empfohlen": 6},

        # 7. Semester
        {"kurscode": "DLBDBAPM01", "name": "Projekt: Agiles Projektmanagement", "ects": 5,
         "pruefungsform": "Projektbericht", "semester_empfohlen": 7},

        # 7.-8. Semester (Wahlpflichtmodule werden separat hinzugefügt)

        # 8. Semester
        # aus der Bachelorarbeit habe ich zwei einzelne Module gemacht,
        # was nicht ganz korrekt ist, aber ein besseres Tracking erlaubt
        {"kurscode": "BBAK01", "name": "Bachelorarbeit", "ects": 9, "pruefungsform": "Bachelorarbeit",
         "semester_empfohlen": 8},
        {"kurscode": "BBAK02", "name": "Kolloquium", "ects": 1, "pruefungsform": "Prüfung mündlich",
         "semester_empfohlen": 8}
    ]

    # Module in die Datenbank einfügen
    for modul_info in module_data:
        modul = Modul(**modul_info)
        db.session.add(modul)

    db.session.commit()
    print(f"{len(module_data)} Module wurden in die Datenbank eingefügt.")


def seed_wahlpflichtbereiche():
    """Befüllt die Datenbank mit den Wahlpflichtbereichen."""

    # Überprüfen, ob Daten bereits existieren
    if Wahlpflichtbereich.query.count() > 0:
        print("Wahlpflichtbereiche bereits in der Datenbank vorhanden.")
        return

    # Wahlpflichtbereiche aus dem Studienablaufplan
    wahlpflichtbereiche_data = [
        {
            "name": "Wahlpflichtbereich A",
            "beschreibung": "Spezialisierungsbereich A mit 10 ECTS",
            "ects": 10,
            "module_namen": [
                "Autonomous Driving",
                "Robotics und Automatisierung",
                "Data Engineer",
                "Digitale Signalverarbeitung und Sensortechnologie",
                "Datenbankentwickler",
                "Business Intelligence",
                "Data Analyst",
                "Augmented, Mixed und Virtual Reality"
            ]
        },
        {
            "name": "Wahlpflichtbereich B",
            "beschreibung": "Spezialisierungsbereich B mit 10 ECTS",
            "ects": 10,
            "module_namen": [
                "Internationales Marketing und Branding",
                "Angewandter Vertrieb",
                "Supply Chain Management",
                "IT-Projekt- und -Architekturmanagement",
                "Psychologie der Mensch-Computer-Interaktion"
            ]
        },
        {
            "name": "Wahlpflichtbereich C",
            "beschreibung": "Spezialisierungsbereich C mit 10 ECTS",
            "ects": 10,
            "module_namen": [
                "Autonomous Driving",
                "Robotics und Automatisierung",
                "Data Engineer",
                "Digitale Signalverarbeitung und Sensortechnologie",
                "Datenbankentwickler",
                "Business Intelligence",
                "Data Analyst",
                "Augmented, Mixed und Virtual Reality",
                "Internationales Marketing und Branding",
                "Angewandter Vertrieb",
                "Supply Chain Management",
                "IT-Projekt- und -Architekturmanagement",
                "Psychologie der Mensch-Computer-Interaktion",
                "Fremdsprache Italienisch",
                "Fremdsprache Französisch",
                "Fremdsprache Spanisch",
                "Fremdsprache Englisch",
                "Studium Generale",
                "Microsoft ERP - Dynamics 365 Business Central - Functional Consultant",
                "SAP - SAP S/4HANA Business Process Integration - Application Associate",
                "Karriere-Entwicklung"
            ]
        }
    ]

    # Dictionary zum Speichern der erstellten Module
    erstellte_module = {}

    # Erstelle zuerst alle Module für alle Wahlpflichtbereiche
    alle_modulnamen = set()
    for wpb_info in wahlpflichtbereiche_data:
        for name in wpb_info["module_namen"]:
            alle_modulnamen.add(name)

    # Module erstellen und in die Datenbank einfügen
    for modul_name in alle_modulnamen:
        # Prüfen, ob das Modul bereits existiert
        modul = Modul.query.filter_by(name=modul_name).first()
        if not modul:
            # Eindeutigen Kurscode generieren
            base_kurscode = f"WPB-{modul_name.replace(' ', '-')[:12]}"
            kurscode = base_kurscode
            counter = 1

            while Modul.query.filter_by(kurscode=kurscode).first() is not None:
                kurscode = f"{base_kurscode}-{counter}"
                counter += 1

            # Neues Modul erstellen
            modul = Modul(
                kurscode=kurscode,
                name=modul_name,
                ects=10,  # Wahlpflichtmodule haben typischerweise 10 ECTS
                pruefungsform="Variiert",
                semester_empfohlen=7  # Wahlpflichtmodule beginnen typischerweise im 7. Semester
            )
            db.session.add(modul)

        # Modul im Dictionary speichern
        erstellte_module[modul_name] = modul

    # Änderungen speichern, damit alle Module IDs haben
    db.session.flush()

    # Jetzt Wahlpflichtbereiche erstellen und Module zuordnen
    for wpb_info in wahlpflichtbereiche_data:
        module_namen = wpb_info.pop("module_namen")
        wpb = Wahlpflichtbereich(**wpb_info)
        db.session.add(wpb)

        # Flush, um sicherzustellen, dass der Wahlpflichtbereich eine ID hat
        db.session.flush()

        # Module dem Wahlpflichtbereich zuordnen
        for modul_name in module_namen:
            modul = erstellte_module.get(modul_name)
            if modul:
                wpb.module.append(modul)

    # Änderungen in die Datenbank schreiben
    db.session.commit()
    print(f"{len(wahlpflichtbereiche_data)} Wahlpflichtbereiche wurden in die Datenbank eingefügt.")


def seed_example_student():
    """
    Erstellt einen Beispielstudenten mit Fortschritten für das Dashboard.
    In diesem Fall mich selbst: Pascal Brieger, Beginn: 2024-05-01, Regelstudienzeit: 4 Jahre.
    """

    # Überprüfen, ob bereits ein Beispielstudent existiert
    if Student.query.filter_by(name=studenten_name).first():
        print("Beispielstudent bereits in der Datenbank vorhanden.")
        return

    # Beispielstudent erstellen
    student = Student(
        name=studenten_name,
        matrikelnummer=matrikel_nummer,
        studiengang="B.Sc. Angewandte Künstliche Intelligenz",
        studienbeginn=studien_beginn,
        regelstudienzeit=8  # 4 Jahre, angegeben in Semestern
    )
    db.session.add(student)
    db.session.commit()

    # Erstellen von Beispiel Modulen. Logik wie folgt
    # - alle Module aus aktuelles_semester-1 erfolgreich absolviert
    # - alle Module aus aktuelles_semester per Zufall 'Bestanden' oder 'In Bearbeitung'
    # - alle Module aktuelles_semester+1 geplant
    # - rest ignorieren...
    aktuelles_semester = student.aktuelles_semester
    module = Modul.query.filter(Modul.semester_empfohlen <= aktuelles_semester + 1).all()

    for modul in module:
        # Status basierend auf dem empfohlenen Semester festlegen
        if modul.semester_empfohlen < aktuelles_semester:
            status = "Bestanden"
            note = round(random.uniform(1.0, 3.0), 1)  # Zufällige Note zwischen 1.0 und 3.0,

            # Mir ist bewusst die IU erlaubt eine recht freie Einteilung / Selbstgestaltung
            # hiermit versuche ich die Beispieldaten so gut wie Möglich plausibel zu halten

            # Wie viele Tage sind vergangen, seitdem das Studium begonnen hat.
            # Bsp: das Modul is im 3. Semester. Also müssen ca 2*180 Tage vergangen sein
            # um dieses Modul belegen zu können
            tage_seit_studien_beginn = (modul.semester_empfohlen - 1) * 180

            # Random Anzahl an Tagen in diesem Semester
            # dient als, Addition zum Studienbeginn um ein Prüfungsdatum zu erzeugen
            tage_in_diesem_semester = random.randint(20, 150)

            tage = tage_seit_studien_beginn + tage_in_diesem_semester
            datum = studien_beginn + timedelta(days=tage)

        elif modul.semester_empfohlen == aktuelles_semester:
            # etwas mehr entropie in die choice bringen.
            # Sonst kommt es recht häufig vor, dass alles 'Bestanden' oder 'In Bearbeitung' ist.
            status = random.choice(["Bestanden", "In Bearbeitung", "In Bearbeitung", "Bestanden",
                                    "Bestanden", "In Bearbeitung", "In Bearbeitung", "Bestanden"])

            # vergebe eine zufällige Note, wenn das Modul den Status "Bestanden" hat.
            note = round(random.uniform(1.0, 3.0), 1) if status == "Bestanden" else None

            # vergebe ein zufälliges Datum, wenn das Modul den Status "Bestanden" hat.
            datum = date.today() - timedelta(days=random.randint(0, 120)) if status == "Bestanden" else None

        else:
            status = "Geplant"
            note = None
            datum = None

        # das ist dein Kurs: Objektorientierte und funktionale Programmierung mit Python
        # kleines Easter-Egg :P hoffentlich wird das meine Note ;)
        # Note: 1+
        # Status: Bestanden, natürlich!
        # Datum: Heute :D
        if modul.kurscode == "DLBDSOOFPP01_D":
            # schummeln ist erlaubt, getreu dem Motto: Traue keiner Statistik, die du nicht selbst gefälscht hast.
            note = 1
            status = "Bestanden"
            datum = date.today()

        fortschritt = StudentFortschritt(
            student_id=student.id,
            modul_id=modul.id,
            status=status,
            semester_belegt=modul.semester_empfohlen,
            note=note,
            datum_abgeschlossen=datum
        )
        db.session.add(fortschritt)

    # Wahlpflichtfächer gibt es erst ab Semester 7
    # da ich nicht im 7ten Semester bin, ignoriere ich diesen Umstand

    db.session.commit()
    print(f"Beispielstudent 'Pascal Brieger' mit Fortschritten wurde erstellt.")


def init_db(app):
    """Initialisiert die Datenbank mit dem Flask-App-Kontext."""
    with app.app_context():
        create_tables()
        seed_modules()
        seed_wahlpflichtbereiche()
        seed_example_student()
        print("Datenbankinitialisierung abgeschlossen.")


if __name__ == "__main__":
    # Dieses Skript kann zum Testen direkt ausgeführt werden, um die Datenbank zu initialisieren
    from app import create_app

    app = create_app()
    init_db(app)