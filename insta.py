import urllib2
import datetime
import time
import json

clientId = 'ef63de4634b344e3856b4f4138a8db56'
city = "Bali"
subcity = "Ubud"
baliLat = '8.51'
baliLong = '115.239394'
distance = 1000


if __name__ == "__main__":
    # do instagram api call for bali location and get 10000 results.
    # for this make a call for 10 days (21/12/2014 to 1/1/2015) and get 100 results per day. So 1000 in total.
    # for each result, which has non-empty tags, make a call to metamind's image classifier.
    # keep a count of calls to metamind (1000 is the limit for the day)
    # emit tags vs metamind recognition for each result
    count = 0
    start = '22/12/2014'
    startDate = datetime.datetime.strptime(start, '%d/%m/%Y')
    mega = {}
    while count < 2 :
        nextDate = startDate + datetime.timedelta(days=1)
        minStamp = time.mktime(startDate.timetuple())
        maxStamp = time.mktime(nextDate.timetuple())
        searchStr = 'https://api.instagram.com/v1/media/search?lat=' + baliLat + '&lng=' + baliLong + '&client_id=' + clientId + '&MAX_TIMESTAMP=' + str(maxStamp) + '&MIN_TIMESTAMP=' + str(minStamp) + '&distance='  + str(distance) + '&count=10'
        print 'search-str: ' + searchStr
        response = urllib2.urlopen(searchStr)
        res = json.loads(response.read())
        mega[str(startDate)] = res
        print res['data'][0]
        count += 1
        startDate = nextDate
    f = open('out.json', 'w')
    f.write(json.dumps(mega))
    f.close()