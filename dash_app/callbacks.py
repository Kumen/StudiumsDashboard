from dash import Input, Output
from database import studenten_name
from flask import current_app
from models import Student, StudentFortschritt


def register_callbacks(dash_app):
    """Registriert Callbacks für die Dash-Anwendung."""

    @dash_app.callback(
        Output('module-table', 'data'),
        [Input('semester-filter', 'value')]
    )
    def update_table(selected_semester):
        """Aktualisiert die Modultabelle basierend auf dem ausgewählten Semester."""
        with current_app.app_context():
            student = Student.query.filter_by(name=studenten_name).first()

            if not student:
                return []

            # Fortschritte abrufen
            fortschritte = StudentFortschritt.query.filter_by(student_id=student.id).all()
            module_data = []

            for fortschritt in fortschritte:
                modul = fortschritt.modul

                # Semester filtern, wenn ausgewählt
                if selected_semester and selected_semester != "Alle" and modul.semester_empfohlen != int(
                        selected_semester):
                    continue

                module_data.append({
                    'Modul': modul.name,
                    'Kurscode': modul.kurscode,
                    'ECTS': modul.ects,
                    'Semester': modul.semester_empfohlen,
                    'Prüfungsform': modul.pruefungsform,
                    'Status': fortschritt.status,
                    'Note': fortschritt.note,
                    'Abgeschlossen_fmt': fortschritt.datum_abgeschlossen.strftime(
                        '%d.%m.%Y') if fortschritt.datum_abgeschlossen else ''
                })

            # Nach Semester sortieren
            module_data = sorted(module_data, key=lambda x: x['Semester'])

            return module_data

    return dash_app