import glob
import operator
from scipy import stats

def parse_game(game_line):
	## recycled from NHL script, returns dict with what teams
	## and adds the number of wins (1 or 0) for each team
	game = game_line.split(",")

	winner = game[4]
	
	loser = game[6]
	
	#slightly more convoluted than necessary
	game_dict = {}
	game_dict["winner"] = winner
	game_dict["loser"] = loser
	game_dict["winner_wins"] = 1
	game_dict["loser_wins"] = 0
	
	return game_dict


season_rvals = []	

for season in glob.glob("*_season.csv"):
	print(season)
	teams = {} # dictionary of each team and how many wins after each game
	with open(season, 'r') as schedule:
		for line in schedule:
			if line[0:4] != "Week":
				results = parse_game(line)

				## add wins to season records
				for team in ("winner", "loser"):
					try:
						wins_to_date = teams[results[team]][-1]
						teams[results[team]].append(wins_to_date + results[team+"_wins"])
					except KeyError:
						teams[results[team]] = []
						teams[results[team]].append(results[team+"_wins"])

	season_by_games = []
	
	# there's probably more gymnastics than necessary here but it's fast enough as is.
	games_in_season = len(teams["Pittsburgh Steelers"])
	for i in range(games_in_season): # just using the Steelers to get season length
		season_by_games.append({})
	for team in teams.keys():
		for i in range(len(teams["Pittsburgh Steelers"])):
			try: # In case a team didn't play a full schedule (i.e. 2013 Celtics in NBA)
				season_by_games[i][team] = teams[team][i]
			except:
				pass
	
	season_end_ranks = sorted(season_by_games[-1], key=season_by_games[-1].get, reverse=True)
	print(season, season_end_ranks)
	
	season_end_list = list(range(len(season_end_ranks))) # ranks of teams at the end
	for i in range(games_in_season):
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

		# look at how often final top 3 teams are in the top 3
		
			
i = 1
for game in season_rvals:
	average_rval = sum(game) / len(game)
	print("by game " + str(i) + " the r^2 between current and final standings is: " + str(average_rval))
	i += 1
		
with open("NFL_r_squared_table.csv", 'w') as out:
	out.write("game,r_squared\n")
	i = 1
	for game in season_rvals:
		average_rval = sum(game) / len(game)
		out.write(str(i) + "," + str(average_rval) + "\n")
		i += 1