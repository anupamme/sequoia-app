import json

if __name__ == "__main__":
    # read image recognition from metamind output. in that there is user_value which is a url, find in the insta output which standard_resolution.url has the same output. match them. match the tags vs labels (from metamind)
    images = json.loads(open('img.json', 'r').read())
    insta = json.loads(open('out.json', 'r').read())
    for image in images:
        link = image['user_value']
        for metaitem in insta:
            val = insta[metaitem]['data']
            for item in val:
                candidate = item['images']['standard_resolution']['url']
                if link == candidate:
                    tags = item['tags']
                    image['tags'] = tags
    f = open('with-tags.json', 'w')
    f.write(json.dumps(images))
    f.close()
        
    