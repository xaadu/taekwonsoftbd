import os

from django.shortcuts import render, redirect
from django.contrib import messages

from account.decorators import allowed_users
from host.models import Event, PlayerResult

from .forms import JudgeUpdateForm, MarkingForm

# Create your views here.


@allowed_users(['judge'])
def dashboard(request):
    pic_url = request.user.get_prof_pic_url()
    as_judge_1 = request.user.judgemodel.Judge1.all()
    as_judge_2 = request.user.judgemodel.Judge2.all()
    as_judge_3 = request.user.judgemodel.Judge3.all()
    total_events = list(as_judge_1)+list(as_judge_2)+list(as_judge_3)
    context = {
        'pic_url': pic_url,
        'judge_1': as_judge_1,
        'judge_2': as_judge_2,
        'judge_3': as_judge_3,
        'total_events': total_events,
    }
    return render(request, 'judge/dashboard.html', context=context)


@allowed_users(['judge'])
def profile(request):
    pic_url = request.user.get_prof_pic_url()
    form = JudgeUpdateForm(instance=request.user)

    if request.POST:
        form = JudgeUpdateForm(request.POST, request.FILES,
                               instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Successfully Updated.')
            return redirect('judge:dashboard')

    context = {
        'pic_url': pic_url,
        'type': 'Judge',
        'form': form,
        'ipinfo_token': os.environ.get('IPLOOKUP_TOKEN'),
    }
    return render(request, 'prof_update.html', context)


def players(request, event_id):
    pic_url = request.user.get_prof_pic_url()
    event = Event.objects.get(pk=event_id)
    players = event.registeredplayer_set.all()
    context = {
        'pic_url': pic_url,
        'players': players,
        'event': event
    }
    return render(request, 'judge/players.html', context)


def set_point(request, event_id, player_id, round):
    event = Event.objects.get(pk=event_id)
    player = event.registeredplayer_set.get(pk=player_id)
    judge = request.user.judgemodel
    try:
        roundResult = player.playerresult_set.get(round=round, judge=judge)
    except Exception as e:
        print(e)
        roundResult = None
    form = MarkingForm(instance=roundResult)
    if request.POST:
        form = MarkingForm(request.POST, instance=roundResult)
        if form.is_valid():
            mf = form.save(commit=False)
            mf.player = player
            mf.judge = judge
            mf.round = round
            mf.save()
            messages.success(request, 'Marks Saved!')
            return redirect('judge:players', event_id=event_id)
    context = {
        'form': form,
        'event': event,
        'player': player,
        'round': round
    }
    return render(request, 'judge/marking.html', context)
