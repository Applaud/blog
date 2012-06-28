#! /usr/bin/env python

import httplib
import sys
import json
import hashlib
import getpass
import Image

CONNECTION = '127.0.0.1:8000'

def is_valid(char):
    return char not in ('#', '%', '*', '&', '{', '}', '+',
                     '\\', '/', ':', '<', '>', '?', '\n')


def url_escape(string):
    l = []
    for char in string:
        if is_valid(char):
            l.append(char)
    return ''.join(l)

def normalize_string(string):
    string = string.lower()
    string = url_escape(string)
    return '-'.join(string.split(' '))

def p_ify(lines):
    return '<p>%s</p>\n' % ''.join(lines)

def strip_newlines(line):
    if line[-1] == '\n':
        return '%s' % line[:-1]
    return line

def split_paragraphs(entry):
    body_list = []
    para_list = []
    for line in entry:
        line = strip_newlines(line)
        if line == '':
            if len(para_list):
                body_list += p_ify(para_list)
                para_list = []
        else:
            para_list.append('%s ' % line)
    if len(para_list):
        body_list += p_ify(para_list)
    return body_list

def send_entry(data, content_type, jsonify=True):
    conn = httplib.HTTPConnection(CONNECTION)
    if jsonify:
        data = json.dumps(data)
    headers = {'Content-type': content_type}
    request = conn.request('POST', '/post', data, headers)
    response = conn.getresponse()
    response_text = response.read()
    if response_text == 'success!':
        print 'Success!'
    elif response_text == 'password failure!':
        print response_text
    else:
        print "Bad news! This failed."

def get_password():
    password = getpass.getpass()
    h = hashlib.sha512()
    h.update(password)
    return h.hexdigest()

def blog(filename):
    with open(filename) as entry:
        title = entry.readline()
        tagline = entry.readline()
        body = ''.join([line for line in split_paragraphs(entry) if line != ''])
        entry_data = {'title': strip_newlines(title),
                      'normalized_title': normalize_string(title),
                      'tagline': strip_newlines(tagline),
                      'body': body,
                      'password': get_password()}
        send_entry(entry_data, 'application/json')

def img(filename):
    image = Image.open(filename)
    image_format = image.format
    if image_format != 'JPEG' and image_format != 'PNG':
        print 'Bad image type!'
        sys.exit()
    image = open(filename)
    data = []
    boundary = '----------boundary----------'
    data.extend(['--' + boundary,
                 'Content-disposition: form-data; name="password"',
                 '',
                 get_password()])
    data.extend(['--' + boundary,
                 'Content-disposition: form-data; name="file"; filename="%s";' % filename,
                 'Content-type: %s' % 'img/png' if image_format == 'PNG' else 'img/jpeg',
                 '',
                 image.read()])
    data.append('--' + boundary + '--')
    data.append('')
    body = '\r\n'.join(data)
    send_entry(body, 'multipart/form-data; boundary=%s' % boundary, jsonify=False)

def main():
    if len(sys.argv) != 3:
        print sys.argv
        print 'Usage: post <blog | image> <filename>'
        sys.exit()
    if sys.argv[1] == 'blog':
        blog(sys.argv[2])
    elif sys.argv[1] == 'image':
        img(sys.argv[2])
    else:
        print "Your shit doesn't make sense."

if __name__ == '__main__':
    main()
