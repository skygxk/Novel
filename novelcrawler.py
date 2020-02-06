# -*- coding:utf-8 -*-
# crawl the novels from http://www.xbiquge.la/
import requests
import os
import json
import signal
import time
import multiprocessing as mp
import htmlparser as hp

# get the html from the url
def __get_html(url):
    respone = requests.get(url)
    html = respone.content.decode('utf-8')
    if hp.is_error(html):
        return __get_html(url)
    return html

# append a new chapter and to the existed novel update the current url
def __update_novel(name, title, text, url):
    # file writing lock
    __psbusy[name] = True
    path = './Novels/' + name + '/'
    if not os.path.exists(path):
        print(r'The novel does not exist!')
    else:
        contents = []
        chapter = '\n' + title + text
        # append chapter
        with open(path + name + '.txt', 'a', encoding='utf-8') as fout:
            fout.write(chapter)
        # get contents
        with open(path + 'contents.json', 'r', encoding='utf-8') as fin:
            contents = json.loads(fin.read())
        # append contents
        with open(path + 'contents.json', 'w', encoding='utf-8') as fout:
            content = {
                'title': title,
                'index': contents[-1]['index'] + contents[-1]['count'],
                'count': chapter.count('\n')
            }
            contents.append(content)
            fout.write(json.dumps(contents))
        with open(path + 'url', 'w', encoding='utf-8') as fout:
            fout.write(url)
        # file writing unlock
        __psbusy[name] = False

def __stop_handler(signum, frame):
    for key in __psbusy:
        if __psbusy[key] == True:
            time.sleep(0.001)
            os.kill(os.getpid(), signal.SIGINT)
            return
    print(r'The crawler is stopped!')
    exit(0)

# whether there is a file writing in the process
__psbusy = {'name': False}

signal.signal(signal.SIGINT, __stop_handler)

# crawl a new novel by its url of the first chapter
def crawl(url):
    html = __get_html(url)
    name = hp.get_name(html)
    path = './Novels/' + name + '/'
    if os.path.exists(path):
        print('The novel has already existed! You can update it.')
    else:
        os.makedirs(path)
        with open(path + name + '.txt', 'w', encoding='utf-8') as fout:
            fout.write(name)
        with open(path + 'contents.json', 'w', encoding='utf-8') as fout:
            contents = [{
                'title': name,
                'index': 0,
                'count': 1
            }]
            fout.write(json.dumps(contents))
        # initialize the novel by the first chapter
        html = __get_html(url)
        __update_novel(name, hp.get_title(html), hp.get_text(html), url)
        print(name + ' ' + hp.get_title(html) + ' is crawled...')
        # start to continuous crawl
        update(name)

# update an existed novel by its name
def update(name=''):
    # update all novels by multiprocessing
    if(name==''):
        ps = []
        names = os.listdir('./Novels/')
        for name in names:
            p = mp.Process(target=update, args=(name,))
            ps.append(p)
        for index in range(len(names)):
            ps[index].start()
        return
    # update selected novel
    path = './Novels/' + name + '/'
    url = ''
    if not os.path.exists(path):
        print('The novel does not exist!')
    else:
        # access url
        with open(path + 'url', 'r', encoding='utf-8') as fin:       
            url = fin.read()
        # crawl chpaters until to an end
        html = __get_html(url)
        url = hp.get_url(html)
        while not hp.is_over(html):
            html = __get_html(url)
            __update_novel(name, hp.get_title(html), hp.get_text(html), url)
            print(name + ' ' + hp.get_title(html) + ' is crawled...')
            url = hp.get_url(html)
        print('Update ' + name + '!')
