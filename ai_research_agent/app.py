from flask import Flask, render_template, redirect, url_for, g
import os
from config import Config
import database

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Initialize SQLite database
    database.init_app(app)

    # Register Blueprints
    from routes import auth, dashboard, agent
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(agent.bp)

    # Root landing page route
    @app.route('/')
    def landing():
        if g.user:
            return redirect(url_for('dashboard.index'))
        return render_template('landing.html')

    return app

app = create_app()

if __name__ == '__main__':
    # Run server
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
