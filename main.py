import GameModule
import PointsTracker
import UserInterface
import numpy as np
import matplotlib.pyplot as plt
import sys

team, year, player = UserInterface.getUserInput()

# get all plays and when they happened by player
plays = GameModule.getAllPlays(year, team)
all_plays_with_player = []
foul_plays_with_player = []
index = 0
for play in plays:
    if player in play:
        all_plays_with_player.append((play, index))
    if "END OF GAME" in play:
        all_plays_with_player.append((play, index))
        index = 0
    if "drawn by " + player in play:
        foul_plays_with_player.append((play, index))
    index += 1

# create points tracker, then iterate through games and handle where to add points
pt_tr = PointsTracker.PointsTracker(player)

foul_counter = 0
for play in all_plays_with_player:
    if play in foul_plays_with_player:
        foul_counter += 1
    if player + " makes " in play[0] or "free throw" in play[0]:
        if "free throw" in play[0]:
            if "misses" in play[0]:
                pt_tr.addPointsScored(foul_counter, 0, play[1], 1)
            else:
                pt_tr.addPointsScored(foul_counter, 1, play[1], 1)
        if "2-pt" in play[0]:
            if "misses" in play[0]:
                pt_tr.addPointsScored(foul_counter, 0, play[1], 0)
            else:
                pt_tr.addPointsScored(foul_counter, 2, play[1], 0)
        if "3-pt" in play[0]:
            if "misses" in play[0]:
                pt_tr.addPointsScored(foul_counter, 0, play[1], 0)
            else:
                pt_tr.addPointsScored(foul_counter, 3, play[1], 0)
    if "END OF " in play[0]:
        foul_counter = 0

ts_percentages, pts_scored, attempts, play_counts = pt_tr.getAveragePoints(
    False)

# output shot times (mean and standard deviation)
averages = []
std_devs = []
for (foul_number, play_times) in sorted(play_counts):
    average = round(np.average(np.array(play_times)), 1)
    std_dev = round(np.std(np.array(play_times)), 1)
    averages.append(average)
    std_devs.append(std_dev)

# plot data, shot attempts
#plt.subplot(3, 1, 1)
x_ts = np.arange(1, len(ts_percentages) + 1)
y_ts = np.array(ts_percentages)
plt.plot(x_ts, y_ts, 'ro')
plt.xticks(x_ts)
plt.yticks(np.arange(0, 1.5, step=0.2))
ind = 0
# for (a,b) in zip(x_ts, y_ts):
#    plt.text(a, b, attempts[ind])
#    ind += 1
plt.xlabel("Foul #")
plt.ylabel("TS% before Foul #")
plt.title("TS% vs # of Fouls on " + player + ", " + team + ", " + year)
plt.tight_layout()
plt.show()

#plt.subplot(3, 1, 2)
x_pt = np.arange(1, len(pts_scored) + 1)
y_pt = np.array(pts_scored)
plt.plot(x_pt, y_pt, 'bo')
plt.xticks(x_pt)
ind = 0
for (a, b) in zip(x_pt, y_pt):
    plt.text(a, b, attempts[ind])
    ind += 1
plt.xlabel("Foul #")
plt.ylabel("Pts Scored before Foul #")
plt.title("Pts Scored vs # of Fouls on " + player + ", " + team + ", " + year)
plt.tight_layout()
plt.show()


#plt.subplot(3, 1, 3)
x_fouls = np.arange(1, len(averages) + 1)
y_fouls = sorted(averages)
plt.errorbar(x_fouls, y_fouls, yerr=std_devs, linestyle='None', marker='o')
plt.xticks(x_fouls)
plt.xlabel("Foul #")
plt.ylabel("Average Plays before Foul #")
plt.title("Average Plays Finished vs # of Fouls on " +
          player + ", " + team + ", " + year)


plt.tight_layout()
plt.show()

print("Raw values for True Shooting: " + str(y_ts))
print("Raw values for Points Scored: " + str(y_pt))
print("Raw values for Average Plays until Foul: " + str(y_fouls))
