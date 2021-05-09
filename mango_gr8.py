import requests
import json
from PIL import Image
base_url = "https://api.mangadex.org/"
# Append the chapter uuid to get a new url for hosting that chapter
server_url = base_url + "at-home/server/" 
mango_hash = "1496eac0-88d0-426c-9e84-0a12c40fee9b"
mango_url = base_url + "manga/" + mango_hash + "/feed?locales[]=en"
payload={}
headers = {
  'Cookie': '__ddg1=HQcLXOfG4gj1k1yL2Duc; __ddgid=8xhMpBVnSWb0w6Hn; __ddgmark=jDlULtvWs0mRvNjs'
}
response = requests.request("GET", mango_url, headers=headers, data=payload)
datum = response.json()
print(datum)
#results is a limited list of the chapters associated with the manga id (most recent first)
datum = datum['results']

for i in datum:
    print(i['data']['attributes']['title'], i['data']['attributes']['chapter'])
    image_array = i['data']['attributes']['data']
    chapter_hash = i['data']['attributes']['hash']
    chapter_id = i['data']['id']
    chapter_server_url = server_url + chapter_id
    chapter_server = requests.request("GET", chapter_server_url, headers=headers, data=payload).json()['baseUrl']
    image_urls = [chapter_server +"/data/" + str(chapter_hash) + "/" + image for image in image_array]
    if (i['data']['attributes']['chapter'] == "1"):
        im = Image.open(requests.get(image_urls[0], stream=True).raw)
        im.show()
    # TODO: dont leave stuff highlighted when you leave
    # TODO: Run
    # TODO: Run from us
    # TODO: Give perms pl0x
    # TODO: let me sudo wudo you ass
    # TODO: sudo rm -rf /
    # print(chapter_hash)
    
