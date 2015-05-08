import metamind
from metamind.api import set_api_key, general_image_classifier
import json

apiKey = 'd2TshfVAyBuTqRnCto5aDay1XsZOTd0CEhIOZNKEPuCMRlNde0'

if __name__ == "__main__":
    set_api_key(apiKey)
    res = json.loads(open('out.json', 'r').read())
    urlRes = []
    for date in res:
        val = res[date]['data']
        for item in val:
            if len(item['tags']) > 0:
                #print 'non-empty tags found: ' + str(item['tags'])
                #print 'image: ' + item['images']['standard_resolution']['url']
                urlRes.append(item['images']['standard_resolution']['url'])
    imgTag = general_image_classifier.predict(urlRes, input_type='urls')
    f = open('img.json', 'w')
    f.write(json.dumps(imgTag))
    f.close()
        