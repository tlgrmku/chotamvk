import requests
import json
import re
import os
import time
import random

vktoken = str(os.environ.get('VKTOKEN')) #str
vktoken2 = str(os.environ.get('VKTOKEN2')) #str
tgtoken = str(os.environ.get('TGTOKEN')) #str
chatforbot = str(os.environ.get('CHATFORBOT')) #str
starthour = int(os.environ.get('STARTHOUR')) #2
endhour = int(os.environ.get('ENDHOUR')) #19
stime = int(os.environ.get('STIME')) #5
stime2 = int(os.environ.get('STIME2')) #60


def get_newsfeed():
    if random.randint(0, 1) == 0:
        try:
            newsfeed = requests.get('https://api.vk.com/method/newsfeed.get?', params={
                'access_token': vktoken,
                'filters': 'post',
                'v': '5.103',
                'count': '1'
                }).json()
        except:
            print('Не удалось сделать первый запрос к Вконтакте')
            pass
        else:
            return newsfeed
    else:
        try:
            newsfeed = requests.get('https://api.vk.com/method/newsfeed.get?', params={
                'access_token': vktoken2,
                'filters': 'post',
                'v': '5.103',
                'count': '1'
                }).json()
        except:
            print('Не удалось сделать второй запрос к Вконтакте')
            pass
        else:
            return newsfeed

def get_fresh_post(newsfeed):
    fresh_post = newsfeed['response']['items'][0]['date']
    try:
        with open('savedatapost', 'r') as savefile:
            date_post = savefile.read()
            if int(fresh_post) <= int(date_post):
                return True
            else:
                with open('savedatapost', 'w') as newsavefile:
                    newsavefile.write(str(fresh_post))
                    return False
    except:
        with open('savedatapost', 'w') as newfile:
            newfile.write(str(fresh_post))
            print('Создан файл savedatapost')
            return True

def get_url_post(newsfeed):
    sourceid = str(newsfeed['response']['items'][0]['source_id'])
    postid = str(newsfeed['response']['items'][0]['post_id'])
    url_post = 'https://vk.com/wall' + sourceid + '_' + postid
    return url_post
    
def get_name_post(newsfeed):
    sourceid = str(newsfeed['response']['items'][0]['source_id'])
    sourceid = sourceid[:1]
    if sourceid == '-':
        name_post = '<ins>' + str(newsfeed['response']['groups'][0]['name']) + '</ins>'
        return name_post
    else:
        firstname = str(newsfeed['response']['profiles'][0]['first_name'])
        lastname = str(newsfeed['response']['profiles'][0]['last_name'])
        name_post = '<ins>' + firstname + ' ' + lastname + '</ins>'
        return name_post

def get_text_post(newsfeed):
    text_post = newsfeed['response']['items'][0]['text']
    if len(text_post) > 800:
        text_post = str(text_post[0:800] + '... Продолжение по кнопке ниже.')
        return text_post
    else:
        return text_post

#----------------------------------------------------------------------------------------------
def send_mesg_post(newsfeed, text):
    urlpost = get_url_post(newsfeed)
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendMessage'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': urlpost
                    }]
            ]
    }
    mesg_post = requests.post(method, data={
         'chat_id': chatforbot,
         'text': text,
         'parse_mode': 'HTML',
         'disable_notification': 1,
         'reply_markup': json.dumps(reply_markup)
         })
    if mesg_post.status_code != 200:
        return 'Что-то пошло не так в mesg_post'
    else:
        return text

def send_photo_post(newsfeed, url_photo_post, text):
    urlpost = get_url_post(newsfeed)
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendPhoto'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': urlpost
                    }]
            ]
    }
    photo_post = requests.post(method, data={
         'chat_id': chatforbot,
         'photo': url_photo_post,
         'caption': text,
         'parse_mode': 'HTML',
         'disable_notification': 1,
         'reply_markup': json.dumps(reply_markup)
         })
    if photo_post.status_code != 200:
        return 'Что-то пошло не так в photo_post'
    else:
        return text + '\n' + url_photo_post

def send_anim_post(newsfeed, anim, text):
    urlpost = get_url_post(newsfeed)
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendAnimation'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': urlpost
                    }]
            ]
    }
    anim_post = requests.post(method, data={
         'chat_id': chatforbot,
         'animation': anim,
         'caption': text,
         'parse_mode': 'HTML',
         'disable_notification': 1,
         'reply_markup': json.dumps(reply_markup)
         })
    if anim_post.status_code != 200:
        return 'Что-то пошло не так в anim_post'
    else:
        return text

#----------------------------------------------------------------------------------------------
def get_attach_audio(newsfeed):
    try:
        newsfeed['response']['items'][0]['attachments'][0]['audio']
    except:
        text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed)
        return send_mesg_post(newsfeed, text)
    else:
        pass

def get_attach_poll(newsfeed):
    try:
        poll = str(newsfeed['response']['items'][0]['attachments'][0]['type'])
        question_poll = str(newsfeed['response']['items'][0]['attachments'][0]['poll']['question'])
    except:
        return get_attach_audio(newsfeed)
    else:
        if poll == 'poll':
            text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed) + '\nК посту прикреплён опрос: ' + question_poll
            return send_mesg_post(newsfeed, text)
        else:
            pass

def get_attach_doc(newsfeed):
    try:
        url_doc = str(newsfeed['response']['items'][0]['attachments'][0]['doc']['url'])
        doc_file = str(newsfeed['response']['items'][0]['attachments'][0]['doc']['ext'])
    except:
        return get_attach_poll(newsfeed)
    else:
        if doc_file == 'gif':
            text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed)
            return send_anim_post(newsfeed, url_doc, text)
        elif doc_file == 'jpg':
            text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed)
            return send_photo_post(newsfeed, url_doc, text)
        elif doc_file == 'doc':
            text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed) + '\n' + url_doc
            return send_mesg_post(newsfeed, text)
        else:
            pass

def get_attach_video(newsfeed):
    try:
        owner_video = str(newsfeed['response']['items'][0]['attachments'][0]['video']['owner_id'])
        id_video = str(newsfeed['response']['items'][0]['attachments'][0]['video']['id'])
    except:
        return get_attach_doc(newsfeed)
    else:
        url_video = 'https://vk.com/video' + owner_video + '_' + id_video
        text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed) + '\n' + url_video
        return send_mesg_post(newsfeed, text)

def get_attach_link(newsfeed):
    try:
        link_post = str(newsfeed['response']['items'][0]['attachments'][0]['link']['url'])
    except:
        return get_attach_video(newsfeed)
    else:
        array_photo_link_post = newsfeed['response']['items'][0]['attachments'][0]['link']['photo']['sizes']
        array_width = []
        for w in array_photo_link_post:
            array_width.append(w['width'])
        for p in array_photo_link_post:
            if p['width'] == max(array_width):
                url_photo_linkpost = p['url']
                text = re.sub(r'http\S+', '', get_name_post(newsfeed) + '\n' + get_text_post(newsfeed)) + '\n' + link_post
                return send_photo_post(newsfeed, url_photo_linkpost, text)
            else:
                pass

def get_attach(newsfeed):
    try:
        array_photo_post = newsfeed['response']['items'][0]['attachments'][0]['photo']['sizes']
    except:
        return get_attach_link(newsfeed)
    else:
        array_width = []
        for w in array_photo_post:
            array_width.append(w['width'])
        for p in array_photo_post:
            if p['width'] == max(array_width):
                url_photo_post = p['url']
                text = get_name_post(newsfeed) + '\n' + get_text_post(newsfeed)
                return send_photo_post(newsfeed, url_photo_post, text)
            else:
                pass

#----------------------------------------------------------------------------------------------
print(requests.get('https://wikipedia.org/').headers['X-Client-IP'])
hours = list(range(starthour, (endhour + 1)))

while True:
    if time.localtime()[3] in hours:
        newsfeed = get_newsfeed()
        if get_fresh_post(newsfeed) == True:
            print('Такой пост уже был')
            pass
        else:
            try:
                newsfeed['response']['items'][0]['copy_history']
            except:
                try:
                    if newsfeed['response']['items'][0]['marked_as_ads'] == 1:
                        print('Реклама')
                        pass
                    else:
                        print(get_attach(newsfeed))
                except:        
                    print(get_attach(newsfeed))
            else:
                print('Репост')
                pass

        time.sleep(stime)
    else:
        print('Бот спит')
        time.sleep(stime2)
