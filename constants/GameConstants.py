#we will have more levels of blinds
#each of them lasting for 9 rounds
BIG_BLINDS = [10, 20, 30, 40, 50, 60, 80, 100, 150, 200]
HANDS_PER_ROUND = 9
MAX_PLAYERS = 9
HUMAN_PLAYER_INDEX = 0
HOLE_CARDS_PROBABILITIES = [[0.85, 0.68, 0.67, 0.66, 0.64, 0.63, 0.63, 0.62, 0.62, 0.62, 0.61, 0.60, 0.59],
                            [0.66, 0.83, 0.64, 0.64, 0.63, 0.61, 0.60, 0.59, 0.58, 0.58, 0.57, 0.56, 0.55],
                            [0.65, 0.62, 0.80, 0.61, 0.61, 0.59, 0.58, 0.56, 0.55, 0.55, 0.54, 0.53, 0.52],
                            [0.65, 0.62, 0.59, 0.78, 0.59, 0.57, 0.56, 0.54, 0.53, 0.52, 0.51, 0.50, 0.50],
                            [0.64, 0.61, 0.59, 0.57, 0.75, 0.56, 0.54, 0.53, 0.51, 0.49, 0.49, 0.48, 0.47],
                            [0.62, 0.59, 0.57, 0.55, 0.53, 0.72, 0.53, 0.51, 0.50, 0.48, 0.46, 0.46,	0.45],
                            [0.61, 0.58, 0.55, 0.53, 0.52, 0.50, 0.69, 0.50, 0.49, 0.47, 0.45, 0.43, 0.43],
                            [0.60, 0.57, 0.54, 0.52, 0.50, 0.48, 0.47, 0.67, 0.48, 0.46, 0.45, 0.43, 0.41],
                            [0.59, 0.56, 0.53, 0.50, 0.48, 0.47, 0.46, 0.45, 0.64, 0.46, 0.44, 0.42, 0.40],
                            [0.60, 0.55, 0.52, 0.49, 0.47, 0.45, 0.44, 0.43, 0.43, 0.61, 0.44, 0.43, 0.41],
                            [0.59, 0.54, 0.51, 0.48, 0.46, 0.43, 0.42, 0.41, 0.41, 0.41, 0.58, 0.42, 0.40],
                            [0.58, 0.54, 0.50, 0.48, 0.45, 0.43, 0.40, 0.39, 0.39, 0.39, 0.38, 0.55,	0.39],
                            [0.57, 0.53, 0.49, 0.47, 0.44, 0.42, 0.40, 0.37, 0.37, 0.37, 0.36, 0.35, 0.51]]