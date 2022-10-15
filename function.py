from warnings import formatwarning
import variables as vars
from printy import printy
from bs4 import BeautifulSoup as bs
from urllib import request
import time


def getActualFile(url):
    printy('[c>]Checking url: '+url)
    file_format_found = compareFormats(url)
    if file_format_found == False:
        try:
            if 'http' not in url: url = vars.root_url+url
            if compareFormats(url) == True: return 1
            html = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
            html = request.urlopen(html)
            
            if html.status == 200:
                html = bs(html.read().decode('utf-8'), 'html.parser')
                a_tags = html.find_all('a')
                for href in a_tags:
                    try:
                        filter = Filters(href.get('href'))
                        if filter:
                            file_format_found = compareFormats(href.get('href'))
                            if file_format_found == False:
                                try:
                                    printy('[c>]Checking url: '+href.get('href'))
                                    html = request.Request(vars.root_url+href.get('href'), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
                                    html = request.urlopen(html)
                                    if html.status == 200:
                                        html = bs(html.read(), 'html.parser')
                                        a_tags = html.find_all('a')
                                        for href in a_tags:
                                            try:
                                                file_format_found = compareFormats(href.get('href'))
                                                if file_format_found == False:
                                                    if len(href.get('href')) > 1:
                                                        filter = Filters(href.get('href'))
                                                        if filter:getActualFile(href.get('href'))
                                                    else:continue
                                                else:continue
                                            except:continue
                                    else: printy('[o]Error 404: '+url)

                                except:
                                    printy('[o]URL is Broken: @[m]We can\'t send request: '+url)
                                    continue

                    except: continue
            else:
                printy('[o]Error 404: '+url)
                return 0
        except:
            printy('[o]URL is Broken: @[m]We can\'t send request: '+url)
            return 0

def compareFormats(url):
    for formats in vars.file_formates:
        if formats in url:
            vars.total_founds += 1
            founds = str(vars.total_founds)
            printy('[o>]founds: '+founds+'@[c>] '+url)
            text_ = '"'+vars.root_url + url + '"\n'
            text = '"'+founds+'",'+text_
            vars.downloadable_contents_urls.append(text_)
            writeFile(text, 'output.csv')
            return True
    return False


def writeFile(text, file):
    if vars.rewriteFile:
        file = open(vars.root_path+'/'+file, 'w')
        vars.rewriteFile = False
    else: file = open(vars.root_path+'/'+file, 'a')
    file.write(text)
    file.close()
    return 0


def Filters(url):
    for path in vars.invalid_paths:
        if path in url:
            return 0
    return 1

def catcher():
    printy('[p>]connecting to the server...')
    for url in vars.urls_list:
        if compareFormats(url) == True:continue
        if len(url) < 2: continue
        vars.root_url = ''
        root_ = url.split('/')
        for i in range(0, 3):
            if i == 0: vars.root_url += root_[i]+'//'
            else:
                try:vars.root_url += root_[i]
                except: pass
        try:
            html = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
            html = request.urlopen(html)
            if html.status == 200:
                html = bs(html.read().decode('utf-8'), 'html.parser')
                a_tags = html.find_all('a')
                try:
                    for href in a_tags:
                        if len(href.get('href')) > 1:
                            filter = Filters(href.get('href'))
                            if filter:getActualFile(href.get('href'))
                except:continue
            else:
                printy('[o]Error 404: '+url)
                continue
        except:
            printy('[o]URL is Broken: @[m]We can\'t send request: '+url)
            continue


def getUrls():
    printy('[p>]Getting URLs...')
    try:
        with open(vars.root_path+'/urls.txt', 'r+') as urls_file:
            urls_list = urls_file.readlines()
            urls_file.close()
    except:
        printy('[m]urls file not found!')
        printy('[o>]creating new urls file in same dir')
        with open(vars.root_path+'/urls.txt', 'w') as new_file:
            new_file.write(vars.url_defaults)
            printy('[c>]urls.txt file is created successfuly')
        printy('[c>]Add your urls here...')
    for url in urls_list:
        if '#' not in url:
            if len(url) > 1:
                vars.urls_list.append(url)
