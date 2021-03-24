from django.shortcuts import redirect, render

from django.contrib import messages

# Create your views here.

from host.models import Event, RegisteredPlayer


def events(request):
    events = Event.objects.all()
    context = {
        'events': events
    }
    return render(request, 'stream/helpers/events.html', context)


def players(request, event_id):
    event = Event.objects.get(pk=event_id)
    players = event.registeredplayer_set.all()
    context = {
        'event': event,
        'players': players,
    }
    return render(request, 'stream/helpers/players.html', context)


def playerDetails(request, event_id, reg_player_id, round):
    try:
        reg_player = RegisteredPlayer.objects.get(pk=reg_player_id)
    except Exception as e:
        print(e)
        messages.error(request, 'No Player Found')
        return redirect('stream:players', event_id=event_id)

    total_round = reg_player.category.round
    if round > total_round:
        messages.error(request, 'Round is out of range!')
        return redirect('stream:players', event_id=event_id)
    context = {
        'player': reg_player,
        'current_round': round
    }
    return render(request, 'stream/splitted/playerDetails.html', context)
