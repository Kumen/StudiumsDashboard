import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash import html, dcc, dash_table
from database import studenten_name
from flask import current_app
from models import Student, StudentFortschritt


def create_layout(app):
    """Erstellt das Layout für die Dash-Anwendung."""

    # erst stellen wir sicher, dass wir alle notwendigen Informationen zusammen getragen haben,
    # die wir zu Anzeige bringen wollen.

    # Anwendungskontext sicherstellen
    with current_app.app_context():
        # Beispielstudent abrufen - It's me Mario, ähhh Pascal...
        student = Student.query.filter_by(name=studenten_name).first()

        if not student:
            return html.Div(
                "Keine Studentendaten vorhanden. Bitte stelle sicher, dass die Datenbank initialisiert wurde.")

        # Fortschrittsdaten sammeln
        fortschritte = StudentFortschritt.query.filter_by(student_id=student.id).all()
        module_data = []

        for fortschritt in fortschritte:
            modul = fortschritt.modul
            module_data.append({
                'Modul': modul.name,
                'Kurscode': modul.kurscode,
                'ECTS': modul.ects,
                'Semester': modul.semester_empfohlen,
                'Prüfungsform': modul.pruefungsform,
                'Status': fortschritt.status,
                'Note': fortschritt.note,
                'Abgeschlossen': fortschritt.datum_abgeschlossen
            })

        df_module = pd.DataFrame(module_data)

        # Allgemeine Daten berechnen
        ects_gesamt = 180
        ects_bestanden = df_module[df_module['Status'] == 'Bestanden']['ECTS'].sum()
        ects_in_bearbeitung = df_module[df_module['Status'] == 'In Bearbeitung']['ECTS'].sum()
        ects_geplant = ects_gesamt - ects_bestanden - ects_in_bearbeitung

    # ECTS pro Semester berechnen
    df_ects_pro_semester = df_module.groupby('Semester')['ECTS'].sum().reset_index()
    df_ects_pro_semester['Semester'] = df_ects_pro_semester['Semester'].astype(str)

    # ECTS-Fortschritt berechnen
    ects_fortschritt = [
        {'Status': 'Bestanden', 'ECTS': ects_bestanden},
        {'Status': 'In Bearbeitung', 'ECTS': ects_in_bearbeitung},
        {'Status': 'Geplant', 'ECTS': ects_geplant}
    ]
    df_ects_fortschritt = pd.DataFrame(ects_fortschritt)

    # Notenverteilung
    df_noten = df_module.dropna(subset=['Note'])

    return create_html_layout(df_ects_fortschritt, df_ects_pro_semester, df_module, df_noten, ects_bestanden,
                                ects_gesamt, ects_in_bearbeitung, student)


def create_html_layout(df_ects_fortschritt, df_ects_pro_semester, df_module, df_noten, ects_bestanden, ects_gesamt,
                       ects_in_bearbeitung, student):
    return html.Div([
        # Header mit Studiengangs-Info
        create_html_header(student),

        # Kennzahlen-Karten
        dbc.Row([
            # Aktuelles Semester
            create_current_semester_card(student),

            # ECTS-Fortschritt
            create_ects_progress_card(ects_bestanden, ects_gesamt, ects_in_bearbeitung, student),

            # Notendurchschnitt
            create_notendurchschnitt_card(student),

            # Zeitlicher Fortschritt
            create_time_progress_card(student)
        ], className="stats-row"),

        # Diagramme
        dbc.Row([
            # ECTS-Fortschritt
            create_ects_pie_graph(df_ects_fortschritt),

            # ECTS pro Semester
            create_ects_bar_graph(df_ects_pro_semester)
        ], className="charts-row"),

        # Weitere Diagramme
        dbc.Row([
            # Notenverteilung
            create_noten_histogramm(df_noten),

            # Modulstatus
            create_modul_bar_graph(df_module)
        ], className="charts-row"),

        # Modultabelle
        dbc.Row([
            create_modul_table(df_module)
        ], className="table-row"),

        # Footer mit Credits
        dbc.Row([
            dbc.Col([
                html.P(
                    "Dashboard für B.Sc. Angewandte Künstliche Intelligenz | Daten basierend auf dem Studienablaufplan der IU",
                    className="text-center text-muted mt-4")
            ], width=12)
        ])
    ], className="dashboard-container")


def create_modul_table(df_module):
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader("Modulübersicht"),
            dbc.CardBody([
                # Filtersteuerelemente
                html.Div([
                    html.Label("Semester-Filter: ", className="mr-2"),
                    dcc.Dropdown(
                        id='semester-filter',
                        options=[
                                    {'label': 'Alle Semester', 'value': 'Alle'}
                                ] + [
                                    {'label': f'Semester {sem}', 'value': sem}
                                    for sem in sorted(df_module['Semester'].unique())
                                ],
                        value='Alle',
                        className="mb-3",
                        style={'width': '250px'}
                    )
                ], className="mb-3"),
                dash_table.DataTable(
                    id='module-table',
                    columns=[
                        {'name': 'Modul', 'id': 'Modul', 'type': 'text'},
                        {'name': 'Kurscode', 'id': 'Kurscode', 'type': 'text'},
                        {'name': 'ECTS', 'id': 'ECTS', 'type': 'numeric'},
                        {'name': 'Semester', 'id': 'Semester', 'type': 'numeric'},
                        {'name': 'Prüfungsform', 'id': 'Prüfungsform', 'type': 'text'},
                        {'name': 'Status', 'id': 'Status', 'type': 'text'},
                        {'name': 'Note', 'id': 'Note', 'type': 'numeric'},
                        {'name': 'Abgeschlossen', 'id': 'Abgeschlossen_fmt', 'type': 'text'},
                    ],
                    data=[
                        {
                            **row,
                            # String-Konvertierung für Anzeige, aber Typ-Erhaltung für Filterung
                            'ECTS': row['ECTS'],
                            'Semester': row['Semester'],
                            'Note': row['Note'] if pd.notna(row['Note']) else None,
                            'Abgeschlossen_fmt': row['Abgeschlossen'].strftime('%d.%m.%Y') if pd.notna(
                                row['Abgeschlossen']) else ''
                        }
                        for row in df_module.sort_values('Semester').to_dict('records')
                    ],
                    filter_action='native',  # Wichtig für Filterung
                    sort_action='native',
                    sort_mode='multi',
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Status} = "Bestanden"'},
                            'backgroundColor': '#d4edda',
                            'color': '#155724'
                        },
                        {
                            'if': {'filter_query': '{Status} = "In Bearbeitung"'},
                            'backgroundColor': '#fff3cd',
                            'color': '#856404'
                        },
                        {
                            'if': {'filter_query': '{Status} = "Geplant"'},
                            'backgroundColor': '#f8f9fa',
                            'color': '#6c757d'
                        }
                    ],
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },
                    page_size=99,  # will immer alles sehen... und ja leider der einzige Weg -.-''
                    filter_options={'case': 'insensitive'},
                    # Macht Filterung nicht abhängig von Groß-/Kleinschreibung
                    style_table={'overflowX': 'auto'}
                )
            ])
        ], className="dashboard-card")
    ], width=12)


def create_modul_bar_graph(df_module):
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader("Modulstatus"),
            dbc.CardBody([
                dcc.Graph(
                    id='modulstatus-graph',
                    figure=px.bar(
                        df_module.groupby('Status').size().reset_index(name='Anzahl'),
                        x='Status',
                        y='Anzahl',
                        text='Anzahl',
                        color='Status',
                        color_discrete_map={
                            'Bestanden': '#28a745',
                            'In Bearbeitung': '#ffc107',
                            'Geplant': '#6c757d'
                        }
                    ).update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        xaxis_title="Status",
                        yaxis_title="Anzahl Module"
                    ).update_traces(
                        texttemplate='%{text}',
                        textposition='outside'
                    )
                )
            ])
        ], className="dashboard-card")
    ], width=6)


def create_noten_histogramm(df_noten):
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader("Notenverteilung"),
            dbc.CardBody([
                dcc.Graph(
                    id='noten-graph',
                    figure=px.histogram(
                        df_noten,
                        x='Note',
                        nbins=10,
                        range_x=[1.0, 4.0],
                        color_discrete_sequence=['#6f42c1']
                    ).update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        xaxis_title="Note",
                        yaxis_title="Anzahl Module"
                    )
                )
            ])
        ], className="dashboard-card")
    ], width=6)


def create_ects_bar_graph(df_ects_pro_semester):
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader("ECTS pro Semester"),
            dbc.CardBody([
                dcc.Graph(
                    id='ects-pro-semester-graph',
                    figure=px.bar(
                        df_ects_pro_semester,
                        x='Semester',
                        y='ECTS',
                        text='ECTS',
                        color_discrete_sequence=['#17a2b8']
                    ).update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        xaxis_title="Semester",
                        yaxis_title="ECTS"
                    ).update_traces(
                        texttemplate='%{text}',
                        textposition='outside'
                    )
                )
            ])
        ], className="dashboard-card")
    ], width=6)


def create_ects_pie_graph(df_ects_fortschritt):
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader("ECTS-Fortschritt"),
            dbc.CardBody([
                dcc.Graph(
                    id='ects-fortschritt-graph',
                    figure=px.pie(
                        df_ects_fortschritt,
                        values='ECTS',
                        names='Status',
                        hole=0.3,
                        color='Status',
                        color_discrete_map={
                            'Bestanden': '#28a745',
                            'In Bearbeitung': '#ffc107',
                            'Geplant': '#6c757d'
                        }
                    ).update_layout(
                        margin=dict(l=20, r=20, t=30, b=20),
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
                    )
                )
            ])
        ], className="dashboard-card")
    ], width=6)


def create_time_progress_card(student):
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Zeitlicher Fortschritt", className="card-title"),
                html.H2(
                    f"{min(100, round(student.aktuelles_semester / student.regelstudienzeit * 100, 1))}%",
                    className="card-value"
                ),
                html.P(f"Studienbeginn: {student.studienbeginn.strftime('%d.%m.%Y')}",
                       className="card-subtitle")
            ])
        ], className="dashboard-card")
    ], width=3)


def create_notendurchschnitt_card(student):
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Notendurchschnitt", className="card-title"),
                html.H2(
                    f"{student.notendurchschnitt:.2f}" if student.notendurchschnitt else "N/A",
                    className="card-value"
                ),
                html.P("Gewichteter Durchschnitt (nach ECTS)",
                       className="card-subtitle")
            ])
        ], className="dashboard-card")
    ], width=3)


def create_ects_progress_card(ects_bestanden, ects_gesamt, ects_in_bearbeitung, student):
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("ECTS-Fortschritt", className="card-title"),
                html.H2(f"{ects_bestanden} / {ects_gesamt} ECTS", className="card-value"),
                dbc.Progress(
                    value=student.gesamtfortschritt,
                    label=f"{student.gesamtfortschritt}%",
                    color="success",
                    className="mb-2"
                ),
                html.P(f"{ects_in_bearbeitung} ECTS in Bearbeitung",
                       className="card-subtitle")
            ])
        ], className="dashboard-card")
    ], width=3)


def create_current_semester_card(student):
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Aktuelles Semester", className="card-title"),
                html.H2(f"{student.aktuelles_semester}. Semester", className="card-value"),
                html.P(f"von {student.regelstudienzeit} Semestern (Regelstudienzeit)",
                       className="card-subtitle")
            ])
        ], className="dashboard-card")
    ], width=3)


def create_html_header(student):
    return dbc.Row([
        dbc.Col([
            html.H1("Studiums-Dashboard: B.Sc. Angewandte Künstliche Intelligenz",
                    className="dashboard-title"),
            html.H4(f"Student: {student.name} (Matrikelnr. {student.matrikelnummer})",
                    className="dashboard-subtitle")
        ], width=12)
    ], className="header-row")