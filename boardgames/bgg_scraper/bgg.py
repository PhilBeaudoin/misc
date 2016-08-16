import csv
import urllib2
import xml.etree.ElementTree as ET

#tree = ET.parse('country_data.xml')
#root = tree.getroot()

result = ET.fromstring('<items></items>')

with open('80000.csv', 'rb') as csvfile:
  gamereader = csv.reader(csvfile, delimiter=',', quotechar='"')
  i = 0;
  req = []; 
  for row in gamereader:
    i += 1
    if i > 20000:
      f = open('result.xml', 'w')
      f.write(ET.tostring(result))
      break
    req.append(row[0])
    if i % 50 == 0:
      url = 'http://www.boardgamegeek.com/xmlapi2/thing?id=' + ','.join(req)
      print url
      req = []
      response = urllib2.urlopen(url)
      responseText = response.read()
      xml = ET.fromstring(responseText)
      for child in xml:
        result.append(child)

