import urllib
import json
import MySQLdb
import sys
import time
from random import randint
from datetime import datetime
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')
reload(sys)
sys.setdefaultencoding('utf-8')

while True:
  try:
    conn = MySQLdb.connect(host=parser.get('MySQL', 'host'), user=parser.get('MySQL', 'username'), passwd=parser.get('MySQL', 'password'), db=parser.get('MySQL', 'db'))
    x = conn.cursor()

    request  = urllib.urlopen("https://www.guloggratis.dk/modules/gg_app/public/search/result/")
    response = request.read()
    data = json.loads(response)

    for obj in data['results']:
      timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      x.execute("""INSERT IGNORE INTO articles VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (obj['id'], obj['creationDate'], obj['lastUpdate'], obj['header'], obj['price'], obj['shortDescription'], obj['ad_link'], obj['zipcode'], obj['city'], obj['imageSrc'], obj['location'], timestamp))
      conn.commit()
#debug stuff
#      print obj['id']
    conn.close()
  except IOError:
    pass
  except ValueError:
    pass
  except LookupError:
    pass
  except:
    pass
  #random timer between each check
  time.sleep(randint(18, 22)) 
