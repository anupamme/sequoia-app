import urllib2
import datetime
import time
import json
import calendar

clientId = 'ef63de4634b344e3856b4f4138a8db56'
city = "Bali"
subcity = "Ubud"
baliLat = '8.51'
baliLong = '115.239394'
distance = 1000
count = 100

def callApi(startStamp, endStamp):
    searchStr = 'https://api.instagram.com/v1/media/search?lat=' + baliLat + '&lng=' + baliLong + '&client_id=' + clientId + '&MAX_TIMESTAMP=' + str(endStamp) + '&MIN_TIMESTAMP=' + str(startStamp) + '&distance='  + str(distance) + '&count=10'
    print searchStr
    response = urllib2.urlopen(searchStr)
    res = json.loads(response.read())
    return res

if __name__ == "__main__":
    # call instagram api for 1 year for each month for 1st week.
    # compare the dates of creation for each month.
    start = '1/05/2014'
    startDate = datetime.datetime.strptime(start, '%d/%m/%Y')
    count = 0
    result = {}
    while count < 2:
        endDate = startDate + datetime.timedelta(days=3)
        minStamp = calendar.timegm(startDate.timetuple())
        maxStamp = calendar.timegm(endDate.timetuple())
        res = callApi(minStamp, maxStamp)
        result[str(startDate)] = res
        startDate = startDate + datetime.timedelta(days=30)
        count += 1
    f = open('out-y.json', 'w')
    f.write(json.dumps(result))
    f.close()