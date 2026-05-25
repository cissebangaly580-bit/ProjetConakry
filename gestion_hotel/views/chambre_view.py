from flask import Blueprint, render_template, request, redirect, url_for
from models.chambre import lister_chambres, ajouter_chambre, modifier_chambre, supprimer_chambre, get_chambre
from forms.chambre_form import ChambreForm

chambre_bp = Blueprint('chambre', __name__)

@chambre_bp.route('/chambres')
def liste():
    chambres = lister_chambres()
    return render_template('chambres/liste.html', chambres=chambres)

@chambre_bp.route('/chambres/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = ChambreForm()
    if form.validate_on_submit():
        ajouter_chambre(
            form.numero.data,
            form.type_chambre.data,
            form.prix_nuit.data,
            form.capacite.data
        )
        return redirect(url_for('chambre.liste'))
    return render_template('chambres/ajouter.html', form=form)

@chambre_bp.route('/chambres/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    chambre = get_chambre(id)
    form = ChambreForm()
    if form.validate_on_submit():
        modifier_chambre(
            id,
            form.numero.data,
            form.type_chambre.data,
            form.prix_nuit.data,
            form.capacite.data,
            form.statut.data
        )
        return redirect(url_for('chambre.liste'))
    return render_template('chambres/modifier.html', form=form, chambre=chambre)

@chambre_bp.route('/chambres/supprimer/<int:id>')
def supprimer(id):
    supprimer_chambre(id)
    return redirect(url_for('chambre.liste'))