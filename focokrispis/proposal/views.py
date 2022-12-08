from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

import django.db.models as models

from .forms import ProposalForm
from .models import Proposal

import datetime



def have_pending_proposal(user):
    return Proposal.objects.filter(user=user, status='Pending').exists()

def get_tomorrow_date_name():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.strftime("%A")

def get_users_without_proposals():
    users = get_user_model().objects.all()
    users_without_proposals = []
    for user in users:
        if not have_pending_proposal(user):
            users_without_proposals.append(user)
    return users_without_proposals

def get_number_of_votes():
    return Proposal.objects.aggregate(models.Sum('number_of_votes'))

def get_number_of_users():
    return get_user_model().objects.count()

@login_required
def proposal_view(request):
    tomorrow = get_tomorrow_date_name()
    already_proposed = have_pending_proposal(request.user)
    if already_proposed:
        return render(request, 'proposal/new_proposal.html', {'already_proposed': already_proposed, 'new_proposal': ProposalForm(), 'tomorrow': tomorrow})

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Proposal submitted successfully')
            return redirect('proposal')
    return render(request, 'proposal/new_proposal.html', {'new_proposal': ProposalForm(), 'already_proposed': already_proposed, 'tomorrow': tomorrow})

@login_required
def show_proposals(request):
    already_voted = request.COOKIES.get('voted')
    voting_user = request.COOKIES.get('user')
    if not already_voted or (already_voted and voting_user != request.user.username):
        already_voted = False
    
    results_available = get_number_of_users() <= get_number_of_votes()['number_of_votes__sum']

    today = datetime.date.today().strftime("%Y-%m-%d" )
    tomorrow = get_tomorrow_date_name()
    proposals = Proposal.objects.filter(date__date=today)
    users_without_proposals = get_users_without_proposals()
    return render(request, 'proposal/todays_proposals.html', {'proposals': proposals, 'users_without_proposals': users_without_proposals, 'tomorrow': tomorrow, 'already_voted': already_voted, 'results_available': results_available})

@login_required
def vote(request, proposal_id):
    if request.COOKIES.get('voted') and request.COOKIES.get('user') == request.user.username:
        messages.error(request, 'You have already voted today')
        return redirect('todays_proposals')
    proposal = Proposal.objects.get(id=proposal_id)
    proposal.number_of_votes += 1
    proposal.save()
    response = redirect('todays_proposals')
    expire_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie('voted', True, expires=expire_datetime)
    response.set_cookie('user', request.user.username, expires=expire_datetime)
    return response

@login_required
def results(request):
    today = datetime.date.today().strftime("%Y-%m-%d" )
    tomorrow = get_tomorrow_date_name()
    proposals = Proposal.objects.filter(date__date=today)
    winner = proposals.order_by('-number_of_votes').first()
    return render(request, 'proposal/results.html', {'winner': winner, 'tomorrow' : tomorrow})
        

