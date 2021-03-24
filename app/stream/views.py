from django.shortcuts import redirect, render, HttpResponse

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


def roundResult(request, event_id, reg_player_id, round):
    event = Event.objects.get(pk=event_id)
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

    results = reg_player.playerresult_set.filter(round=round)
    judges = [event.judge_1, event.judge_2, event.judge_3]

    try:
        judge1 = reg_player.playerresult_set.get(judge=judges[0])
    except:
        #messages.error(request, 'Judge 1 Not Submitted the Point')
        judge1 = None
    try:
        judge2 = reg_player.playerresult_set.get(judge=judges[1])
    except:
        #messages.error(request, 'Judge 2 Not Submitted the Point')
        judge2 = None
    try:
        judge3 = reg_player.playerresult_set.get(judge=judges[2])
    except:
        #messages.error(request, 'Judge 3 Not Submitted the Point')
        judge3 = None

    tot_pre, tot_acc, total = 0, 0, 0

    for result in results:
        tot_pre += result.presentation
        tot_acc += result.accuracy

    rl = len(results)

    if rl > 0:
        tot_acc = "{:.2f}".format(tot_acc/rl)
        tot_pre = "{:.2f}".format(tot_pre/rl)
        total = "{:.2f}".format(float(tot_acc)+float(tot_pre))

    context = {
        'player': reg_player,
        'current_round': round,
        'results': results,
        'judges': judges,
        'judge1': judge1,
        'judge2': judge2,
        'judge3': judge3,
        'acc': tot_acc,
        'pre': tot_pre,
        'total': total,
    }
    return render(request, 'stream/splitted/roundResult.html', context)


def finalResult(request, event_id, reg_player_id):
    event = Event.objects.get(pk=event_id)
    try:
        reg_player = RegisteredPlayer.objects.get(pk=reg_player_id)
    except Exception as e:
        print(e)
        messages.error(request, 'No Player Found')
        return redirect('stream:players', event_id=event_id)

    total_round = reg_player.category.round

    results = list()

    for i in range(1, total_round+1):
        roundResults = reg_player.playerresult_set.filter(round=i)
        tot = 0
        for result in roundResults:
            tot += result.presentation
            tot += result.accuracy
        if len(roundResults) > 0:
            tot /= len(roundResults)
        results.append("{:.2f}".format(tot))
    total = 0
    for r in results:
        total += float(r)

    if len(results) > 0:
        total = total/len(results)

    context = {
        'player': reg_player,
        'results': results,
        'total': total,
    }
    return render(request, 'stream/splitted/finalResult.html', context)
