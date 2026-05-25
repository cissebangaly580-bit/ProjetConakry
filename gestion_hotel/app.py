from flask import Flask, render_template
from views.chambre_view import chambre_bp
from views.client_view import client_bp
from views.agent_view import agent_bp
from views.reservation_view import reservation_bp
from views.facture_view import facture_bp
from views.voyage_view import voyage_bp

app = Flask(__name__)
app.secret_key = 'conakry2026'

# Enregistrement des blueprints
app.register_blueprint(chambre_bp)
app.register_blueprint(client_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(facture_bp)
app.register_blueprint(voyage_bp)

@app.route('/')
def accueil():
    return render_template('accueil.html')
@app.route('/quitter')
def quitter():
    return "<h2 style='text-align:center; margin-top:100px;'>👋 Au revoir ! Fermez cet onglet pour quitter.</h2>"
if __name__ == '__main__':
    app.run(debug=True)