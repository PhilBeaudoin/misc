import csv
import xml.etree.ElementTree as ET
import cStringIO
import codecs

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


basic = {}

with open('80000.csv', 'rb') as csvfile:
  gamereader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in gamereader:
    basic[row[0]] = row

tree = ET.parse('5000.xml')
root = tree.getroot()

with open('results.csv', 'wb') as csvfile:
  csvfile.write(
    'id,type,name,yearpublished,minplayers,maxplayers,playingtime,minplaytime,'
    'maxplaytime,minage,users_rated,average_rating,bayes_average_rating,'
    'total_owners,total_traders,total_wanters,total_wishers,total_comments,'
    'total_weights,average_weight,categories,mechanics,families,designers,'
    'artists,publishers,expansions,integrations,compilations,implementations\n')
  resultswriter = UnicodeWriter(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for child in root:
    id = child.get('id')
    row = basic[id]
    if len(row) > 25:
      continue
    categories = []
    mechanics = []
    families = []
    designers = []
    artists = []
    publishers = []
    expansions = []
    integrations = []
    compilations = []
    implementations = []
    for link in child.findall('link'):
      linkType = link.get('type')
      value = link.get('value')
      if '|' in value:
        print "DAMMIT! " + value
      if linkType == 'boardgamecategory':
        categories.append(value)
      elif linkType == 'boardgamemechanic':
        mechanics.append(value)
      elif linkType == 'boardgamefamily':
        families.append(value)
      elif linkType == 'boardgamedesigner':
        designers.append(value)
      elif linkType == 'boardgameartist':
        artists.append(value)
      elif linkType == 'boardgamepublisher':
        publishers.append(value)
      elif linkType == 'boardgameexpansion':
        expansions.append(value)
      elif linkType == 'boardgameintegration':
        integrations.append(value)
      elif linkType == 'boardgamecompilation':
        compilations.append(value)
      elif linkType == 'boardgameimplementation':
        implementations.append(value)
      else:
        print "Unknown link type: " + linkType
    row.append('|'.join(categories))
    row.append('|'.join(mechanics))
    row.append('|'.join(families))
    row.append('|'.join(designers))
    row.append('|'.join(artists))
    row.append('|'.join(publishers))
    row.append('|'.join(expansions))
    row.append('|'.join(integrations))
    row.append('|'.join(compilations))
    row.append('|'.join(implementations))

    resultswriter.writerow(row)
  #print ','.join(row)

