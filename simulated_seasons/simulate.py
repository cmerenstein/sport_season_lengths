import random
from scipy import stats

def sim_game(home, away):
	winner_loser = {}
	better = ""
	worse = ""
	
	if quality_of_teams[home] > quality_of_teams[away]:
		better = home
		worse = away
	else:
		better = away
		worse = home
	
	if random.random() < odds_better_team_wins:
		winner_loser["winner"] = better
		winner_loser["loser"] = worse
	else:
		winner_loser["winner"] = worse
		winner_loser["loser"] = better
		
	return winner_loser


	
teams = []

quality_of_teams = {}
for i in range(30):
	team_name = str("team_" + str(i))
	teams.append(team_name)
	quality_of_teams[team_name] = i

length_of_season = 82
odds_better_team_wins = .50 # 0.5 = totally luck, 1.0 = better team wins every time

rvals = []
for season in range(100):
	standings_by_game = []
	wins_by_team = {}
	for team in teams:
		wins_by_team[team] = 0

	for game_number in range(length_of_season):
	## simulate each set of games for every team
		random.shuffle(teams)
		
		for i in range(0, 30, 2):
			home = teams[i]
			away = teams[i + 1]
			
			winner_loser = sim_game(home, away)
			wins_by_team[winner_loser["winner"]] += 1
		
		standings = sorted(wins_by_team, key=wins_by_team.get, reverse=True)
		standings_by_game.append(standings)
		print(game_number, wins_by_team)
		
	## calculate correlation between standings at each game and final standings
	final_standings = standings_by_game[-1]
	final_rank_dummy_list = list(range(30))
	for i in range(length_of_season):
		standings = standings_by_game[i]
		print(standings)
		teams_ranked_list = []
		for team in final_standings:
			# ordered the same as final season standings
			teams_ranked_list.append(standings.index(team))
		r, pval = stats.spearmanr(final_rank_dummy_list, teams_ranked_list)
		try:
			rvals[i].append(r)
		except IndexError:
			rvals.append([])
			rvals[i].append(r)
	print(len(standings_by_game))
			
with open("simulated_50.csv", 'w') as out:
	out.write("games, r_squared, odds better team wins\n")
	for i in range(82):
		mean_rval = sum(rvals[i]) / len(rvals[i])
		out.write(str(i) + "," + str(mean_rval) + "," + str(odds_better_team_wins) + "\n")
	