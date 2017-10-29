import requests
from bs4 import BeautifulSoup
      

for year in range(2000,2018):
	schedule = []
	baseball_reference = "https://www.baseball-reference.com/leagues/MLB/" + str(year) + "-schedule.shtml"

	print(baseball_reference)
	
	page = requests.get(baseball_reference).content
	soup = BeautifulSoup(page, "html.parser")
	regular_season = soup.find("div", {"class":"section_content"})
	for div in regular_season.findAll("div"):
		for p in div.findAll("p"):
			text = p.getText()
			if "Standings" in text:
				continue
			else:
				game_line = text.replace("(", "").replace(")", "").split('\n')
				schedule.append(",".join(game_line))

	file =  "mlb_" + str(year) + "_season.csv"
	with open(file, 'w') as out:
		for game in schedule:
			line = game + "\n"
			out.write(line)
	out.close()
