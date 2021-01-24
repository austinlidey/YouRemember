import requests

#################################################################
#  Code to read URL from data file provided by DataScraper.py   #
#################################################################
url_list = []

input = open("playlistDetails.txt", "r")

loopCounter = 1
lastURL = 0
for x in input:
    url_raw = ""
    if loopCounter == 2 or loopCounter - 3 == lastURL: # add to list
        lastURL = loopCounter
        url_raw += x
        url_list.append(url_raw)

    loopCounter += 1

input.close()

hot_urls = []
for x in url_list:
    link = x.replace('\n', '')
    newURL = ''
    newURL += 'https://i.ytimg.com/vi/' + link + '/mqdefault.jpg'

    hot_urls.append(newURL)

#############################################################
#  Code to save the image to specified directory using URL  #
#############################################################
imagedlCounter = 1
for x in hot_urls:
    url = x
    image = requests.get(url)
    path = 'images/image' + imagedlCounter.__str__() + '.jpg'

    with open(path, 'wb') as f:
        f.write(image.content)
    print('file {} downloaded'.format(imagedlCounter))
    imagedlCounter+=1

print('All images downloaded successfully!')

