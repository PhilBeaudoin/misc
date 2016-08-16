import random
import numpy	

# What's in the bag at the beginning.
# 0,1,2 = color 0,1,2
# 3 = black/crash
initBagCounts = [5, 5, 5, 12]

# The position of each of the three markers at the beginning.
initPos = [0, 0, 0, 3]

# The value of shares at each position.
shareValue = [0, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]

# The crash level at each round.
crash = [-5, -7, -10, -20]

# The delta for each share color and the crash marker.
#deltas = [[0, 2, 4, 7], [0, 2, 4, 7], [0, 2, 4, 7], [0, 1, 2, 4]]  # 3 players
#deltas = [[0, 1, 3, 6], [0, 1, 3, 6], [0, 1, 3, 6], [0, 1, 2, 3]]  # 4 players
deltas = [[0, 1, 2, 4, 7], [0, 1, 2, 4, 7], [0, 1, 2, 4, 7], [0, 1, 1, 2, 3]]  # 5 players

# The number of trials. Increase to reduce noise.
numTrials = 1
#numTrials = 10000

# Number of rounds in the game.
numRounds = 4

# Moves per round
#movesPerRound = 6 * 3  # 3 player game.
#movesPerRound = 6 * 4  # 4 player game.
movesPerRound = 6 * 5  # 5 player game.

# A result is:
# {final:  [f0, f1, f2, f3],
#  maxVal: [m0, m1, m2, m3],
#  crash:  [c0, c1, c2, c3],
#  totalCrashes: t,
#  finalStd: s,
#  num: n}

# Results is a list containing one result per trial.
results = []

def appendToBag(bag, counts):
	for i in xrange(4):
		bag += [i] * counts[i]
	random.shuffle(bag)
# The trials.
for trial in xrange(numTrials):
	pos = initPos + []
	numCrash = [0,0,0,0]
	bag = []
	appendToBag(bag, initBagCounts)
	out = [0,0,0,0]
	maxVal = [0,0,0,0]
	n = 0
	for round in xrange(numRounds):
		for move in xrange(movesPerRound):
			draw = bag.pop()
			out[draw] += 1
			if out[draw] == len(deltas[draw]) - 1:
				for i in xrange(4):
					pos[i] = max(0, pos[i] + deltas[i][out[i]])
				for i in xrange(3):
					if pos[i] >= pos[3]:
						pos[i] = max(0, pos[i] + crash[round])
						numCrash[round] += 1
				print pos
				print numCrash
				# Remove a crash token.
				out[3] = max(0, out[3] - 1)
				appendToBag(bag, out)
				out = [0,0,0,0]
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