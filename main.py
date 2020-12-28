from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)

week = 1

browser.get("https://fantasy.espn.com/basketball/league/scoreboard?leagueId=73608366&matchupPeriodId="+str(week))

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

results = []

# Simulate matchups
for teamIndex in range(10):
	team = teams[teamIndex]
	matchups = teams.copy()
	del matchups[teamIndex] # matchups = all teams without current team
	wonMatchups = 0
	lostTo = []

	for matchup in matchups:
		teamScore = 0
		matchupScore = 0
		ties = 0
		
		for i in range(1, 10):
			# Stat win
			if team[i] > matchup[i]:
				teamScore += 1
			# Stat loss
			elif team[i] < matchup[i]:
				matchupScore += 1
			else:
				ties = ties + 1

		# Team wins
		if teamScore > matchupScore:
			wonMatchups += 1
		# Tie, break with points stat
		elif teamScore == matchupScore and team[9] > matchup[9]:
			wonMatchups += 1
		else:
			lostTo.append(matchup[0])
	
	results.append([team[0], wonMatchups, lostTo])

def sortByWins(arr):
	return arr[1]

results.sort(key=sortByWins, reverse=True)

def lostToString(arr):
	string = ""
	for i, defeat in enumerate(arr):
		if i:
			string += ", "+defeat
		else:
			string += defeat
	
	return string

for result in results:
	print(result[0]+" -- Wins: "+str(result[1]) + " -- Lost to: " + lostToString(result[2]) + "\n<br/>")
	
