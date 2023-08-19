from qiniu import Auth, BucketManager
import pickle
import cPickle
import requests
import json
import os
import shutil

ACCESS_KEY = "APPKEY"
SECRET_KEY = "SECRETKEY"
BUCKET = "YELLOW"


def main():
    items = []
    auth = Auth(ACCESS_KEY, SECRET_KEY)
    bucket = BucketManager(auth)
    data = bucket.list(BUCKET)
    if data[0].get("items"):
        items += data[0]['items']
    while data[0].get("marker") != None:
        print "fetch again:", data[0]["marker"]
        data = bucket.list(BUCKET, marker = data[0]["marker"])
        items += data[0]["items"]
    print "++++++++++++++++++++++++++++++++++++++++"
    print len(items), type(items[0]), type(items[len(items)-1])
    print "++++++++++++++++++++++++++++++++++++++++"
    print items[0]
    print "++++++++++ BEGING YELLOW ++++++++++"
    #for item in items:
    #    print item["key"]
    f = open("data.pk", "wb")
    pickle.dump(items, f)
    f.close()

def parse():
    f = open("data.pk", "r+")
    data = cPickle.load(f)
    #print type(data), len(data), data[0]
    domain = "http://7xjwhg.com1.z0.glb.clouddn.com"
    i = 0
    for item in data:
        i += 1
        if i % 500 == 0: 
            i = 0
            print "COUNT:", i
        url = domain + "/" + item["key"] + "?nrop"
        try:
            data = get_url_data(url)
        except:
            print "error occured:[%s]" % url
            continue
        if data["code"] != 0:
            print "nrop error", data["code"]
        else:
            info = data["fileList"][0]
            if info["label"] in (0,):
                got_yellow(info, item["key"])

def got_yellow(info, name):
    if name.find("/") != -1:
        name = name[name.find("/")+1:]
    path = "pictures/full/" + name[0:2] + "/" + name
    if os.path.exists(path):
        dst_path = "pictures/yellow/" + name
        if os.path.exists(dst_path):
            return
        print dst_path
        shutil.copy(path, dst_path)
    else:
        print "MISS:", path
    

def get_url_data(url):
    ret = requests.get(url)
    ret.close()
    return json.loads(ret.text)
    

if __name__ == '__main__':
    parse()
    #main()
