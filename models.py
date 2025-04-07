import math

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# M zu N Relationstabelle für Module in Wahlpflichtbereichen
module_wahlpflichtbereich = db.Table(
    'module_wahlpflichtbereich',
    db.Column('modul_id', db.Integer, db.ForeignKey('modul.id'), primary_key=True),
    db.Column('wahlpflichtbereich_id', db.Integer, db.ForeignKey('wahlpflichtbereich.id'), primary_key=True)
)


class Modul(db.Model):
    """Modell für ein Modul im Studiengang."""
    id = db.Column(db.Integer, primary_key=True)
    kurscode = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ects = db.Column(db.Integer, nullable=False)
    pruefungsform = db.Column(db.String(50), nullable=False)
    semester_empfohlen = db.Column(db.Integer, nullable=False)

    # Beziehungen
    student_fortschritte = db.relationship('StudentFortschritt', backref='modul', lazy=False)

    # Beziehung zu Wahlpflichtbereichen
    wahlpflichtbereiche = db.relationship(
        'Wahlpflichtbereich',
        secondary=module_wahlpflichtbereich,
        back_populates='module'
    )

    def __repr__(self):
        return f'<Modul {self.kurscode}: {self.name}>'


class Wahlpflichtbereich(db.Model):
    """Modell für einen Wahlpflichtbereich."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    beschreibung = db.Column(db.Text, nullable=True)
    ects = db.Column(db.Integer, nullable=False, default=10)  # Standardmäßig 10 ECTS

    # Beziehung zu Modulen
    module = db.relationship(
        'Modul',
        secondary=module_wahlpflichtbereich,
        back_populates='wahlpflichtbereiche'
    )

    def __repr__(self):
        return f'<Wahlpflichtbereich {self.name}>'


# noinspection PyTypeChecker
class Student(db.Model):
    """Modell für einen Studenten."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    matrikelnummer = db.Column(db.String(10), unique=True, nullable=False)
    studiengang = db.Column(db.String(100), nullable=False, default='B.Sc. Angewandte Künstliche Intelligenz')
    studienbeginn = db.Column(db.Date, nullable=False)
    regelstudienzeit = db.Column(db.Integer, nullable=False, default=6)  # In Semestern (beispiel VZ=6, TZ1=8, TZ2=12)

    # Beziehungen
    fortschritte = db.relationship('StudentFortschritt', backref='student', lazy=False)

    def __repr__(self):
        return f'<Student {self.matrikelnummer}: {self.name}>'

    @property
    def aktuelles_semester(self):
        """Berechnet das aktuelle Semester basierend auf dem Studienbeginn."""
        heute = datetime.now().date()
        monate_seit_beginn = (heute - self.studienbeginn).days // 30
        semester = math.ceil(monate_seit_beginn / 6)

        return max(1, semester)

    @property
    def gesamtfortschritt(self):
        """Berechnet den Gesamtfortschritt in Prozent."""
        abgeschlossene_ects = sum([f.modul.ects for f in self.fortschritte if f.status == 'Bestanden'])
        return round((abgeschlossene_ects / 180) * 100, 1)  # 180 ECTS insgesamt

    @property
    def notendurchschnitt(self):
        """Berechnet den Notendurchschnitt."""
        benotete_fortschritte = [f for f in self.fortschritte if f.note is not None]
        if not benotete_fortschritte:
            return None

        summe_gewichtet = sum([f.note * f.modul.ects for f in benotete_fortschritte])
        summe_ects = sum([f.modul.ects for f in benotete_fortschritte])

        return round(summe_gewichtet / summe_ects, 2) if summe_ects > 0 else None


class StudentFortschritt(db.Model):
    """Modell für den Fortschritt eines Studenten in einem Modul."""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    modul_id = db.Column(db.Integer, db.ForeignKey('modul.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Geplant')  # Geplant, In Bearbeitung, Bestanden
    semester_belegt = db.Column(db.Integer, nullable=True)
    note = db.Column(db.Float, nullable=True)
    datum_abgeschlossen = db.Column(db.Date, nullable=True)

    def __repr__(self):
        status_text = f", Note: {self.note}" if self.note else ""
        return f'<Fortschritt {self.student.name} - {self.modul.name}: {self.status}{status_text}>'