from flask import Blueprint, render_template, request, redirect, url_for
from models.agent import lister_agents, ajouter_agent, modifier_agent, supprimer_agent, get_agent
from forms.agent_form import AgentForm

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/agents')
def liste():
    agents = lister_agents()
    return render_template('agents/liste.html', agents=agents)

@agent_bp.route('/agents/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = AgentForm()
    if form.validate_on_submit():
        ajouter_agent(
            form.nom.data,
            form.prenom.data,
            form.login.data,
            form.mdp.data,
            form.role.data
        )
        return redirect(url_for('agent.liste'))
    return render_template('agents/ajouter.html', form=form)

@agent_bp.route('/agents/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    agent = get_agent(id)
    form = AgentForm()
    if form.validate_on_submit():
        modifier_agent(
            id,
            form.nom.data,
            form.prenom.data,
            form.login.data,
            form.role.data
        )
        return redirect(url_for('agent.liste'))
    return render_template('agents/modifier.html', form=form, agent=agent)

@agent_bp.route('/agents/supprimer/<int:id>')
def supprimer(id):
    supprimer_agent(id)
    return redirect(url_for('agent.liste'))