import numpy as np

class PointsTracker:
    def __init__(self, player_name):
        self.player_name = player_name
        self.avgs_tracker = {}
        self.foul_positions = []

    def getPlayerName(self):
        return self.player_name

    def addPointsScored(self, ind, num_points, score_index, free_throw_attempts):
        if ind not in self.avgs_tracker:
            self.avgs_tracker[ind] = [0, 0, 0, []]
        self.avgs_tracker[ind][0] += num_points
        self.avgs_tracker[ind][1] += 1
        self.avgs_tracker[ind][2] += free_throw_attempts
        self.avgs_tracker[ind][3].append(score_index)

    def getAveragePoints(self, print_or_not):
        ts_percentages = []
        attempts = []
        for avgs in self.avgs_tracker.values():
            if avgs[1] + avgs[2] > 0:
                ts_percentages.append(round(avgs[0] / (2 * (avgs[1] + 0.44 * avgs[2])), 4))
            else:
                ts_percentages.append(0)
            attempts.append(avgs[1])
        pts_scored = [lst[0] for lst in self.avgs_tracker.values()]
        if print_or_not:
            for i in range(len(ts_percentages)):
                print("TS% after Foul #" + str(i + 1) + ": " + str(ts_percentages[i]))
                print("Points after Foul #" + str(i + 1) + ": " + str(pts_scored[i]))
        temp_check = [(key, value[3]) for (key, value) in self.avgs_tracker.items()]
        return (ts_percentages, pts_scored, attempts, temp_check)
