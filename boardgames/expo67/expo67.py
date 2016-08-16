from random import shuffle

numValues = 21
numColors = 3
numPavillion = 6
numPlayers = 4
cardsPerHand = 10


deck = []
for i in range(numValues):
  for c in range(numColors):
    deck.append({'val': i, 'col':c})
shuffle(deck)

def numHourglasses(card):
  return int(card['val'] / 3)

def printCard(card):
  print 'Value: ' + str(card['val']) + '  Color: ' + str(card['col'])

def printDeck(deck):
  for card in deck:
    printCard(card);

printDeck(deck)

objectives = []
for i in range(numPavillion):
  objectives.append(i)
shuffle(objectives)

players = []
for i in range(numPlayers):
  players.append({'hand': deck[-cardsPerHand], 'objective': objectives[i]})
  deck = deck[:-cardsPerHand]

pavillions = []
for i in range(numPavillion):
  pavillions.append({'numCards': 0, 'topCard': None, 'color': i % numColors})
