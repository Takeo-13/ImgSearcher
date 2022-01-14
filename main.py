#Imports. Not less, not more.
from requests import get
from urllib.parse import quote_plus as qp
import os, os.path
import json
import fake_useragent
import random
from time import sleep

def loadbar(i,p):   #do not kick me pls, i was really unconsious
                    #do not thust him, it's his work
    percent = (i/p)*100
    if percent >= 100:
        return '[██████████]'
    elif percent >= 90:
        return '[█████████ ]'
    elif percent >= 80:
        return '[████████  ]'
    elif percent >= 70:
        return '[███████   ]'
    elif percent >= 60:
        return '[██████    ]'
    elif percent >= 50:
        return '[█████     ]'
    elif percent >= 40:
        return '[████      ]'
    elif percent >= 30:
        return '[███       ]'
    elif percent >= 20:
        return '[██        ]'
    elif percent >= 10:
        return '[█         ]'
    else:
        return '[          ]'

#Proxy method
def proxy_get():
    proxies_plain = []
    proxies_2 = get('https://www.proxy-list.download/api/v1/get?type=http').content.decode().split('\r\n')
    for i in range(len(proxies_2)-1):
        proxies_plain.append({'http': proxies_2[i]})
        print(proxies_plain[i])
        print(f'Proxy {i+1}: \'http://{proxies_2[i]}\'')
    return proxies_plain

#Method to download and pack images basing on filter
def dap(linkarr, filter):
    try:
        if filter == '':
            os.mkdir('notag')
        else:
            os.mkdir(filter)
    except FileExistsError:
        print(f'[NOTICE] The same folder, starting from {len(os.listdir(filter))}')
        ctr = len(os.listdir(filter))
    if len(linkarr) == 0:
        print('[ERROR] Not a single picture. Either there is problem with the Internet, or with proxy.')
    else:
        for i in range(len(linkarr)):
            try:
                if 'http' not in linkarr[i]:
                    img_data = get('http://'+linkarr[i]).content
                else:
                    img_data = get(linkarr[i]).content
                with open(os.path.abspath(os.getcwd()) + '/' + filter + '/' + str(i+ctr+1) + '.jpg', 'a+b') as handler:
                    handler.write(img_data)
                    handler.close()
                print(f'{loadbar(i, len(linkarr))} Imported to .jpg {i + 1} images of {len(linkarr)}')
            except:
                print(f'[ERROR {i}] Connection was refused, picture is unavailable.')
                print(f'[INFO] {linkarr[i]}')
        print(f'[███████████] Successfully processed {len(linkarr)} pictures.')

#Methods to work with net and html
def grab(filter='', p=1):
    if p <= 0:
        print('[FATAL] Switching off')
        return -1
    url = 'https://yandex.ru/images/search?text'
    print(url+'='+qp(filter))
    response = []
    cur = 0
    ua = fake_useragent.UserAgent()
    proxies = proxy_get()
    print('[NOTICE] Proxies acqured!')
    for i in range(p):
        os.system('cls')
        try:
            UA = ua.random
            headers = {'User-Agent': UA}
            print(f'\n[NOTICE] Rotating User-Agent to {str(UA)}')
            curproxy = random.choice(proxies)
            print(f'[NOTICE] Rotating proxy to {str(curproxy)}')
            response.append(get(url+'='+qp(filter) + '&p=' + str(i), proxies=curproxy).content.decode())
        except TimeoutError:
            print('[WARN] Couldn\'t connect to proxie, trying to do without it')
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
            print(f'{loadbar(i, p)} GOT {i+1} pages of images of {p}')
        sleep(random.randint(1, 4))
    return parseHtml(response, filter, p)

def parseHtml(rsparr, filter, p):
    strarr = []
    onlyClassedAs = []
    floor = 0
    obj = 0
    ctr = 0
    for rsp in rsparr:
        for i in range(len(rsp)):
            if rsp[i] == '<':
                strarr.append([''])
                floor += 1
                obj = 0
            elif rsp[i] == '>':
                if floor == 0:
                    break
                strarr.append([''])
                obj = 0
                floor += 1
            else:
                if rsp[i] == '/' and rsp[i-1] != '<' or rsp[i] != '/':
                    strarr[floor-1][obj] += rsp[i]
        ctr+=1
        os.system('cls')
        print(f'[NOTICE] Parsed {ctr} pages of {p}')
        print(loadbar(ctr, len(rsparr)))

    for i in range(len(strarr)):
        if 'class=\"serp-item serp-item_type_search' in strarr[i][0] and 'div' in strarr[i][0]:
            onlyClassedAs.append(strarr[i][0])
            print(f'[NOTICE {str(i+1)}] Obtained IMG link!')

    for i in range(len(onlyClassedAs)):
        onlyClassedAs[i] = onlyClassedAs[i][onlyClassedAs[i].find("\"origin\":"):]
        try:
            onlyClassedAs[i] = json.loads(onlyClassedAs[i][:onlyClassedAs[i].find("}", 1)+1].replace('"origin":', ''))['url']
            print(onlyClassedAs[i])
        except:
            print('[ERROR] Problem with JSON in HTML, skipping.')
            print('[INFO] '+ onlyClassedAs[i])
            onlyClassedAs[i] = 'https://www.meme-arsenal.com/memes/15ef8d1ccbb4514e0a758c61e1623b2f.jpg'
    return dap(onlyClassedAs, filter)

if __name__ == '__main__':
    if random.uniform(0.0, 1.0) <= 0.95:
        print('           _ . - = - . _                    Image Grabber \'Blind Eye\' v3.1')
        print('       . "  \  \   /  /  " .                ')
        print('     ,  \                 /  .              MIT License')
        print('   . \   _,.--~=~"~=~--.._   / .            Copyright (c) 2021 Aprasidze Georgy')
        print('  ;  _.-"  / \ !   ! / \  "-._  .           ')
        print(' / ,"     / ,` .---. `, \     ". \\         ')
        print('/.    `~  |   /:::::\   |  ~`   \'.\\       + Improved quality of images A LOT')
        print('\`.  `~   |   \:::::/   | ~`  ~ .\'/        ')
        print(' \ `.  `~ \ `, `~~~\' ,`/   ~`.\' /         + Passed out because this devil captured my mind.')
        print('  .  "-._  \ / !   ! \ /  _.-"  .           + Contract helps me a lot...')
        print('   ./    "=~~.._  _..~~=`"    \.            ')
        print('     ,/         ""          \,              ')
        print('       . _/             \_ .                ')
        print('          " - ./. .\. - "                   Works with Yandex Images')
        print('----------------------------------------    To exit just print 0')

    else:
        print("""        
         ,..........   ..........,                          Archive Index 'Great Eye Lib' v9999.9
     ,..,'          '.'          ',..,                      Copyright (c) 5026 Shirime-san~
    ,' ,'            :            ', ',                     ??■■?■?■ License
   ,' ,'             :             ', ',                    - We are 50/50
  ,' ,'              :              ', ',                   - Shirime-senpai is telling him how to code!
 ,' ,'............., : ,.............', ',                  Works with Shirime-san archives~
,'  '............   '.'   ............'  ',                 To exit just print 0
 '''''''''''''''''';''';''''''''''''''''''
                    """)
    while True:
        resp = grab(input('\nRequest filter> '), int(input('Amount of pages to parse (30 pictures per page)> ')))
        if resp == -1:
            break
    input('\nEnter to exit...')
