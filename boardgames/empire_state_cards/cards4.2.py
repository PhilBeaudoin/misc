import random
import numpy	

# Res 0: Main resouce of company
# Res 1: Second resouce wrt company
# Res 2: Third resouce wrt company
# Res 3: Money on company
# Res -1: Reshuffle
# Redraw: Bitfield to indicate redraw

R1 = 1
R2 = 2
R3 = 4
R4 = 8

cards = [ 
  {'res': 3, 'val': 4, 'redraw': R1 | R2 | R3 | R4},
  {'res': 0, 'val': 5, 'redraw': R1 | R2 | R3 | R4},
  {'res': 3, 'val': 6, 'redraw': R1 | R2 | R3},
  {'res': 0, 'val': 6, 'redraw': R1 | R2 | R3},
  {'res': 1, 'val': 5, 'redraw': R1 | R3 | R4}, 
  {'res': 1, 'val': 3, 'redraw': R4},
  {'res': 2, 'val': 3, 'redraw': R2 | R3 | R4}, 
  {'res': 3, 'val': 3, 'redraw': R2 | R4}, 
  {'res': 0, 'val': 4, 'redraw': R2 | R4},
  {'res': 3, 'val': 3, 'redraw': R3 | R4},
  {'res': 3, 'val': 4, 'redraw': R3},
  {'res': 3, 'val': 4, 'redraw': R4} ]
#  {'res': -1, 'val': 0, 'redraw': 0} ]

# This indicates the round in which each builds happens
buildRound = [1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

# The number of builds in a game
numBuilds = 8

# The number of trials. Increase to reduce noise.
numTrials = 1
#numTrials = 10000

# A result is:
# [ {costs: [r0_0, r1_0, r2_0, r3_0], val: v_0, size: s_0}, 
#   {costs: [r0_1, r1_1, r2_1, r3_1], val: v_1, size: s_1}, ... ]
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
	random.shuffle(cards)
	cardsCopy = cards + []
	result = []
	stack = []
	for build in xrange(numBuilds):
		roundNumber = buildRound[build] - 1
		rep = 0
		while len(cardsCopy) > 0 and (len(stack) < 2 or stack[-1]['redraw'] & (1 << roundNumber)):
            # Guards against infinite loop
			rep += 1
			if (rep > 100) :
				print 'INFINITE LOOP!'
				print roundNumber
				print stack
				print cardsCopy
				exit()
			card = cardsCopy.pop()
			if card['res'] == -1:
				# Reshuffle and clear stack.
				cardsCopy = cardsCopy + stack
				random.shuffle(cardsCopy)
				stack = []
			else:
				stack.append(card)
		print stack
		val = stack[-1]['val']
		buildResult = {'costs': [0,0,0,0], 'val': val, 'size': len(stack)}
		for card in stack:
			buildResult['costs'][card['res']] += val
		result.append(buildResult)
		stack.pop()
	results.append(result)

def numMoves(costs):
	numForMoney = 0
	if costs[3] > 2 :
		if costs[3] < 7 :
			numForMoney= 1
		else:
			numForMoney = (costs[3]+1)/2 - 2
	return max(0, costs[0] - 2) + max(0, costs[1] - 2) + max(0, costs[2] - 2) + numForMoney

def doable(costs):
	if numMoves(costs) < 6:
		return 1
	else:
		return 0

# These arrays are of the form:
#   [ [x0, x1, x2, ...], ... ]
# Where x0 is the statistics on first build.
sizes = [[buildResult['size'] for buildResult in result] for result in results]
vals = [[buildResult['val'] for buildResult in result] for result in results]
totalCosts = [[sum(buildResult['costs']) for buildResult in result] for result in results]
doable = [[doable(buildResult['costs']) for buildResult in result] for result in results]

# Define these 4 statistics in one go:
# costOnRes[0], costOnRes[1], costOnRes[2], costOnRes[3]
costOnRes = [[[buildResult['costs'][res] for buildResult in result] for result in results] for res in xrange(4)]
costOnCubes = [[sum(buildResult['costs'][0:3]) for buildResult in result] for result in results]

def printAll(fun):
	print '  Sizes: '
	print [fun(l) for l in zip(*sizes)]
	print '  Doable: '
	print [fun(l) for l in zip(*doable)]
	print '  Vals: '
	print [fun(l) for l in zip(*vals)]
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

# print 'MINIMUM'
# printAll(min)

#print '25%'
#printAll(lambda l: numpy.percentile(l,25))

print 'MEANS'
printAll(numpy.mean)

#print 'MEDIANS'
#printAll(lambda l: numpy.percentile(l,50))

#print '75%'
#printAll(lambda l: numpy.percentile(l,75))

#print 'MAXIMUM'
#printAll(max)

#print results
#print doable
