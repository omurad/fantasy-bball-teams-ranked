from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tabulate import tabulate

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)

week = 6

print("<h2>Week "+str(week)+"</h2>")

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

browser.quit()

results = []

# Concat losses into string
def lostToString(arr):
	string = ""
	for i, defeat in enumerate(arr):
		if i:
			string += ", "+defeat
		else:
			string += defeat
	
	return string

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

		# Team won
		if teamScore > matchupScore:
			wonMatchups += 1
		# Tie, break with points stat
		elif teamScore == matchupScore and team[9] > matchup[9]:
			wonMatchups += 1
		# Team lost
		else:
			lostTo.append(matchup[0])
	
	results.append([team[0], wonMatchups, lostToString(lostTo)])

# Sort value handler
def sortByWins(arr):
	return arr[1]

# Sort results array DESC by wins
results.sort(key=sortByWins, reverse=True)

# Print results in HTML friendly format
print("<h4>All Matchups</h4>")
print(tabulate(results, tablefmt='html'))

# Get stat leaders
stats = [["FG%", "FT%", "3PM", "3P%", "REB", "AST", "STL", "BLK", "PTS"], []]
# Loop over stats
for statIndex in range(1, 10):
	statLeader = ""
	topStat = float(0)
	# Loop over teams
	for team in teams:
		# New stat leader
		if team[statIndex] > topStat:
			statLeader = team[0]
			topStat = team[statIndex]
		# Tie for stat leader
		elif team[statIndex] == topStat:
			statLeader += ", "+team[0]
	
	stats[1].append(statLeader)
	
print("<h4>Top stat performers</h4>")
print(tabulate(stats, tablefmt='html'))
