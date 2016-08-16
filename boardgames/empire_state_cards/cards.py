import random
import numpy	

# Res 0: Main resouce of company
# Res 1: Second resouce wrt company
# Res 2: Third resouce wrt company
# Res 3: Money on company
# Val = -1 : draw again

mainCard = {'res': 3, 'val': -1}

cardsA = [ 
  {'res': 0, 'val': -1}, {'res': 0, 'val': 4},
  {'res': 1, 'val': 3},
  {'res': 3, 'val': -1}, ]

cardsB= [ 
  {'res': 0, 'val': -1}, {'res': 0, 'val': 5},
  {'res': 1, 'val': -1},
  {'res': 2, 'val': 3}, 
  {'res': 3, 'val': 4}, ]

cardsC= [ 
  {'res': 0, 'val': -1},
  {'res': 1, 'val': 6},
  {'res': 2, 'val': -1}, {'res': 2, 'val': 4},
  {'res': 3, 'val': -1}, {'res': 3, 'val': 5}, ]

# The number of builds is the number of non-negative valued cards
numBuilds = 0
for card in cardsC + cardsB + cardsA:
  if card['val'] >= 0:
  	numBuilds += 1

# The number of trials. Increase to reduce noise.
numTrials = 1

# A result is:
# [ {costs: [r0_0, r1_0, r2_0, r3_0], size: s_0}, 
#   {costs: [r0_1, r1_1, r2_1, r3_1], size: s_1}, ... ]
# Where:
#  r0_0 is the cost of resource 0 on the first build
#  r1_0 is the cost of resource 1 on the first build
#  r0_1 is the cost of resource 0 on the second build
#  etc.

# Results is a list containing one result per trial.
results = []

# The trials.
for trial in xrange(numTrials):
	# Shuffle in-place, but since we always suffle it's all right.
	random.shuffle(cardsA)
	random.shuffle(cardsB)
	random.shuffle(cardsC)
	cards = cardsC + cardsB + cardsA
	result = []
	stack = [mainCard]
	for build in xrange(numBuilds):
		while stack[-1]['val'] == -1:
			if len(stack) == 7:
				# Reshuffle and clear stack.
				cards = cards + stack[1:]
				random.shuffle(cards)
				stack = [mainCard]
			else:
				stack.append(cards.pop())
		buildResult = {'costs': [0,0,0,0], 'size': len(stack)}
		val = stack[-1]['val']
		for card in stack:
			buildResult['costs'][card['res']] += val
		result.append(buildResult)
		stack.pop()
	results.append(result)

# These arrays are of the form:
#   [ [x0, x1, x2, ...], ... ]
# Where x0 is the statistics on first build.
sizes = [[buildResult['size'] for buildResult in result] for result in results]
totalCosts = [[sum(buildResult['costs']) for buildResult in result] for result in results]

# Define these 4 statistics in one go:
# costOnRes[0], costOnRes[1], costOnRes[2], costOnRes[3]
costOnRes = [[[buildResult['costs'][res] for buildResult in result] for result in results] for res in xrange(4)]
costOnCubes = [[sum(buildResult['costs'][0:3]) for buildResult in result] for result in results]

def printAll(fun):
	print '  Sizes: '
	print [fun(l) for l in zip(*sizes)]
	print '  Total cost: '
	print [fun(l) for l in zip(*totalCosts)]
	print '  Cost on cubes: '
	print [fun(l) for l in zip(*costOnCubes)]
	print '  Cost on money: '
	print [fun(l) for l in zip(*costOnRes[3])]
	print '  Cost on main resource: '
	print [fun(l) for l in zip(*costOnRes[0])]
	print '  Cost on second resource: '
	print [fun(l) for l in zip(*costOnRes[1])]
	print '  Cost on third resource: '
	print [fun(l) for l in zip(*costOnRes[2])]

# print 'Min'
# printAll(min)

# print '25%'
# printAll(lambda l: numpy.percentile(l,25))

# print 'MEDIANS'
# printAll(numpy.mean)

# print '75%'
# printAll(lambda l: numpy.percentile(l,75))

# print 'Max'
# printAll(max)

print results
