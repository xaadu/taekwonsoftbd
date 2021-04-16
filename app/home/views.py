import os

from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

# Create your views here.

from host.models import Event, RegisteredTeam, RegisteredPlayer, Category
from account.decorators import allowed_users
from taekwonsoftbd.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT

from .forms import ContactForm, PlayerApplyForm, PlayerUpdateForm


from PIL import Image, ImageDraw, ImageFont


def helper_func_splitText(text):
    text = text.split()
    l = len(text)
    if l > 3:
        first_part = ' '.join(text[:(l//2)])
        second_part = ' '.join(text[(l//2):])
        text = '\n'.join([first_part, second_part])
    elif l == 3:
        first_part = ' '.join(text[:2])
        second_part = ' '.join(text[2:])
        text = '\n'.join([first_part, second_part])
    elif l == 2:
        first_part = ' '.join(text[0])
        second_part = ' '.join(text[1])
        text = '\n'.join([first_part, second_part])
    return text


def comingsoon(request):
    return render(request, 'comingsoon.html')


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    form = ContactForm()

    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Message from {form.cleaned_data["name"]}'
            sender = os.environ.get('SENDER')
            message = 'Sender: '+form.cleaned_data["email"] + '\n\n' \
                'Message: '+form.cleaned_data["message"]
            receipients = os.environ.get('CONTACT_RECIPIENTS').split(',')
            try:
                send_mail(subject, message, sender,
                          receipients, fail_silently=True)
                messages.success(request, 'Email sent successfully!')
            except BadHeaderError:
                messages.error(request, 'Email Could not be send!')
            return redirect('home:home')

    context = {
        'form': form
    }
    return render(request, 'home/contact.html', context)


def about(request):
    return render(request, 'home/about.html')


def events(request):
    events = Event.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(events, 6)
    try:
        events = paginator.page(page)
    except:
        events = paginator.page(1)

    context = {
        'events': events
    }

    return render(request, 'home/events.html', context)


def event_details(request, pk):
    event = Event.objects.get(pk=pk)
    tteams, tplayers = len(event.registeredteam_set.all()), len(
        event.registeredplayer_set.all())
    teamData = {}
    try:
        teams = event.registeredteam_set.all()

        for team in teams:
            teamData[team] = team.registeredplayer_set.all()
    except Exception as e:
        print(e)

    context = {
        'event': event,
        'teamData': teamData,
        'tteams': tteams,
        'tplayers': tplayers,
    }

    return render(request, 'home/event.html', context)


def event_teams(request, pk):
    event = Event.objects.get(pk=pk)
    teams = event.registeredteam_set.all()
    context = {
        'event': event,
        'teams': teams
    }

    return render(request, 'home/teams.html', context)


def event_team_details(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    team = event.registeredteam_set.get(pk=reg_team_id)
    players = team.registeredplayer_set.all()
    context = {
        'event': event,
        'team': team,
        'players': players
    }

    return render(request, 'home/team_details.html', context)


def event_players(request, pk):
    event = Event.objects.get(pk=pk)
    players = event.registeredplayer_set.all()
    context = {
        'event': event,
        'players': players
    }

    return render(request, 'home/players.html', context)


@allowed_users(['tl'])
def manage(request, pk):
    event = Event.objects.get(pk=pk)
    teamData = {}
    try:
        teams = list(event.registeredteam_set.all())

        # Doesn't support in mysql
        # userTeams = request.user.teamleadermodel.registeredteam_set.filter(
        #    event_id=pk)
        #teams = teams.intersection(userTeams)

        userTeams = list(request.user.teamleadermodel.team_set.all())
        userTeamIDs = [user.id for user in userTeams]
        teams = [team for team in teams if team.team_id in userTeamIDs]

        for team in teams:
            teamData[team] = team.registeredplayer_set.all()

    except Exception as e:
        print(e)

    context = {
        'event': event,
        'teamData': teamData
    }

    return render(request, 'home/manage.html', context)


@allowed_users(['tl'])
def downloadID(request, event_id, team_id, player_id):
    event = Event.objects.get(pk=event_id)
    team = RegisteredTeam.objects.get(pk=team_id)
    player = RegisteredPlayer.objects.get(pk=player_id)

    event_name = event.title
    player_pic_url = player.player.picture.url
    player_name = player.player.name
    player_country = player.player.country
    player_club = team.team.teamleader.club_name
    category = player.category.name

    if DEBUG:
        static_dir = 'static'
    else:
        static_dir = STATIC_ROOT

    bg_image = static_dir + '/images/id_card.jpg'
    player_pic = MEDIA_ROOT + '/images/player/' + player_pic_url.split('/')[-1]

    im = Image.open(player_pic)
    img = Image.open(bg_image)

    width, height = im.size

    im = im.crop((0, 0, width, width))
    im = im.resize((340, 340))

    width, height = im.size

    bigsize = (width * 3, height * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)

    # im.putalpha(mask)
    img.paste(im, (386, 74), mask)

    width, height = img.size

    jersey = ImageFont.truetype(
        static_dir+'/vendor/fonts/JerseyM54.ttf', 100
    )
    metrisch = ImageFont.truetype(
        static_dir+'/vendor/fonts/Metrisch-Medium.otf', 44
    )
    metrisch2 = ImageFont.truetype(
        static_dir+'/vendor/fonts/Metrisch-Medium.otf', 32
    )

    d = ImageDraw.Draw(img)

    # player_name = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'
    # event_name = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'
    # category = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'

    # Player ID
    font = jersey
    player_id = str(player_id).zfill(4)
    w, h = d.textsize(player_id, font=font)
    d.text((60, 120), player_id,
           fill=(255, 255, 255), font=font)

    # Player Name
    font = metrisch
    w, h = d.textsize(player_name, font=font)
    if width-w < 20:
        player_name = helper_func_splitText(player_name)
    w, h = d.textsize(player_name, font=font)
    d.text(((width-w)/2, 500), player_name,
           fill=(27, 26, 81), font=font)

    # Player Category
    font = metrisch2
    w, h = d.textsize(category, font=font)
    if width-w < 20:
        category = helper_func_splitText(category)
    w, h = d.textsize(category, font=font)
    d.text(((width-w)/2, 600), category,
           fill=(50, 50, 50), font=font)

    # Player Club
    font = metrisch2
    w, h = d.textsize(player_club, font=font)
    d.text(((width-w)/2, 700), player_club,
           fill=(100, 100, 100), font=font)

    # Player Country
    font = metrisch2
    w, h = d.textsize(player_country, font=font)
    d.text(((width-w)/2, 750), player_country,
           fill=(100, 100, 100), font=font)

    # Event Name
    font = metrisch
    w, h = d.textsize(event_name, font=font)
    if width-w < 20:
        event_name = helper_func_splitText(event_name)
    w, h = d.textsize(event_name, font=font)
    d.text(((width-w)/2, 820), event_name,
           fill=(50, 50, 50), font=font)

    '''img_path = MEDIA_ROOT + f'/temp/{event_id}/id_cards'

    if not os.path.isdir(img_path):
        os.makedirs(img_path)

    img_path = img_path + f'/id_card_{player_id}.jpg'

    img.save(img_path, 'JPEG', quality=100, subsampling=0)'''

    response = HttpResponse(content_type='image/jpeg')

    img.save(response, 'JPEG', quality=100, subsampling=0)

    # return FileResponse(open(img_path, 'rb'))
    return response


@allowed_users(['tl'])
def event_team_update(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    team = event.registeredteam_set.get(pk=reg_team_id)
    players = request.user.teamleadermodel.player_set.all()
    player_ids = [player.id for player in players]
    # print(player_ids)
    categories = event.category_set.all()
    category_ids = [category.id for category in categories]
    # print(category_ids)

    if request.POST:
        # print(request.POST)
        post_data = dict(request.POST)
        data = dict()
        for key in post_data.keys():
            if key.startswith('player') and not key.startswith('player_'):
                data[int(key[6:])] = int(post_data['player_cat'+key[6:]][0])

        team.registeredplayer_set.all().delete()
        for player_id, category_id in data.items():
            #print(player_id, category_id)
            if player_id in player_ids and category_id in category_ids:
                x = RegisteredPlayer.objects.create(
                    event=event,
                    team=team,
                    player_id=player_id,
                    category_id=category_id
                )
                x.save()
                # print(x)
        messages.success(request, 'Updated Successfully')
        return redirect('home:manage', pk=event.id)

    context = {
        'event': event,
        'players': players,
        'categories': categories,
    }

    return render(request, 'home/update.html', context)


@allowed_users(['tl'])
def event_team_delete(request, event_id, reg_team_id):
    event = Event.objects.get(pk=event_id)
    event.registeredteam_set.get(pk=reg_team_id).delete()
    return redirect('home:manage', pk=event_id)


@allowed_users(['tl'])
def apply(request, pk):
    event = Event.objects.get(pk=pk)
    teams = request.user.teamleadermodel.team_set.all()
    team_ids = [team.id for team in teams]
    players = request.user.teamleadermodel.player_set.all()
    player_ids = [player.id for player in players]
    categories = event.category_set.all()
    category_ids = [category.id for category in categories]

    if request.POST:
        # print(request.POST)
        post_data = dict(request.POST)
        data = dict()
        for key in post_data.keys():
            if key.startswith('player') and not key.startswith('player_'):
                data[int(key[6:])] = int(post_data['player_cat'+key[6:]][0])
        team_id = post_data.get('team', None)
        if team_id != None and int(team_id[0]) in team_ids:
            team_id = int(team_id[0])
            rt = RegisteredTeam(
                event=event,
                team_id=team_id
            )
            rt.save()
            team_id = rt.id
            for player_id, category_id in data.items():
                #print(player_id, category_id)
                if player_id in player_ids and category_id in category_ids:
                    x = RegisteredPlayer.objects.create(
                        event=event,
                        team_id=team_id,
                        player_id=player_id,
                        category_id=category_id
                    )
                    x.save()
                    # print(x)
            messages.success(request, 'Applied Successfully')
            return redirect('home:event_details', pk=event.id)

    context = {
        'event': event,
        'teams': teams,
        'players': players,
        'categories': categories,
    }

    return render(request, 'home/apply.html', context)


def result_categories(request, event_id):
    event = Event.objects.get(pk=event_id)
    categories = event.category_set.all()
    _categories = {}
    for category in categories:
        _categories[category] = len(category.registeredplayer_set.all())

    context = {
        'event': event,
        'categories': _categories,
    }

    return render(request, 'home/result_categories.html', context)


def results(request, event_id, category_id):
    event = Event.objects.get(pk=event_id)
    category = Category.objects.get(pk=category_id)
    players = category.registeredplayer_set.all()
    playerWithResults = dict()
    for player in players:
        roundResults = player.playerresult_set.all()
        finalPoint = 0
        for res in roundResults:
            finalPoint += res.accuracy+res.presentation
        try:
            finalPoint /= len(roundResults)
        except ZeroDivisionError:
            finalPoint = 0
        playerWithResults[player] = '{:.2f}'.format(finalPoint)

    context = {
        'event': event,
        'category': category,
        'playerWithResults': playerWithResults,
    }

    return render(request, 'home/results.html', context)


def downloadCert(request, event_id, team_id, player_id):
    event = Event.objects.get(pk=event_id)
    team = RegisteredTeam.objects.get(pk=team_id)
    player = RegisteredPlayer.objects.get(pk=player_id)
    category = player.category

    event_name = event.title
    player_name = player.player.name
    player_country = player.player.country
    player_club = team.team.teamleader.club_name
    category = player.category.name

    roundResults = player.playerresult_set.all()
    finalPoint = 0
    for res in roundResults:
        finalPoint += res.accuracy+res.presentation
    try:
        finalPoint /= len(roundResults)
    except ZeroDivisionError:
        finalPoint = 0
    finalPoint = '{:.2f}'.format(finalPoint)

    if DEBUG:
        static_dir = 'static'
    else:
        static_dir = STATIC_ROOT

    bg_image = static_dir + '/images/cert.jpg'

    img = Image.open(bg_image)

    width, height = img.size

    jersey = ImageFont.truetype(
        static_dir+'/vendor/fonts/JerseyM54.ttf', 120
    )
    Poppins = ImageFont.truetype(
        static_dir+'/vendor/fonts/Poppins-Regular.ttf', 60
    )
    Poppins_BIG = ImageFont.truetype(
        static_dir+'/vendor/fonts/Poppins-Regular.ttf', 75
    )
    ArimaMadurai = ImageFont.truetype(
        static_dir+'/vendor/fonts/ArimaMadurai-Bold.ttf', 180
    )

    d = ImageDraw.Draw(img)

    # player_name = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'
    # event_name = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'
    # category = 'One Two Three Four Five Six Seven Right Nine Ten Eleven'

    # Player ID
    font = jersey
    player_id = str(player_id).zfill(4)
    w, h = d.textsize(player_id, font=font)
    d.text(((width-w)/2, 1240), player_id,
           fill=(200, 200, 200), font=font)

    
    # Player Name
    font = ArimaMadurai
    w, h = d.textsize(player_name, font=font)
    if width-w < 20:
        player_name = helper_func_splitText(player_name)
    w, h = d.textsize(player_name, font=font)
    d.text(((width-w)/2, 940), player_name,
           fill=(131, 182, 39), font=font)
    
    # Player Category
    font = Poppins
    w, h = d.textsize(category, font=font)
    if width-w < 20:
        category = helper_func_splitText(category)
    w, h = d.textsize(category, font=font)
    d.text(((width-w)/2, 1400), category,
           fill=(100, 100, 100), font=font)

    
    # Player Club
    font = Poppins
    w, h = d.textsize(player_club, font=font)
    d.text(((width-w)/2, 1500), player_club,
           fill=(100, 100, 100), font=font)
    

    # Player Country
    font = Poppins
    w, h = d.textsize(player_country, font=font)
    d.text(((width-w)/2, 1600), player_country,
           fill=(100, 100, 100), font=font)


    # Event Name
    font = Poppins_BIG
    w, h = d.textsize(event_name, font=font)
    if width-w < 20:
        event_name = helper_func_splitText(event_name)
    w, h = d.textsize(event_name, font=font)
    d.text(((width-w)/2, 1710), event_name,
           fill=(50, 50, 50), font=font)

    response = HttpResponse(content_type='image/jpeg')

    img.save(response, 'JPEG', quality=100, subsampling=0)

    return response
