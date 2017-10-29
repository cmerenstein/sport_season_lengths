#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
      

for year in range(2000,2018):
	schedule = []
	for month in ['october', 'november', 'december', 'january', 'february', 'march', 'april']:
		basketball_reference = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_games-" + month + ".html"

		print(basketball_reference)
		
		page = requests.get(basketball_reference).content
		soup = BeautifulSoup(page, "html.parser")
		draft_table = soup.find("table", {"id":"schedule"})
		try: # necessary for shortened seasons
			for row in draft_table.findAll("tr"):
				header = row.findAll("th")
				date = header[0].find(text=True)
				if date == "Playoffs":
					break
				cells = row.findAll("td")
				##print(len(cells))
				game = []
				for data in cells:
					try:
						text = str(data.find(text=True))
						##if month == "april":
							##print(text)
						game.append(str(data.find(text=True)))
					except UnicodeEncodeError:
						row_text.append("")
				schedule.append(game)			
		except:
			if month == "october" or month == "november": #sometimes the seasons starts in november/december
				continue
			else:
				raise
		

	file =  "nba_" + str(year) + ".csv"
	with open(file, 'w') as out:
		for game in schedule:
			line = ",".join(game)
			line = line + "\n"
			out.write(line)
	out.close()
