import os

from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.db.models import Prefetch, F, Func, Value, IntegerField, Count
from django.utils import timezone

# Create your views here.

from host.models import Event, RegisteredTeam, RegisteredPlayer, RegisteredMember, Category
from team_leader.models import Player

from account.decorators import allowed_users
from taekwonsoftbd.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT

from .forms import ContactForm, MemberApplyForm, SubMemberApplyForm, SubMemberApplyForm2


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
    events = Event.objects.all()

    if len(events)>2:
        events = events[:2]
    
    context = {
        'events': events
    }
    return render(request, 'home/home.html', context=context)


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
    total_players = event.registeredmember_set.count()

    context = {
        'event': event,
        'total_players': total_players,
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
    event = Event.objects.get(pk=pk,allow_manage=True)
    reg_members = RegisteredMember.objects.filter(
        event=event,
        has_parent=False,
    ).select_related(
        'member', 'category', 'sub_category',
    ).prefetch_related(
        'submembers',
    ).annotate(
        submembers_count=Count('submembers')
    )

    context = {
        'event': event,
        'reg_members': reg_members,
    }

    return render(request, 'home/manage.html', context)


@allowed_users(['tl'])
def downloadID(request, event_id, reg_member_id):
    event = Event.objects.get(pk=event_id)
    reg_member = RegisteredMember.objects.select_related(
        'member'
    ).get(pk=reg_member_id)

    return HttpResponse('Under Development!')

    event_name = event.title
    player_pic_url = reg_member.member.picture.url
    player_name = reg_member.member.name
    player_country = reg_member.member.country
    player_club = team.team.teamleader.club_name
    category = player.category.name

    if DEBUG:
        static_dir = 'static'
    else:
        static_dir = STATIC_ROOT

    bg_image = (static_dir + '/images/id_card.jpg' if not event.id_bg else MEDIA_ROOT + '/images/id_bg/'+event.id_bg.url.split('/')[-1])
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
def event_member_delete(request, event_id, reg_member_id):
    event = Event.objects.get(pk=event_id)
    event.registeredmember_set.get(pk=reg_member_id).delete()
    return redirect('home:manage', pk=event_id)


# @allowed_users(['tl'])
# def apply(request, pk):
#     event = Event.objects.get(pk=pk)
#     teams = request.user.teamleadermodel.team_set.all()
#     team_ids = [team.id for team in teams]
#     players = request.user.teamleadermodel.player_set.all()
#     player_ids = [player.id for player in players]
#     categories = event.category_set.all()
#     category_ids = [category.id for category in categories]

#     if request.POST:
#         # print(request.POST)
#         post_data = dict(request.POST)
#         data = dict()
#         for key in post_data.keys():
#             if key.startswith('player') and not key.startswith('player_'):
#                 data[int(key[6:])] = int(post_data['player_cat'+key[6:]][0])
#         team_id = post_data.get('team', None)
#         if team_id != None and int(team_id[0]) in team_ids:
#             team_id = int(team_id[0])
#             rt = RegisteredTeam(
#                 event=event,
#                 team_id=team_id
#             )
#             rt.save()
#             team_id = rt.id
#             for player_id, category_id in data.items():
#                 #print(player_id, category_id)
#                 if player_id in player_ids and category_id in category_ids:
#                     x = RegisteredPlayer.objects.create(
#                         event=event,
#                         team_id=team_id,
#                         player_id=player_id,
#                         category_id=category_id
#                     )
#                     x.save()
#                     # print(x)
#             messages.success(request, 'Applied Successfully')
#             return redirect('home:event_details', pk=event.id)

#     context = {
#         'event': event,
#         'teams': teams,
#         'players': players,
#         'categories': categories,
#     }

#     return render(request, 'home/apply.html', context)




@allowed_users(['tl'])
def apply__select_member(request, pk):
    event = Event.objects.get(pk=pk, allow_reg=True)

    teamleader = request.user.teamleadermodel
    players = teamleader.player_set.all()

    context = {
        'event': event,
        'players': players,
    }

    return render(request, 'home/apply.html', context)


@allowed_users(['tl'])
def apply__select_team(request, event_id, member_id):
    event = Event.objects.get(pk=event_id, allow_reg=True)

    teamleader = request.user.teamleadermodel
    player = teamleader.player_set.get(pk=member_id)
    teams = teamleader.team_set.all()

    context = {
        'event': event,
        'player': player,
        'teams': teams,
    }

    return render(request, 'home/apply__select_team.html', context)



@allowed_users(['tl'])
def apply__select_category(request, event_id, member_id, team_id):

    event = Event.objects.prefetch_related('category_set').get(pk=event_id, allow_reg=True)

    teamleader = request.user.teamleadermodel
    member = teamleader.player_set.get(pk=member_id)
    team = teamleader.team_set.get(pk=team_id)

    categories = event.category_set.all()

    context = {
        'event': event,
        'member': member,
        'team': team,
        'categories': categories,
    }

    return render(request, 'home/apply__select_category.html', context)


@allowed_users(['tl'])
def apply__select_subcategory(request, event_id, member_id, team_id, category_id):

    event = Event.objects.prefetch_related(
        Prefetch(
            'category_set', 
            queryset=Category.objects.prefetch_related('subcategory_set')
        )
    ).get(pk=event_id, allow_reg=True)
    category = event.category_set.get(pk=category_id)

    teamleader = request.user.teamleadermodel
    member = teamleader.player_set.get(pk=member_id)
    team = teamleader.team_set.get(pk=team_id)

    subcategories = category.subcategory_set.filter(gender=member.gender)

    member_age = member.calculated_age

    # TODO: check if same player in same category exists and redirect to previous step

    temp = []
    for subcategory in subcategories:
        if member_age <= subcategory.max_age and member_age >= subcategory.min_age:
            temp.append(subcategory.id)

    subcategories = subcategories.filter(id__in=temp) # filter with age range

    context = {
        'event': event,
        'member': member,
        'team': team,
        'category': category,
        'subcategories': subcategories,
    }

    return render(request, 'home/apply__select_subcategory.html', context)




@allowed_users(['tl'])
def apply__select_submember(request, event_id, member_id, team_id, category_id, subcategory_id):

    event = Event.objects.prefetch_related(
        Prefetch(
            'category_set', 
            queryset=Category.objects.prefetch_related('subcategory_set')
        )
    ).get(pk=event_id)

    teamleader = request.user.teamleadermodel
    member = teamleader.player_set.get(pk=member_id)
    team = teamleader.team_set.get(pk=team_id)

    category = event.category_set.get(pk=category_id)
    subcategory = category.subcategory_set.get(pk=subcategory_id)


    # Complete registration if no extra member is present
    if category.extra_players == 0:
        RegisteredMember.objects.create(
            event=event,
            category=category,
            sub_category=subcategory,
            member=member,
            team=team,
        )

        messages.success(request, 'Successfully Applied')
        return redirect('home:manage', pk=event_id)


    # TODO: check for previous apply same

    today = timezone.now().date()
    submembers = request.user.teamleadermodel.player_set.annotate(
        age=Func(
            Value("year"),
            Func(Value(today), F("date_Of_Birth"), function="age"),
            function="date_part",
            output_field=IntegerField(),
        )
    ).filter(
        age__gte=subcategory.min_age,
        age__lte=subcategory.max_age,
        gender=subcategory.gender,
    ).exclude(
        id=member.id
    )

    form = SubMemberApplyForm2(
        data=request.POST or None, 
        submembers=submembers, 
        num_of_player=category.extra_players
    )

    if request.method == 'POST':
        if form.is_valid():
            # Register Main Member
            registered_member = RegisteredMember.objects.create(
                event=event,
                category=category,
                sub_category=subcategory,
                member=member,
                team=team,
            )

            # Register Sub-member
            form_data = form.cleaned_data
            for sub_member in form_data.get('members'):
                RegisteredMember.objects.create(
                    event=event,
                    category=category,
                    sub_category=subcategory,
                    member=sub_member,
                    team=team,
                    has_parent=True,
                    parent_member=registered_member,
                )
            
            messages.success(request, 'Successfully Applied')
            return redirect('home:manage', pk=event_id)

    context = {
        'event': event,
        'member': member,
        'team': team,
        'category': category,
        'subcategory': subcategory,
        'submembers': submembers,
        'num_of_player': category.extra_players,
        'form': form,
    }

    return render(request, 'home/apply__select_submember.html', context)






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

    bg_image = (static_dir + '/images/cert.jpg' if not event.cert_bg else MEDIA_ROOT + '/images/cert_bg/'+event.cert_bg.url.split('/')[-1])

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
