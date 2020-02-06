import os
import json

# get the contents of the novel which name is in the settings.json
def get_contents():
    path = './Novels/' + get_settings('name') + '/contents.json'
    with open(path, 'r', encoding='utf-8') as fin:
        return json.loads(fin.read())

# get the lines of the novel which name is in the settings.json
def get_lines():
    path = './Novels/' + \
        get_settings('name') + '/' + get_settings('name') + '.txt'
    with open(path, 'r', encoding='utf-8') as fin:
        return fin.readlines()

# set the settings in the settings.json by key and value
def set_settings(key, value):
    settings = {}
    with open('./settings.json', 'r', encoding='utf-8') as fin:
        settings = json.loads(fin.read())
    with open('./settings.json', 'w', encoding='utf-8') as fout:
        settings[key] = value
        fout.write(json.dumps(settings))

# get the settings in the settings.json by key
def get_settings(key):
    with open('./settings.json', 'r', encoding='utf-8') as fin:
        return json.loads(fin.read())[key]

# set the markers of the novel which name is in the settings.json
def set_markers(markers):
    path = './Novels/' + get_settings('name') + '/markers.json'
    with open(path, 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(markers))

# get the markers of the novel which name is in the settings.json
def get_markers():
    markers = []
    path = './Novels/' + get_settings('name') + '/markers.json'
    if not os.path.exists(path):
        markers.append(0)
        with open(path, 'w', encoding='utf-8') as fout:
            fout.write(json.dumps(markers))
    with open(path, 'r', encoding='utf-8') as fin:
        return json.loads(fin.read())

# join the lines
def join_lines(lines, index, count):
    s = ''
    for i in range(index, index+count):
        s += lines[i]
    return s

# get the last chapter by the contents and the lines and markers.json, and update it
def get_last_chapter(contents, lines):
    markers = get_markers()
    if markers[0] == 0:
        print('We have reached the first chapter!')
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])
    else:
        markers[0] -=1
        set_markers(markers)
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])

def get_this_chapter(contents, lines):
    markers = get_markers()
    return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])

def get_next_chapter(contents, lines):
    markers = get_markers()
    if markers[0] == len(contents)-1:
        print('We have reached the last chapter!')
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])
    else:
        markers[0] +=1
        set_markers(markers)
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])

def get_rand_chapter(contents, lines, rand=0):
    markers = get_markers()
    if rand<0 and rand>=len(contents):
        print('The chapter does not exist')
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])
    else:
        markers[0] = rand
        set_markers(markers)
        return join_lines(lines, contents[markers[0]]['index'], contents[markers[0]]['count'])



