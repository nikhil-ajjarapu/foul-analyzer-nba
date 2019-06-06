def getUserInput():
    player = input(
        "Please enter the player's name with this format (for example, K. Durant): ")
    team = input(
        "Please enter the initals of the team of the player (for example, GSW): ")
    year = input(
        "Please enter which season (use the year with the playoff games) you would like to analyze (for example, 2019): ")
    return team, year, player
