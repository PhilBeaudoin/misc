#!/usr/bin/python

# Used to generate some sequences on OEIS.

input = [0,1,3,1,0,2,4,2,0]

def calcActives(input):
	actives = []
	line = 0
	while True:
		active = [i == line for i in input]
		if not True in active:
			return actives
		actives += [active]
		line += 1

def calcRanges(actives):
	ranges = []
	for a in actives:
		ranges += [(a.index(True), len(a) - 1 - a[::-1].index(True))]
	return ranges

def sortActives(actives, ranges):


def equiv(input):
	actives = calcActives(input)
	ranges = calcRanges(actives)
	allActives = [False] * len(input)
	activesStr = '     ' * len(input)
	firstStr = activesStr
	firstLineRanges = []
	for actives, r in zip(actives, ranges):
		for flr in firstLineRanges:
			if (r[0] <= flr[1] and flr[0] <= r[1]):
				print firstStr
				print activesStr
				print activesStr
				firstStr = activesStr
				firstLineRanges = []
				break
		firstLineRanges += [r]
		start = r[0]*5
		end = r[1]*5
		firstStr = firstStr[:start] + '*' * (end-start+1) + firstStr[end+1:]
		allActives = [a or aa for a, aa in zip(actives, allActives)]
		activesStr = ''.join([('*    ' if a else '     ') for a in allActives])
	print firstStr
	print activesStr
	print activesStr

equiv(input)
