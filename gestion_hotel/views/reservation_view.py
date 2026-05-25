from flask import Blueprint, render_template, redirect, url_for
from models.reservation import lister_reservations, ajouter_reservation, modifier_reservation, supprimer_reservation, get_reservation
from models.client import lister_clients
from models.agent import lister_agents
from forms.reservation_form import ReservationForm

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservations')
def liste():
    reservations = lister_reservations()
    return render_template('reservations/liste.html', reservations=reservations)

@reservation_bp.route('/reservations/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = ReservationForm()
    clients = lister_clients()
    agents = lister_agents()
    form.client_id.choices = [(c[0], c[1]+' '+c[2]) for c in clients]
    form.agent_id.choices = [(a[0], a[1]+' '+a[2]) for a in agents]
    if form.validate_on_submit():
        ajouter_reservation(form.client_id.data, form.agent_id.data)
        return redirect(url_for('reservation.liste'))
    return render_template('reservations/ajouter.html', form=form)

@reservation_bp.route('/reservations/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    reservation = get_reservation(id)
    form = ReservationForm()
    clients = lister_clients()
    agents = lister_agents()
    form.client_id.choices = [(c[0], c[1]+' '+c[2]) for c in clients]
    form.agent_id.choices = [(a[0], a[1]+' '+a[2]) for a in agents]
    if form.validate_on_submit():
        modifier_reservation(id, form.statut.data)
        return redirect(url_for('reservation.liste'))
    return render_template('reservations/modifier.html', form=form, reservation=reservation)

@reservation_bp.route('/reservations/supprimer/<int:id>')
def supprimer(id):
    supprimer_reservation(id)
    return redirect(url_for('reservation.liste'))