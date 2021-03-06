# Imports. Not less, not more.
from requests import get
from urllib.parse import quote_plus as qp
import os, os.path
import json
import fake_useragent
import random
from time import sleep
import tkinter
import argparse


def loadbar(i, p):  # do not kick me pls, i was really unconsious
    # do not thust him, it's his work
    # it's a big joke on project, really. trust me please
    percent = (i // p) * 10
    return '█' * percent


# Proxy method
# There can be problems, i'll refactor it later. When I'll need find more than 50 pages of pictures, of course.
def proxy_get():
    proxies_plain = []
    try:
        proxies_2 = get('https://www.proxy-list.download/api/v1/get?type=http').content.decode().split('\r\n')
        for i in range(len(proxies_2) - 1):
            proxies_plain.append({'http': proxies_2[i]})
    except:
        print('nea')
    return proxies_plain


# Method to download and pack images basing on filter
def dap(linkarr, filter):
    print(f"[DEBUG] I'm in dap!")
    ctr = 0
    try:
        if filter == '':
            os.mkdir('notag')
        else:
            os.mkdir(filter)
    except FileExistsError:
        print(f'[NOTICE] The same folder, starting from {len(os.listdir(filter))}')
    if len(linkarr) == 0:
        print('[ERROR] Not a single picture. Either there is problem with the Internet, or with proxy.')
    else:
        print('[DEBUG] I\'m grabbing pictures now.')
        for i in range(len(linkarr)):
            try:
                if 'http' not in linkarr[i]:
                    img_data = get('http://' + linkarr[i]).content
                else:
                    img_data = get(linkarr[i]).content
                with open(os.path.abspath(os.getcwd()) + '/' + filter + '/' + str(i + ctr + 1) + '.jpg',
                          'a+b') as handler:
                    handler.write(img_data)
                    handler.close()
            except:
                print(f'[ERROR {i}] Connection was refused, picture is unavailable.')
                print(f'[INFO] {linkarr[i]}')
    tkinter.messagebox.showinfo('Thanks', f'Grabber has finished grabbing {filter} pictures!')

# Methods to work with net and html
def grab(filter='', p=1):
    if p <= 0:
        print('[FATAL] Switching off')
        return -1

    url = 'https://yandex.ru/images/search?text'
    print(url + '=' + qp(filter))
    response = []
    cur = 0

    ua = fake_useragent.UserAgent()
    proxies = proxy_get()

    for i in range(p):

        try:
            UA = ua.random
            headers = {'User-Agent': UA}
            curproxy = random.choice(proxies)
            response.append(get(url + '=' + qp(filter) + '&p=' + str(i), proxies=curproxy).content.decode())

        except TimeoutError:
            print('[WARN] Couldn\'t connect to proxy, trying to do without it')
            response.append(get(url + '=' + qp(filter) + '&p=' + str(i)).content.decode())

        except IndexError:
            print('[WARN] Proxy is not available anymore, doing without it.')
            response.append(get(url + '=' + qp(filter) + '&p=' + str(i)).content.decode())

        if 'ogp.me' in response[i]:
            print('[WARN] Captcha got, cutting job.')
            p = i
            del response[i]
            break

        else:
            print(f'{loadbar(i, p)} GOT {i + 1} pages of images of {p}')

        sleep(random.randint(1, 4))
    return parseHtml(response, filter, p)


def parseHtml(rsparr, filter, p):
    strarr = []
    onlyClassedAs = []
    floor = 0
    obj = 0
    ctr = 0

    for rsp in rsparr:
        rsplen = len(rsp)
        for i in range(rsplen):
            if rsp[i] == '<':
                floor += 1
                strarr.append([''])
                obj = 0

            elif rsp[i] == '>':
                if strarr[floor-1] == 'html':
                    break
                obj = 0

            else:
                if (rsp[i] == '/' and rsp[i - 1] != '<') or rsp[i] != '/':
                    strarr[floor-1][obj] += rsp[i]

        ctr += 1
        print(f'[NOTICE] Parsed {ctr} pages of {p}')
        print(loadbar(ctr, len(rsparr)))

    for i in range(len(strarr)):
        if 'class=\"serp-item serp-item_type_search' in strarr[i][0] and 'div' in strarr[i][0]:
            onlyClassedAs.append(strarr[i][0])
            print(f'[NOTICE {str(i + 1)}] Obtained IMG link!')

    for i in range(len(onlyClassedAs)):
        onlyClassedAs[i] = onlyClassedAs[i][onlyClassedAs[i].find("\"origin\":"):]

        try:
            onlyClassedAs[i] = \
                json.loads(onlyClassedAs[i][:onlyClassedAs[i].find("}", 1) + 1].replace('"origin":', ''))['url']
            print(onlyClassedAs[i])

        except:
            print('[ERROR] Problem with JSON in HTML, skipping.')
            print('[INFO] ' + onlyClassedAs[i])
            onlyClassedAs[i] = 'https://www.meme-arsenal.com/memes/15ef8d1ccbb4514e0a758c61e1623b2f.jpg'

    return dap(onlyClassedAs, filter)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser("scrapper")
    argparser.add_argument('filter', nargs="+", type=str, help="Filter to search Yandex")
    argparser.add_argument('pages', nargs="+", type=int, help="Amount of pages to scrap")
    args = argparser.parse_args()
    grab(vars(args)['filter'][0], vars(args)['pages'][0])