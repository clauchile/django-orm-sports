from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count, Q

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		# 'books' : League.objects.filter(sport ="Baseball"),
		'ligas_baseball' : League.objects.filter(sport__contains ="baseball"),
		# print(Seller.objects.all().query),
		'ligas_mujeres' : League.objects.filter(name__contains ="women"),
		'ligas_hockey' : League.objects.filter(sport__contains ="hockey"),
		'ligas_football' : League.objects.exclude(sport__contains ="soccer"),
		'ligas_conferencia' : League.objects.filter(name__contains ="conference"),
		'ligas_atlantica' : League.objects.filter(name__contains ="atlantic"),
		'equipo_dallas' : Team.objects.filter(location__contains ="dallas"),
		'equipo_raptor' : Team.objects.filter(team_name__contains ="raptors"),
		'equipo_ciudad' : Team.objects.filter(location__contains ="City"),
		'equipo_start_t' : Team.objects.filter(team_name__startswith ="t"),
		'equipos_inOrderA' : Team.objects.all().order_by('location'),
		'equipos_inOrderZ' : Team.objects.all().order_by('-team_name'),
		'player_Cooper' : Player.objects.filter(last_name__contains = 'Cooper'),
		'player_joshua' : Player.objects.filter(first_name__contains = 'Joshua'),
		'player_CeJ' : Player.objects.filter(last_name = 'Cooper').exclude(first_name__contains = "Joshua"),
		'player_AorW' : Player.objects.filter(first_name__contains = 'Alexander') |  Player.objects.filter (first_name__contains = 'Wyatt' ).order_by('last_name'),
		# 'player_AorW' : Player.objects.filter(Q(first_name__contains = 'Alexander') & Q (first_name__contains = 'Wyatt' )).order_by('last_name'),


	}
	print(League.objects.filter(sport__contains ="baseball").query)

	# print(League..filter(sport = "Baseball"))
	return render(request, "leagues/index.html", context)


def exerciseTwo(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		# 'books' : League.objects.filter(sport ="Baseball"),
		'ligas_Ac' : Team.objects.filter(league__name ="Atlantic Soccer Conference"),
		'playerBp' : Player.objects.filter(curr_team__team_name ="Penguins", curr_team__location="Boston"),
		'playerCl' : Player.objects.filter(curr_team__league__name ="International Collegiate Baseball Conference").order_by("last_name"), 
		'playerCA' : Player.objects.filter(curr_team__league__name ="American Conference of Amateur Football", last_name = "Lopez"). order_by("first_name"), 
		'playerAp' : Player.objects.filter(curr_team__league__sport ="Football").order_by("last_name"), 
		# todos los equipos con un jugador (actual) llamado "Sophia"
		'playerSn' : Team.objects.filter(curr_players__first_name__contains = 'Sophia'),
		# todas las ligas con un jugador (actual) llamado "Sophia"
		'playerSv' : League.objects.filter(teams__curr_players__first_name__contains = 'Sophia'),
		#todos con el apellido "Flores" que NO (actualmente) juegan para los Washington Roughriders
		'playerNf' : Player.objects.filter(last_name__contains = "Flores").exclude(curr_team__team_name ="Roughriders"),
		#todos los equipos, pasados y presentes, con los que Samuel Evans ha jugado
		'playerCs' : Team.objects.filter(all_players__first_name__contains = "Samuel", all_players__last_name__contains = "Evans"),
		#todos los jugadores, pasados y presentes, con los gatos tigre de Manitoba
		'playerGt' : Player.objects.filter(all_teams__team_name__contains = "Tiger-Cats", all_teams__location = 'Manitoba'),
		#todos los jugadores que anteriormente estaban (pero que no lo están) con los Wichita Vikings
		'playerWv' : Player.objects.filter(all_teams__team_name__contains = "Vikings", all_teams__location= "Wichita").exclude(curr_team__team_name= "Vikings"),
		# cada equipo para el que Jacob Gray jugó antes de unirse a los Oregon Colts
		'playerJg' : Team.objects.filter(all_players__first_name = "Jacob", all_players__last_name = "Gray").exclude(team_name= "Colts", location ="Oregon"),
		# 13 todos llamados "Joshua" que alguna vez han jugado en la Federación Atlántica de Jugadores de Béisbol Amateur
		'playerJ' : Player.objects.filter(first_name = "Joshua").filter(all_teams__league__name__contains = "Atlantic Federation of Amateur Baseball Players") ,
		# 14 todos los equipos que han tenido 12 o más jugadores, pasados y presentes. (SUGERENCIA: busque la función de anotación de Django).
		'playerdozen' : Team.objects.annotate(count_players = Count('all_players')).filter(count_players__gte=12).order_by('location') ,
		# 15 todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
		'playerall' : Player.objects.annotate(count_teams = Count('all_teams')).order_by('-count_teams') ,
	
	}

	# print(League..filter(sport = "Baseball"))
	return render(request, "leagues/ejercicio2.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")	