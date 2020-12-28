"""from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)

browser.get("https://fantasy.espn.com/basketball/league/scoreboard?leagueId=73608366")

# 2D array for all team stats
teams = []

# Wait for stats to load
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.Table__TR--sm")))

# Loop over teams and store stats
for team in browser.find_elements_by_css_selector("tr.Table__TR--sm"):
	stats = []
	for stat in team.find_elements_by_css_selector("td div"):
		try:
			stats.append(float(stat.text))
		except:
			stats.append(stat.text)
	teams.append(stats)

for team in teams:
	print(team)

browser.quit()

"""

teams = [['MIDD', 0.5289, 0.8125, 35.0, 0.4321, 88.0, 51.0, 15.0, 6.0, 312.0], ['JACK', 0.4601, 0.75, 23.0, 0.3333, 98.0, 68.0, 20.0, 11.0, 270.0],['CHEF', 0.4722, 0.8491, 40.0, 0.381, 92.0, 82.0, 18.0, 17.0, 289.0],['SUNs', 0.4703, 0.6324, 24.0, 0.381, 89.0, 50.0, 16.0, 11.0, 241.0],['BAM', 0.5252, 0.8, 10.0, 0.2941, 78.0, 40.0, 12.0, 6.0, 188.0],['CBB', 0.45, 0.9286, 35.0, 0.3804, 82.0, 59.0, 17.0, 10.0, 290.0],['ZK', 0.5141, 0.6604, 21.0, 0.4038, 83.0, 38.0, 10.0, 12.0, 202.0],['BEER', 0.4852, 0.7826, 14.0, 0.3182, 78.0, 40.0, 13.0, 5.0, 232.0],['DD', 0.4828, 0.8, 20.0, 0.3448, 70.0, 51.0, 14.0, 10.0, 232.0],['BALL', 0.4645, 0.7377, 15.0, 0.2459, 79.0, 70.0, 12.0, 4.0, 230.0]]
"""for team in teams:
	print(type(team[9]))"""

results = []

# Simulate matchups
for thisTeam, team in enumerate(teams):
	matchups = teams
	del matchups[thisTeam] # matchups = all teams without current team
	thisTeamScore = 0

	for matchup in matchups:
		teamScore = 0
		matchupScore = 0
		ties = 0 
		for i in range(1, 10):
			# Win
			if team[i] > matchup[i]:
				teamScore = teamScore + 1
			elif team[i] < matchup[i]:
				matchupScore = matchupScore + 1
			else:
				ties = ties + 1

		if teamScore > matchupScore:
			thisTeamScore = thisTeamScore + 1
		elif teamScore == matchupScore and team[9] > matchup[9]:
			thisTeamScore = thisTeamScore + 1
		else:
			print(team[0]+" lost to "+matchup[0])
	
	results.append([team[0], thisTeamScore])

for result in results:
	print(result[0]+": "+str(result[1]))