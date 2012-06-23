#! /usr/bin/env python

import httplib
import sys
import json
import hashlib
import getpass

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

def send_entry(data):
    conn = httplib.HTTPConnection('127.0.0.1:8000')
    request = conn.request('POST', '/post', json.dumps(data))
    response = conn.getresponse()
    response_text = response.read()
    if response_text == 'success!':
        print 'Success!'
    elif response_text == 'password failure!':
        print response_text
    else:
        print "Bad news! This failed."

def main():
    if len(sys.argv) != 2:
        print sys.argv
        print 'Usage: post <filename>'
        sys.exit()
    with open(sys.argv[1]) as entry:
        title = entry.readline()
        tagline = entry.readline()
        body = ''.join([line for line in split_paragraphs(entry) if line != ''])
        password = getpass.getpass()
        h = hashlib.sha512()
        h.update(password)
        entry_data = {'title': strip_newlines(title),
                      'normalized_title': normalize_string(title),
                      'tagline': strip_newlines(tagline),
                      'body': body,
                      'password': h.hexdigest()}
        send_entry(entry_data)

if __name__ == '__main__':
    main()
