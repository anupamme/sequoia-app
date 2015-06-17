import urllib2
import datetime
import time
import json
import calendar
from geopy.distance import vincenty

baseApi = 'https://api.instagram.com/v1/tags/'
subApi = '/media/recent?'
clientId = 'ef63de4634b344e3856b4f4138a8db56'
count = 40
bali_loc = (-8.65, 115.2167)
bali_tourist = ['waterbom', 'sekumpul', 'menjangan', 'scuba', 'jatiluvih', 'tirta', 'tanah', 'kawi', 'shipwreck', 'arma', 'agung', 'uluwatu']
#bali_tourist = ['waterbom']
'''
algorithm for tourist attractions: 
1. call the tags search api with tag names of the correct places.
2. from the results filter out the results which:
2.a. dont have bali in the tags and in the location.
2.b. has 0 likes.
3. keep the unfiltered images urls in one place. And keep the count.
4. If count > 100 then exit else goto next pagination url.

algorithm for hotel amenities:
1. divide hotel into amenities (could be specific per hotel). Define the list of amenities.
2. find tags for each amenity.
3. do search for images with tag == hotelname
    for these images search if they have any of the available amenity tag. Or find word distance with these. And thus find the most probable amenity given tags.
4. thus find images per amenity per hotel.

'''


def callApi(tagname):
    searchStr = baseApi + tagname + subApi + 'client_id=' + clientId + '&count=' + str(count)
    print(searchStr)
    response = urllib2.urlopen(searchStr)
    res = json.loads(response.read())
    return res

def testWhetherValid(tags, loc, likes):
    for tag in tags:
        if 'bali' == tag.lower():
            return True
    if loc is not None:
        local_lat = loc['latitude']
        local_long = loc['longitude']
        if local_lat is not None and local_long is not None:
            local_loc = (local_lat, local_long)
            distance = vincenty(local_loc, bali_loc).miles
            if distance < 5.0:
                return True
    return False

def findTouristAttractions(tagname):
    metaResult = []
    tagResult =  callApi(tagname)
    # filter the results from tags and recall the api with pagination.
    nextUrl = tagResult['pagination']['next_url']
    data = tagResult['data']
    for ele in data:
        tags = ele['tags']
        loc = ele['location']
        likes = ele['likes']
        isValid = testWhetherValid(tags, loc, likes)
        if isValid:
            image = ele['images']['low_resolution']['url']
            metaResult.append(image)
    return metaResult

if __name__ == "__main__":
    result = {}
    for destination in bali_tourist:
        result[destination] = findTouristAttractions(destination)
    f = open('out-tourist.json', 'w')
    f.write(json.dumps(result))
    f.close()