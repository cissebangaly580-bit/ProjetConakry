from pathlib import Path

files = {
    'gestion_voyages/templates/gestion_voyages/voyage_liste.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Voyages - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Voyages</h1>
<a href="{% url 'voyage_nouveau' %}" class="btn-submit">Nouvelle offre</a>
{% if voyages %}
<table class="table">
    <thead>
        <tr><th>Destination</th><th>Date départ</th><th>Date retour</th><th>Prix</th><th>Places</th><th></th></tr>
    </thead>
    <tbody>
        {% for voyage in voyages %}
        <tr>
            <td>{{ voyage.destination }}</td>
            <td>{{ voyage.date_depart }}</td>
            <td>{{ voyage.date_retour }}</td>
            <td>{{ voyage.prix }} GNF</td>
            <td>{{ voyage.places_dispo }}</td>
            <td>
                <a href="{% url 'voyage_detail' voyage.pk %}">Voir</a> |
                <a href="{% url 'voyage_modifier' voyage.pk %}">Modifier</a> |
                <a href="{% url 'voyage_supprimer' voyage.pk %}">Supprimer</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>Aucune offre de voyage disponible.</p>
{% endif %}
{% endblock %}
''',
    'gestion_hotel/templates/gestion_hotel/chambre.liste.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Chambres - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Chambres</h1>
<a href="{% url 'chambre_nouveau' %}" class="btn-submit">Nouvelle chambre</a>
{% if chambres %}
<table class="table">
    <thead>
        <tr><th>Numéro</th><th>Type</th><th>Capacité</th><th>Prix/nuit</th><th>Statut</th><th></th></tr>
    </thead>
    <tbody>
        {% for chambre in chambres %}
        <tr>
            <td>{{ chambre.numero }}</td>
            <td>{{ chambre.get_type_chambre_display }}</td>
            <td>{{ chambre.capacite }}</td>
            <td>{{ chambre.prix_nuit }} GNF</td>
            <td>{{ chambre.get_statut_display }}</td>
            <td>
                <a href="{% url 'chambre_detail' chambre.pk %}">Voir</a> |
                <a href="{% url 'chambre_modifier' chambre.pk %}">Modifier</a> |
                <a href="{% url 'chambre_supprimer' chambre.pk %}">Supprimer</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>Aucune chambre disponible.</p>
{% endif %}
{% endblock %}
''',
    'reservations/templates/reservations/reservation_liste.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Réservations - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Réservations</h1>
<a href="{% url 'reservation_nouveau' %}" class="btn-submit">Nouvelle réservation</a>
{% if reservations %}
<table class="table">
    <thead>
        <tr><th>ID</th><th>Client</th><th>Statut</th><th>Date</th><th></th></tr>
    </thead>
    <tbody>
        {% for reservation in reservations %}
        <tr>
            <td>{{ reservation.id }}</td>
            <td>{{ reservation.client.prenom }} {{ reservation.client.nom }}</td>
            <td>{{ reservation.get_statut_display }}</td>
            <td>{{ reservation.date_reservation }}</td>
            <td>
                <a href="{% url 'reservation_detail' reservation.pk %}">Voir</a> |
                <a href="{% url 'reservation_modifier' reservation.pk %}">Modifier</a> |
                <a href="{% url 'reservation_supprimer' reservation.pk %}">Annuler</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>Aucune réservation enregistrée.</p>
{% endif %}
{% endblock %}
''',
    'facturation/templates/facturation/facture_liste.html': '''{% extends 'conakry_travel_hotel/base.html' %}

{% block title %}Factures - Conakry Travel & Hôtel{% endblock %}

{% block content %}
<h1>Factures</h1>
{% if factures %}
<table class="table">
    <thead>
        <tr><th>ID</th><th>Montant</th><th>Statut</th><th>Date</th><th></th></tr>
    </thead>
    <tbody>
        {% for facture in factures %}
        <tr>
            <td>{{ facture.id }}</td>
            <td>{{ facture.montant }} GNF</td>
            <td>{{ facture.get_statut_paiement_display }}</td>
            <td>{{ facture.date_emission }}</td>
            <td><a href="{% url 'facture_detail' facture.pk %}">Voir</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>Aucune facture générée.</p>
{% endif %}
{% endblock %}
''',
}

for rel_path, content in files.items():
    path = Path(rel_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print('written', len(files), 'templates')
