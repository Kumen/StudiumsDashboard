import os
from flask import Flask, render_template, redirect, url_for
from models import db
from database import init_db
from dash_app import init_dash_app


def create_app():
    """Flask-App-Factory-Funktion."""
    # App initialisieren
    app = Flask(__name__, instance_relative_config=True)

    # Konfiguration
    app.config.from_mapping(
        SECRET_KEY='dev',  # In Produktion ändern - ist ja nur ein Beispielprojekt, daher nicht so schlimm.
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'curriculum.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Sicherstellen, dass das Instance-Verzeichnis existiert
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Datenbank initialisieren
    db.init_app(app)

    # Datenbank mit Beispieldaten befüllen
    init_db(app)

    # Dash-App initialisieren
    init_dash_app(app)

    # Routen definieren
    @app.route('/')
    def index():
        """Startseite - leitet zum Dashboard weiter."""
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        """Dashboard-Seite - leitet zur Dash-App weiter."""
        return redirect('/dashboard/')

    @app.route('/info')
    def info():
        """Informationsseite über das Dashboard."""
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)