import random
import numpy	

# The position of each of the three markers at the beginning.
initPos = [0, 0, 0, 3]

# The value of shares at each position.
shareValue = [0, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]

# The crash level at each round.
crash = [-5, -7, -10, -20]

# The delta for each share color and the crash marker.
# N players?
deltas = [
  [1, 2, 3],
  [1, 2, 3],
  [1, 2, 3],
  [2, 1, 0]
]

# The number of trials. Increase to reduce noise.
numTrials = 1
#numTrials = 10000

# Number of rounds in the game.
numRounds = 4

# Moves per round
#movesPerRound = 6 * 3  # 3 player game.
#movesPerRound = 6 * 4  # 4 player game.
movesPerRound = 6 * 5  # 5 player game.

# The dies
dies = [
  [ {'type': 'PROGRESS', 'color': 0}, {'type': 'PROGRESS', 'color': 1}, {'type': 'PROGRESS', 'color': 2},
    {'type': 'PROGRESS', 'color': 3}, {'type': 'ADVANCE', 'color': 3}, {'type': 'ADVANCE', 'color': 3} ],
  [ {'type': 'ADVANCE', 'color': 0}, {'type': 'ADVANCE', 'color': 1}, {'type': 'ADVANCE', 'color': 2},
    {'type': 'ADVANCE', 'color': 0}, {'type': 'ADVANCE', 'color': 1}, {'type': 'ADVANCE', 'color': 2} ],
]

# A result is:
# {final:  [f0, f1, f2, f3],
#  maxVal: [m0, m1, m2, m3],
#  crash:  [c0, c1, c2, c3],
#  totalCrashes: t,
#  finalStd: s,
#  num: n}

# Results is a list containing one result per trial.
results = []

# The trials.
for trial in xrange(numTrials):
	pos = initPos + []
	numCrash = [0,0,0,0]
	bag = []
	deltaPos = [0,0,0,0]
	maxVal = [0,0,0,0]
	n = 0
	for round in xrange(numRounds):
		for move in xrange(movesPerRound):
			for dice in dies:
				diceResult = random.choice(dice)
				color = diceResult['color']
				if diceResult['type'] == 'PROGRESS':
					deltaPos[color] = min(len(deltas[color]) - 1, deltaPos[color] + 1)
				else:
					pos[color] += deltas[color][deltaPos[color]]
				for i in xrange(3):
					if pos[i] >= pos[3]:
						pos[i] = max(0, pos[i] + crash[round])
						numCrash[round] += 1
				print pos
				n += 1
				maxVal = [max(a,b) for (a,b) in zip(maxVal, pos)]
	results.append({
		'final': pos,
		'maxVal': maxVal,
		'crash': numCrash,
		'totalCrashes': sum(numCrash),
		'finalStd': numpy.std(pos[0:3]),
		'num': n})

finals = [result['final'] for result in results]
maxVals = [result['maxVal'] for result in results]
crashes = [result['crash'] for result in results]
totalCrashes = [result['totalCrashes'] for result in results]
finalStds = [result['finalStd'] for result in results]
nums = [result['num'] for result in results]

def printAll(fun):
	print '  Final: '
	print [fun(l) for l in zip(*finals)]
	print '  Max: '
	print [fun(l) for l in zip(*maxVals)]
	print '  Crash: '
	print [fun(l) for l in zip(*crashes)]
	print '  Total Crashes: '
	print fun(totalCrashes)
	print '  StdDev: '
	print fun(finalStds)
	print '  Number of fill: '
	print fun(nums)

print 'MEANS'
printAll(numpy.mean)