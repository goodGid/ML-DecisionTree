import os
import pandas

home_folder = os.path.expanduser(os.getcwd())
data_folder = os.path.join(home_folder,"resources")  # [1]

data_files = ["nba_2015_10.csv", "nba_2015_11.csv", "nba_2015_12.csv",
            "nba_2016_01.csv", "nba_2016_02.csv", "nba_2016_03.csv",
            "nba_2016_04.csv", "nba_2016_05.csv", "nba_2016_06.csv"]

cvs_objs = []
for f in data_files:
    month_data = os.path.join(data_folder, f)
    cvs_objs.append(pandas.read_csv(month_data))


season_result = pandas.concat(cvs_objs, ignore_index=True)
season_result.columns = ["Date", "StartTime", "VisitorTeam", "VisitorPts",
                         "HomeTeam", "HomePts", "ScoreType", "Overtime", "Notes"]

# HomeWin: 홈팀이 승리한 경우에는 True, 아닌 경우에는 False으로 입력
season_result["HomeWin"] = season_result["HomePts"] > season_result["VisitorPts"]

# 작년 시즌의 순위를 고려
standing_file = os.path.join(data_folder, "nba_2014_2015_standing.csv")
standing_result = pandas.read_csv(standing_file, skiprows=[0]) # standing_file에 0번째 줄은 불필요한 Data이다.

# 선수 개개인의 능력치를 고려
player_file = os.path.join(data_folder, "nba_2016_player_stat.csv")
player_result = pandas.read_csv(player_file)

# 팀 약자와 팀명을 맵핑
team_name = {"GS"  : "Golden State Warriors",
             "SA"  : "San Antonio Spurs",
             "CLE" : "Cleveland Cavaliers",
             "TOR" : "Toronto Raptors",
             "OKC" : "Oklahoma City Thunder",
             "LAC" : "Los Angeles Clippers",
             "ATL" : "Atlanta Hawks",
             "BOS" : "Boston Celtics",
             "CHA" : "Charlotte Hornets",
             "MIA" : "Miami Heat",
             "IND" : "Indiana Pacers",
             "DET" : "Detroit Pistons",
             "POR" : "Portland Trail Blazers",
             "DAL" : "Dallas Mavericks",
             "MEM" : "Memphis Grizzlies",
             "CHI" : "Chicago Bulls",
             "HOU" : "Houston Rockets",
             "WSH" : "Washington Wizards",
             "UTAH" : "Utah Jazz",
             "ORL" : "Orlando Magic",
             "DEN" : "Denver Nuggets",
             "MIL" : "Milwaukee Bucks",
             "SAC" : "Sacramento Kings",
             "NY" : "New York Knicks",
             "NO" : "New Orleans Pelicans",
             "MIN" : "Minnesota Timberwolves",
             "PHX" : "Phoenix Suns",
             "BKN" : "Brooklyn Nets",
             "LAL" : "Los Angeles Lakers",
             "PHI" : "Philadelphia 76ers",
             }

# NBA 모든 선수를 정보를 순회하면서 각 선수의 팀과 PER 값을 추출
team_per = {}
for key, value in team_name.items():
    team_per[value] = []

for idx, row in player_result.iterrows():
    player = row["PLAYER"]
    per = row["PER"]
    team_list = player.split(',')[1].strip(' ').split("/")
    for team in team_list:
        team_per[team_name[team]].append(per)


# PER 지수 비교
import numpy
print("Golden State Warriors: Sum of PER: {0:.2f} / Mean of PER: {1:.2f}"
      .format(numpy.sum(team_per["Golden State Warriors"]), numpy.mean(team_per["Golden State Warriors"])))
print("Philadelphia 76ers: Sum of PER: {0:.2f} / Mean of PER: {1:.2f}"
      .format(numpy.sum(team_per["Philadelphia 76ers"]), numpy.mean(team_per["Philadelphia 76ers"])))