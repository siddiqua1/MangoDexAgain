
import os,json,requests
from flask import Flask, render_template, request
from collections import OrderedDict

app = Flask(__name__)

base_url = "https://api.mangadex.org/"
# Append the chapter uuid to get a new url for hosting that chapter
server_url = base_url + "at-home/server/" 
mango_hash = "1496eac0-88d0-426c-9e84-0a12c40fee9b"
mango_url = base_url + "manga/" + mango_hash + "/feed?locales[]=en"

def mango_list_url(offset=0, tags = []):
    """
    returns the url to get list of 100 mango
    can take in a starting offset and an array of tag hashes
    """
    url = base_url + "manga?limit=100&offset=" + str(offset)
    for tag in tags:
        url += "&includedTags[]=" + str(tag)
    return url

def view_mango(mango_hash):
    """
    returns the url to get feed for a given mango
    english is the best language
    """
    url = base_url + "manga/" + mango_hash + "/feed?locales[]=en"
    return url

def mango_meta(mango_hash):
    """
    returns the url to get descriptor for a given mango
    """
    url = base_url + "manga/" + mango_hash
    return url


def get_server(chap_id):
    """
    returns the url to server to retrieve chap from
    """
    url = server_url + chap_id
    result = requests.request("GET", url).json()['baseUrl']
    return result
def get_pages(chap_hash):
    """
    returns the filenames of the pages in a given chapter
    """
    url = base_url + 'chapter/' + chap_hash
    pages = requests.request("GET", url).json()
 
    return pages['data']['attributes']['data'], pages['data']['attributes']['hash'], pages['relationships'][1]['id']

def get_images(server,chap_hash,images):
    """
    returns an array of the urls in a given chapter when provided the mangodex at home server, 
    chapter hash and the file names of the images
    Make sure to pass in the data-saver array for the images
    """
    chapter=[]
    url = server+"/data/"+chap_hash
    for i in images:
        page=url+'/'+i
        chapter.append(page)
    return chapter

def get_img_preview(server,chap_hash,images,m=1):
    """
    returns a url for the [m] image of the chapter when provided
    the mangodex at home server, chapter hash and the file names of the images
    """

    url = server+"/data-saver/"+chap_hash
    page=url+'/'+images[m]

    return page

f = open("tags.json", "r")

mango_tags=json.loads(f.read())
tag_data={}
for i in mango_tags:
    tag_id=i['data']['id']
    tag_title= i['data']['attributes']['name']['en']
    tag_data[tag_title]=tag_id
tag_data= OrderedDict(sorted(tag_data.items()))    


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mango/<int:offset>/<string:tag>')
def mango(offset, tag=None):
    tags = []
    if (tag != None):
        tags.append(tag)
    url = mango_list_url(offset=offset,tags=tags)
    result = requests.request("GET", url).json()['results']

    return render_template("list.html", results = result, offset = offset, tag=tag)

@app.route('/mango/<int:offset>')
def mango_no_tag(offset):
    url = mango_list_url(offset=offset)
    result = requests.request("GET", url).json()['results']

    return render_template("list.html", results = result, offset = offset)

@app.route('/mango_page/<string:mango_hash>')
def mango_page(mango_hash):
    url = view_mango(mango_hash)
    #data for chapter 
    result = requests.request("GET", url).json()['results']

    #meta data for the manga
    meta = requests.request("GET", mango_meta(mango_hash)).json()
    print(mango_meta(mango_hash))
    #image preview for mango (generally page two of the first chapter)
    #use data saver version
    preview = 0
    if len(result) > 0:
        chapter1 = result[-1]['data']
        server = get_server(chapter1['id'])
        preview = get_img_preview(server,chapter1['attributes']['hash'],chapter1['attributes']['dataSaver'] ,m=0)
    return render_template("mango.html", results = result, meta=meta, preview=preview)

@app.route('/chapter/<string:chap_id>')
def chapter_loader(chap_id):
    data, chap_hash, mango_id = get_pages(chap_id)
    server = get_server(chap_id)
    images = get_images(server,chap_hash,data)
    
    return render_template("chapter.html",images=images, mango_id=mango_id)

@app.route('/tags')
def tags():
    return render_template("tag.html",tags=tag_data)

@app.route('/test')
def adhoc_test():
    return request.query_string


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True)
  #app.run(host = '0.0.0.0', port = port)