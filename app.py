from flask import Flask, render_template
import json
from collections import OrderedDict
import requests
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
    returns the url to get list of 100 mango
    can take in a starting offset and an array of tag hashes
    """
    url = base_url + "manga/" + mango_hash + "/feed?locales[]=en"
    return url
    
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
    # print("test")
    return render_template("index.html")

@app.route('/mango/<int:offset>')
def mango(offset):
    url = mango_list_url(offset=offset)
    result = requests.request("GET", url).json()['results']

    return render_template("list.html", results = result, offset = offset)

@app.route('/mango_page/<string:mango_hash>')
def mango_page(mango_hash):
    url = view_mango(mango_hash)
    result = requests.request("GET", url).json()['results']
    # aList = json.dumps(jsonString)
    
    return render_template("mango.html", results = result)




@app.route('/tags')
def tags():
    return str(tag_data)
app.run(debug=True)