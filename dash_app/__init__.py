import dash
import dash_bootstrap_components as dbc
from flask import Flask
from .layout import create_layout
from .callbacks import register_callbacks


def init_dash_app(flask_app):
    """
    Initialisiert die Dash-App und registriert sie bei der Flask-App.

    Args:
        flask_app (Flask): Die Flask-App-Instance

    Returns:
        dash.Dash: Die initialisierte Dash-App
    """
    # Dash-App mit Flask-App und Bootstrap-Theme initialisieren
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        meta_tags=[
            {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
        ]
    )

    # Titel setzen
    dash_app.title = 'Studiums-Dashboard'

    # Callbacks registrieren
    register_callbacks(dash_app)

    # Layout als Funktion definieren, um es dynamisch zu laden.
    # Führt sonst zu 'RuntimeError: Working outside of application context.'
    # innerhalb der create_layout benötige ich bereits eine funktionierende FlaskApp
    # wir befinden uns noch in der Initialisierungsphase, daher kann ich dieses Verhalten in die
    # Ausführungszeit verlagern, indem ich es in einen funktionalen Aufruf kapsel (Lambda)
    dash_app.layout = lambda: create_layout(dash_app)

    return dash_app