# -*- coding: utf-8 -*-
import os
import pymongo
from base64 import b64encode
import requests
import lxml.html as H
from html2text import html2text
import time
import random
import json
from cStringIO import StringIO as BytesIO
import Image


def move_pictures():
    #pic_dir = "pictures\\full"
    pic_dir = "pictures\\thumbs\\big"
    pics = [ pic for pic in os.listdir(pic_dir) 
            if pic.endswith(".jpg")]
    for pic in pics:
        sub_dir = pic[:2]
        new_dir = os.path.join(pic_dir, sub_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        old_path = os.path.join(pic_dir, pic)
        new_path = os.path.join(pic_dir, os.path.join(sub_dir, pic))
        try:
            os.rename(old_path, new_path)
        except:
            if os.path.exists(new_path):
                os.remove(old_path)

def update_data():
    connection = pymongo.Connection('localhost', 27017)
    db = connection['douban_group']
    collection = db['haixiuzu']
    i = 0
    for one in collection.find():
        #i = i + 1
        #if i > 3:break
        update_flag = False
        _id = one['_id']
        print _id
        images = one['images']
        #print '-' * 80
        #print images
        for x in range(len(images)):
            path = images[x]['path']
            if not os.path.exists(os.path.join('pictures', path)):
                update_flag = True
                sub_dir = path.split('/')[1][:2]
                file_name = path.split('/')[1]
                new_path = "full/%s/%s" % (sub_dir, file_name)
                images[x]['path'] = new_path
        #print '-' * 80
        #print images
        if update_flag:
            print "-----------update------------"
            collection.update({"_id":_id}, {"$set":{"images":images}})
                
def check_empty_images():
    connection = pymongo.Connection('localhost', 27017)
    db = connection['douban_group']
    collection = db['haixiuzu']
    for one in collection.find():
        _id = one['_id']
        if not one.has_key("images"):
            print "not has image keys:", _id
            #collection.remove({"_id":_id})
        else:
            images = one['images']
            if len(images) == 0:
                print "need to download again:", _id


def get_author_loc(db, author_url):
    loc = "Uknown"
    # first, find in db
    item = db.find_one({"author_url":author_url,"loc":{"$exists":True}, "loc":{"$ne":""}})
    if item:
        print "got from local:", author_url
        return item["loc"]

    time.sleep(random.randrange(2,3))
    while True:
        try:
            print "begin to fetch url:", author_url
            #response = requests.get(author_url, headers=headers)
            response = requests.get(author_url)
        except:
            print "an error occured"
            time.sleep(random.randrange(3,5))
            continue
        if not response.ok:
            print "response status is wrong."
            response.close()
            time.sleep(random.randrange(3,5))
            continue
        response.close()
        break
    doc = H.document_fromstring(response.text)
    l = doc.xpath('//div[@class="mod user-card"]/div[2]/ul[1]/li[2]')
    if len(l) == 0:
        # people deleted by douban
        return "Dead"
    loc_html = l[0].text_content()
    loc = html2text(loc_html).strip('\r\n\t ')
    if loc == "":
        loc = "Uknown"
    else:
        loc = html2text(loc_html).strip('\n ')
    if loc != "Uknown":
        print "got :", author_url
    return loc

def check_loc():
    connection = pymongo.Connection('localhost', 27017)
    collection = connection['douban_group']
    db = collection['haixiuzu']
    #cur = db.find({"loc":{"$exists":0}}).sort("_id", pymongo.DESCENDING)
    cur = db.find({"loc":""}).sort("_id", pymongo.DESCENDING)
    for one in cur:
        loc = get_author_loc(db, one['author_url'])
        if loc == "Error":
            continue
        db.update({"author_url":one['author_url']}, {"$set":{"loc":loc}}, multi=True)

#72579103 
def test():
    connection = pymongo.Connection('localhost', 27017)
    db = connection['douban_group']
    collection = db['haixiuzu']
    #collection.update({"_id":"72579103"}, {"$unset":{"loc":1}}, False, True)
    collection.update({"author_url":"http://www.douban.com/group/people/77287752/"}, {"$set":{"loc":"wlmq"}})


def thumb_pic(image, size):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, image)
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.copy()
    image.thumbnail(size, Image.ANTIALIAS)
    return image

def dump_data():
    connection = pymongo.Connection('localhost', 27017)
    collection = connection['douban_group']
    db = collection['haixiuzu']
    cur = db.find().sort("_id", pymongo.DESCENDING).limit(50)
    obj = json.loads('{ "data":[], "download":"downloadfile.gz", "thumb":{ "max":[267, 200], "min":[150, 112] }, "blur":[600, 336] }')
    for item in cur:
        if not item.has_key('images'):
            #print item['_id']
            continue
        for image in item['images']:
            data = json.loads('{ "blur":"", "img":[ "", [500, 648] ], "thumb":[ "", [150, 200] ] }')
            pic_path = "/pictures/" + image['path']
            thumb_path = "/pictures/thumbs/" + image['path'].replace('full', 'big')
            img = Image.open(BytesIO(open(pic_path[1:], "rb").read()))
            _size = list(img.size)
            data['img'][0] = pic_path
            data['img'][1] = _size
            data['thumb'][0] = thumb_path
            obj['data'].append(data)
            # if thumb doesn't exists, create it.
            if not os.path.exists(thumb_path[1:]):
                thumb_img = thumb_pic(img, (150, 200))
                thumb_dir = os.path.dirname(thumb_path[1:])
                if not os.path.exists(thumb_dir):
                    print "create directory:", thumb_dir
                    os.mkdir(thumb_dir)
                thumb_img.save(open(thumb_path[1:], "wb"), "JPEG")
    open("gallary/data.json", "w").write(json.dumps(obj, indent=4, separators=(',', ': ')))




if __name__ == '__main__':
    #get_author_loc("http://www.douban.com/group/people/mktime/")
    #check_empty_images()
    #check_loc()
    #test()
    dump_data()
