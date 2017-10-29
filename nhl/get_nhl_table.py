import glob
import operator
from scipy import stats

def parse_game(game_line):
	## This returns a dict of who the home and away teams were
	## and the number of points (2 for win, 1 OT loss/tie, 0 loss)
	## each team gained from the game.
	game = game_line.split(",")
	away = game[1]
	away_goals = game[2]
	away_points = 0
	
	home = game[3]
	home_goals = game[4]
	home_points = 0
	
	OT = True
	if (game[5] == ""):
		OT = False

	if int(away_goals) > int(home_goals):
		away_points = 2
		if OT:
				home_points = 1
	elif int(home_goals) > int(away_goals):
		home_points = 2
		if OT:
				away_points = 1
	# except:
		
	else: # before the lockout there were ties
			home_points = 1
			away_points = 1
	game_dict = {}
	game_dict["home"] = home
	game_dict["away"] = away
	game_dict["away_points"] = away_points
	game_dict["home_points"] = home_points
	return game_dict

def postponed(line):
	## Just check to make sure the game was actually played
	game = line.split(",")
	away_goals = game[2]
	home_goals = game[4]
	try:
		int(away_goals)
		int(home_goals)
		return False #meaning not postponed
	except ValueError:
		return True
		
season_rvals = []	

for season in glob.glob("*_season.csv"):
	teams = {} # dictionary of each team and how many points after each game
	with open(season, 'r') as schedule:
		for line in schedule:
			if line[0:4] != "Date":
				if postponed(line):					
					continue
				results = parse_game(line)

				## add points to season records
				for team in ("home", "away"):
					try:
						points_to_date = teams[results[team]][-1]
						teams[results[team]].append(points_to_date + results[team+"_points"])
					except KeyError:
						teams[results[team]] = []
						teams[results[team]].append(results[team+"_points"])


	# there's probably more gymnastics than necessary here but it's fast enough as is.
	season_by_games = []	
	for i in range(82):
		season_by_games.append({})
	for team in teams.keys():
		for i in range(82):
			season_by_games[i][team] = teams[team][i]
	
	season_end_ranks = sorted(season_by_games[-1], key=season_by_games[-1].get, reverse=True)
	print(season, season_end_ranks)
	season_end_list = list(range(len(season_end_ranks))) # ranks of teams at the end
	for i in range(82):
		teams_ranked = sorted(season_by_games[i], key=season_by_games[i].get, reverse=True)
		teams_ranked_list = []
		for team in season_end_ranks:
			# ordered the same as final season standings
			teams_ranked_list.append(teams_ranked.index(team))
		r, pval = stats.spearmanr(season_end_list, teams_ranked_list)
		
		# add r val for this game at this season to list for all seasons
		try:
			season_rvals[i].append(r)
		except:
			season_rvals.append([])
			season_rvals[i].append(r)

i = 1
for game in season_rvals:
	average_rval = sum(game) / len(game)
	print("by game " + str(i) + " the r^2 between current and final standings is: " + str(average_rval))
	i += 1

with open("NHL_r_squared_table.csv", 'w') as out:
	out.write("game,r_squared\n")
	i = 1
	for game in season_rvals:
		average_rval = sum(game) / len(game)
		out.write(str(i) + "," + str(average_rval) + "\n")
		i += 1