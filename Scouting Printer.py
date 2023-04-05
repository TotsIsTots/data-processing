# Scouting Printer
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import webbrowser
import statbotics
CurrentTime = dt.datetime.now()
sb = statbotics.Statbotics()
path = os.getcwd()

team_number = int(input("Enter Team Number: "))

# Pull data from data.csv
data = pd.read_csv('data.csv')
data.sort_values(by=['Match Number'], inplace=True)

MatchesPlayed = list(data[data['Team Number'] == team_number]['Match Number'])
MatchesStr = "Matches played: " + str(MatchesPlayed)[1:-1]
NumofBreakdownsStr= "Number of breakdowns: " + str(data[data['Team Number'] == team_number]['Robot Breakdown'].sum())
DefenseStr = "Average defense level: " + str(data[data['Team Number'] == team_number]['DEFENSE'].mean())
StatBotinfo = pd.DataFrame(sb.get_team_year(team_number, dt.datetime.now().year, ['auto_epa_end', 'teleop_epa_end', 'endgame_epa_end', 'epa_end']), index=[0])

low_auto_cube_points = [x * 3 for x in list(data[data['Team Number'] == team_number]['Auto Low Cube'])]
mid_auto_cube_points = [x * 4 for x in list(data[data['Team Number'] == team_number]['Auto Mid Cube'])]
top_auto_cube_points = [x * 6 for x in list(data[data['Team Number'] == team_number]['Auto High Cube'])]

auto_cube_scores = [x + y + z for x, y, z in zip(low_auto_cube_points, mid_auto_cube_points, top_auto_cube_points)]

low_auto_cone_points = [x * 3 for x in list(data[data['Team Number'] == team_number]['Auto Low Cone'])]
mid_auto_cone_points = [x * 4 for x in list(data[data['Team Number'] == team_number]['Auto Mid Cone'])]
top_auto_cone_points = [x * 6 for x in list(data[data['Team Number'] == team_number]['Auto High Cone'])]

auto_cone_scores = [x + y + z for x, y, z in zip(low_auto_cone_points, mid_auto_cone_points, top_auto_cone_points)]

auto_mobility_points = [x * 3 for x in list(data[data['Team Number'] == team_number]['MOBILITY'])]
auto_docked_points = [x * 8 for x in list(data[data['Team Number'] == team_number]['Auto Docked'])]
auto_engaged_points = [x * 12 for x in list(data[data['Team Number'] == team_number]['Auto Engage'])]

auto_community_scores = [x + y + z for x, y, z in zip(auto_mobility_points, auto_docked_points, auto_engaged_points)]

low_tele_cube_points = [x * 2 for x in list(data[data['Team Number'] == team_number]['Tele Low Cube'])]
mid_tele_cube_points = [x * 3 for x in list(data[data['Team Number'] == team_number]['Tele Mid Cube'])]
top_tele_cube_points = [x * 5 for x in list(data[data['Team Number'] == team_number]['Tele High Cube'])]

teleop_cube_scores = [x + y + z for x, y, z in zip(low_tele_cube_points, mid_tele_cube_points, top_tele_cube_points)]

low_tele_cone_points = [x * 2 for x in list(data[data['Team Number'] == team_number]['Tele Low Cone'])]
mid_tele_cone_points = [x * 3 for x in list(data[data['Team Number'] == team_number]['Tele Mid Cone'])]
top_tele_cone_points = [x * 5 for x in list(data[data['Team Number'] == team_number]['Tele High Cone'])]

teleop_cone_scores = [x + y + z for x, y, z in zip(low_tele_cone_points, mid_tele_cone_points, top_tele_cone_points)]

teleop_parked_points = [x * 2 for x in list(data[data['Team Number'] == team_number]['Tele Charge Station'] == 'Parked')]
teleop_docked_points = [x * 6 for x in list(data[data['Team Number'] == team_number]['Tele Charge Station'] == 'Docked')]
teleop_engaged_points = [x * 10 for x in list(data[data['Team Number'] == team_number]['Tele Charge Station'] == 'Engaged')]

teleop_community_scores = [x + y + z for x, y, z in zip(teleop_parked_points, teleop_docked_points, teleop_engaged_points)]

link_scores = [x * 5 for x in list(data[data['Team Number'] == team_number]['Links'])]

total_cone_scores = [x + y for x, y in zip(teleop_cone_scores, auto_cone_scores)]
total_cube_scores = [x + y for x, y in zip(teleop_cube_scores, auto_cube_scores)]
total_auto_scores = [x + y for x, y in zip(auto_cone_scores, auto_cube_scores)]
total_teleop_scores = [x + y + z for x, y, z in zip(teleop_cone_scores, teleop_cube_scores, link_scores)]
total_points = [x + y + z + a + b for x, y, z, a, b in zip(total_cone_scores, total_cube_scores, auto_community_scores, teleop_community_scores, link_scores)]
for xc in MatchesPlayed:
    plt.axvline(x=xc, color='lightgrey', linestyle='--')
plt.plot(MatchesPlayed, total_points)
plt.xlabel('Match Number')
plt.ylabel('Points')
plt.savefig('scorevmatch.png')
plt.close()


for xc in MatchesPlayed:
    plt.axvline(x=xc, color='lightgrey', linestyle='--')
plt.plot(MatchesPlayed, total_auto_scores)
plt.xlabel('Match Number')
plt.ylabel('Auto Points')
plt.savefig('auto_scorevmatch.png')
plt.close()

TTA = {'Top': sum(top_auto_cone_points) / len(MatchesPlayed), 'Mid': sum(mid_auto_cone_points) / len(MatchesPlayed),'Bot': sum(low_auto_cone_points) / len(MatchesPlayed)}
Triangle_Table_Auto = pd.DataFrame(TTA, index=[0])
STA = {'Top': sum(top_auto_cube_points) / len(MatchesPlayed), 'Mid': sum(mid_auto_cube_points) / len(MatchesPlayed),'Bot': sum(low_auto_cube_points) / len(MatchesPlayed)}
Square_Table_Auto = pd.DataFrame(STA, index=[0])
CSTA = {'Mobility': sum(auto_mobility_points) / len(MatchesPlayed), 'Docked': sum(auto_docked_points) / len(MatchesPlayed),'Engaged': sum(auto_engaged_points) / len(MatchesPlayed)}
ChargeStation_table_Auto = pd.DataFrame(CSTA, index=[0])


for xc in MatchesPlayed:
    plt.axvline(x=xc, color='lightgrey', linestyle='--')
total = plt.plot(MatchesPlayed, total_teleop_scores)
link_line = plt.plot(MatchesPlayed, link_scores)
cone_line = plt.plot(MatchesPlayed, teleop_cone_scores)
cube_line = plt.plot(MatchesPlayed, teleop_cube_scores)
plt.xlabel('Match Number')
plt.ylabel('Teleop Points')
plt.legend((total[0], link_line[0], cone_line[0], cube_line[0]), ('Total', 'Links', 'Cones', 'Cubes'))
plt.savefig('teleop_scorevmatch.png')
plt.close()

TTT = {'Top': sum(top_tele_cone_points) / len(MatchesPlayed), 'Mid': sum(mid_tele_cone_points) / len(MatchesPlayed),'Bot': sum(low_tele_cone_points) / len(MatchesPlayed)}
Triangle_Table_Tele = pd.DataFrame(TTT, index=[0])
STT = {'Top': sum(top_tele_cube_points) / len(MatchesPlayed), 'Mid': sum(mid_tele_cube_points) / len(MatchesPlayed),'Bot': sum(low_tele_cube_points) / len(MatchesPlayed)}
Square_Table_Tele = pd.DataFrame(STT, index=[0])
CSTT = {'Parked': sum(teleop_parked_points) / len(MatchesPlayed), 'Docked': sum(teleop_docked_points) / len(MatchesPlayed),'Engaged': sum(teleop_engaged_points) / len(MatchesPlayed)}
ChargeStation_table_Tele = pd.DataFrame(CSTT, index=[0])
        
# sum of all robots docked or engaged in a match

i = 0
teams_on_station = []
for index, row in data.iterrows():
    if row['Team Number'] == team_number:
        teams = list(data[(data['Alliance'] == row['Alliance']) & (data['Match Number'] == row['Match Number'])]['Team Number'])
        # print each team's charging status
        teams_on_station.append(0)
        for team in teams:
            status = list(data[(data['Team Number'] == team) & (data['Match Number'] == row['Match Number'])]['Tele Charge Station'])[0]
            if status == 'Engaged' or status == 'Docked':
                teams_on_station[i] += 1
        i += 1



i = 0
for xc in MatchesPlayed:
    plt.vlines(x=xc, ymin=teams_on_station[i], ymax=3, color='lightgrey', linestyle='--')
    
    i += 1

i = 0
for status in list(data[data['Team Number'] == team_number]['Tele Charge Station']):
    if status == 'Parked':
        plt.hlines(y=1, xmin=MatchesPlayed[i] - 1, xmax=MatchesPlayed[i] + 1, color='black')
    elif status == 'Docked':
        plt.hlines(y=2, xmin=MatchesPlayed[i] - 1, xmax=MatchesPlayed[i] + 1, color='black')
    elif status == 'Engaged':
        plt.hlines(y=3, xmin=MatchesPlayed[i] - 1, xmax=MatchesPlayed[i] + 1, color='black')
    i += 1
    
plt.bar(MatchesPlayed, teams_on_station)
plt.xlabel('Match Number')
plt.ylabel('Number of Robots on Charge Station')

# new y label on other side
ax2 = plt.twinx()
ax2.set_ylabel('Charge Station Status')
plt.yticks([1, 2, 3], ['Parked', 'Docked', 'Engage'])

#extend image to the right



plt.savefig('teleop_parked_docked_engaged.png')
plt.close()

comments_list = list(data[data['Team Number'] == team_number]['Comment'])
comments_str = ''
for i in range(len(comments_list)):
    if type(comments_list[i]) == str:
        comments_list[i] = comments_list[i].replace('■', ',')
        comments_str += 'Match ' + str(MatchesPlayed[i]) + ': ' + comments_list[i] + '<br>'

# write HTML

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Scouting</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
    <h1>Overview of Team {team_number}</h1>
    <p>{CurrentTime}<p>
    <p>{MatchesStr}</p>
    <p>{NumofBreakdownsStr}</p>
    <p>{DefenseStr}</p>
    <p>{StatBotinfo.to_html(classes='table', header="true", index=False)}</p>
    <img src="{path}/scorevmatch.png" alt="Score vs Match">
    <br>

    <h1>Auto</h1>
    <img src="{path}/auto_scorevmatch.png" alt="Auto Score vs Match">
     <div class="row">
        <div class="col-sm-4">
            <p>Average cone scores:</p>
            {Triangle_Table_Auto.to_html(classes='table', header="true", index=False)}
        </div>
        <div class="col-sm-4">
            <p>Average cube scores:</p>
            {Square_Table_Auto.to_html(classes='table', header="true", index=False)}
        </div>
        <div class="col-sm-4">
            <p>Average community scores:</p>
            {ChargeStation_table_Auto.to_html(classes='table', header="true", index=False)}
        </div>
    </div>
    
                
    
    <h1>Teleop</h1>
    <img src="{path}/teleop_scorevmatch.png" alt="Teleop Score vs Match">
    <div class="row">
        <div class="col-sm-4">
            <p>Average cone scores:</p>
            {Triangle_Table_Tele.to_html(classes='table', header="true", index=False)}
        </div>
        <div class="col-sm-4">
            <p>Average cube scores:</p>
            {Square_Table_Tele.to_html(classes='table', header="true", index=False)}
        </div>
        <div class="col-sm-4">
            <p>Average community scores:</p>
            {ChargeStation_table_Tele.to_html(classes='table', header="true", index=False)}
        </div>
    </div>
    
    <h1>EndGame</h1>
    <img src="{path}/teleop_parked_docked_engaged.png" alt="Teleop Parked/Docked/Engaged">
    <br>
    <p>Comments:</p>
    <div style="height:250px;width:500px;border:1px solid #4e4e4e;font:16px Arial, Serif;overflow:auto;">
        <p>{comments_str}</p>
    </div>
</div>
<br>
</body>
</html>

            '''



html_file_name = str(team_number) +'_report.html'


save_path_c = os.path.join("save_path",html_file_name)
print(save_path_c)
with open(save_path_c, 'w') as f:
    f.write(html)


# open HTML file
webbrowser.open('file://' + os.path.realpath(save_path_c))