import requests
import json
import re
import os
import time

vktoken = str(os.environ.get('VKTOKEN'))
tgtoken = str(os.environ.get('TGTOKEN'))
chatforbot = str(os.environ.get('CHATFORBOT'))
stime = int(os.environ.get('STIME'))

def get_newsfeed(): #запрос данных с vk
    newsfeed = requests.get('https://api.vk.com/method/newsfeed.get?', params={
        'access_token': vktoken,
        'filters': 'post',
        'v': '5.103',
        'count': '1'
        }).json()
    return newsfeed

def get_reklama(newsfeed): #проверка поста на рекламу
    try:
        reklama = str(newsfeed['response']['items'][0]['marked_as_ads'])
        if reklama == '1':
            return '1'
        elif reklama == '0':
            return '0'
    except:
        return '0'
        
def get_repost(newsfeed): #проверка поста на репост
    try:
        repost = str(newsfeed['response']['items'][0]['copy_history'])
        return True
    except:
        return False
        
def get_url_post(newsfeed): #получение ссылки на пост
    sourceid = str(newsfeed['response']['items'][0]['source_id'])
    postid = str(newsfeed['response']['items'][0]['post_id'])
    url_post = 'https://vk.com/wall' + sourceid + '_' + postid
    return url_post
        
def get_name_post(newsfeed): #получение имени или названия группы
    sourceid = str(newsfeed['response']['items'][0]['source_id'])
    sourceid = sourceid[:1] #определение источника(есть ли '-' перед id)
    if sourceid == '-': #если '-' есть возвращает название группы
        namegroup = '<em>' + str(newsfeed['response']['groups'][0]['name']) + '</em>'
        return namegroup
    else: #если '-' нет возвращает имя и фамилию автора поста
        firstname = newsfeed['response']['profiles'][0]['first_name']
        lastname = newsfeed['response']['profiles'][0]['last_name']
        nameauthor = '<em>' + str(firstname) + ' ' + str(lastname) + '</em>'
        return nameauthor
        
def get_text_post(newsfeed): #получение текста поста
    text_post = newsfeed['response']['items'][0]['text']
    return text_post

def get_attach_photo(newsfeed): #получение фотографии из поста
    try:
        array_photo_post = newsfeed['response']['items'][0]['attachments'][0]['photo']['sizes']
        array_width = []
        for i in array_photo_post:
            array_width.append(i['width'])
        width = max(array_width)
        for p in array_photo_post:
            if p['width'] == int(width):
                photo_post = p['url']
        return photo_post
    except:
        return 'Нет фото'
    
def get_attach_audio(newsfeed): #получение аудио из поста
    try:
        artist_post = str(newsfeed['response']['items'][0]['attachments'][0]['audio']['artist'])
        title_post = str(newsfeed['response']['items'][0]['attachments'][0]['audio']['title'])
        name_audio = artist_post + ' - ' + title_post
        url_audio = str(newsfeed['response']['items'][0]['attachments'][0]['audio']['url'])
        return name_audio, url_audio
    except:
        return 'Нет аудио'

def get_attach_video(newsfeed): #получение видео из поста
    try:
        owner_video = str(newsfeed['response']['items'][0]['attachments'][0]['video']['owner_id'])
        id_video = str(newsfeed['response']['items'][0]['attachments'][0]['video']['id'])
        url_video = 'https://vk.com/video' + owner_video + '_' + id_video
        return url_video
    except:
        return 'Нет видео'
        
def get_attach_doc(newsfeed): #получение документа из поста
    try:
        url_doc = str(newsfeed['response']['items'][0]['attachments'][0]['doc']['url'])
        doc_file = str(newsfeed['response']['items'][0]['attachments'][0]['doc']['ext'])
        return url_doc, doc_file
    except:
        return 'Нет документов'

def get_attach_link(newsfeed): #получение ссылки из поста
    try:
        link_post = str(newsfeed['response']['items'][0]['attachments'][0]['link']['url'])
        array_photo_link_post = newsfeed['response']['items'][0]['attachments'][0]['link']['photo']['sizes']
        array_width = []
        for i in array_photo_link_post:
            array_width.append(i['width'])
        width = max(array_width)
        for p in array_photo_link_post:
            if p['width'] == int(width):
                photo_link_post = p['url']
        return link_post, photo_link_post
    except:
        return 'Нет фото и ссылки'
        
def get_poll(newsfeed): #получение опроса
    try:
        poll = str(newsfeed['response']['items'][0]['attachments'][0]['type'])
        question_poll = str(newsfeed['response']['items'][0]['attachments'][0]['poll']['question'])
        if poll == 'poll':
            return 'К посту прикреплён опрос. Подробности смотрите Вконтакте. Вопрос: ' + question_poll
        else:
            return 'Нет опроса'
    except:
        return 'Нет опроса'
        
def delete_link_text(text_post): #удаление ссылки из текста
    text_post = re.sub(r'http\S+', '', text_post)
    return text_post
    
def get_fresh_post(newsfeed): #проверка поста на свежесть
    fresh_post = newsfeed['response']['items'][0]['date']
    try:
        with open('savedatapost', 'r') as savefile:
            date_post = savefile.read()
            if int(fresh_post) <= int(date_post):
                return True
            else:
                with open('savedatapost', 'w') as newsavefile:
                    fresh_post = str(fresh_post)
                    newsavefile.write(fresh_post)
                    return False
    except:
        with open('savedatapost', 'w') as newfile:
            fresh_post = str(fresh_post)
            newfile.write(fresh_post)
            return False
    
def send_mesg_post(url_post, text): #отправка сообщения
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendMessage'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': url_post
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
        raise Exception('send_mesg_post')
    
def send_photo_post(url_post, photo, text): #отправка сообщения с фото
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendPhoto'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': url_post
                    }]
            ]
    }
    photo_post = requests.post(method, data={
         'chat_id': chatforbot,
         'photo': photo,
         'caption': text,
         'parse_mode': 'HTML',
         'disable_notification': 1,
         'reply_markup': json.dumps(reply_markup)
         })

    if photo_post.status_code != 200:
        raise Exception('send_photo_post')
    
def send_anim_post(url_post, anim, text): #отправка сообщения с gif
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendAnimation'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': url_post
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
        raise Exception('send_anim_post')
    
def send_audio_post(url_post, audiourl, text): #отправка сообщения с аудио
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendAudio'
    reply_markup = {
            'inline_keyboard': [
                    [{
                           'text': 'Ссылка на пост',
                           'url': url_post
                    }]
            ]
    }
    audio_post = requests.post(method, data={
         'chat_id': chatforbot,
         'audio': audiourl,
         'caption': text,
         'parse_mode': 'HTML',
         'disable_notification': 1,
         'reply_markup': json.dumps(reply_markup)
         })

    if audio_post.status_code != 200:
        raise Exception('send_audio_post') 
    
def get_post(newsfeed): #получение поста и всех прикреплённых данных
    url_post = get_url_post(newsfeed)
    name = get_name_post(newsfeed)
    text_post = get_text_post(newsfeed)
    photo = get_attach_photo(newsfeed)
    if photo == 'Нет фото':
        video = get_attach_video(newsfeed)
        if video == 'Нет видео':
            audio = get_attach_audio(newsfeed)
            if audio == 'Нет аудио':
                doc = get_attach_doc(newsfeed)
                if doc == 'Нет документов':
                    link = get_attach_link(newsfeed)
                    if link == 'Нет фото и ссылки':
                        poll = get_poll(newsfeed)
                        if poll == 'Нет опроса':
                            text = name + '\n' + text_post + '\n'
                            send_mesg_post(url_post, text)
                            return url_post, name, text_post
                        else:
                            text = name + '\n' + text_post[0:990] + '\n' + poll
                            send_mesg_post(url_post, text)
                            return url_post, name, text_post, poll
                    else:
                        text_post = delete_link_text(text_post)
                        text = name + '\n' + text_post[0:990] + '\n' + link[0]
                        photo = link[1]
                        send_photo_post(url_post, photo, text)
                        return url_post, name, text_post, photo
                else:
                    if doc[1] == 'gif':
                        text = name + '\n' + text_post[0:990] + '\n'
                        anim = doc[0]
                        send_anim_post(url_post, anim, text)
                        return url_post, name, text_post, doc[1]
                    elif doc[1] == 'jpg':
                        text = name + '\n' + text_post[0:990] + '\n'
                        photo = doc[0]
                        send_photo_post(url_post, photo, text)
                        return url_post, name, text_post, doc[1]
                    elif doc[1] == 'doc':
                        text = name + '\n' + text_post[0:990] + '\n' + doc[0]
                        send_mesg_post(url_post, text)
                        return url_post, name, text_post, doc[1]
                    else:
                        return url_post, name, text_post, doc
            else:
                text = name + '\n' + text_post[0:990] + '\n' + audio[0]
                audiourl = audio[1]
                send_audio_post(url_post, audiourl, text)
                return url_post, name, text_post + '\n' + audio[0], audio[1]
        else:
            text = name + '\n' + text_post[0:990] + '\n' + video
            send_mesg_post(url_post, text)
            return url_post, name, text_post, video
    else:
        text = name + '\n' + text_post[0:990] + '\n'
        send_photo_post(url_post, photo, text)
        return url_post, name, text_post, photo

while True:
    newsfeed = get_newsfeed() #запрос данных с vk
    fresh = get_fresh_post(newsfeed) #проверка поста на свежесть
    if fresh == True:
        print('Такой пост уже был')
        pass
    else:
        reklama = get_reklama(newsfeed) #проверка поста на рекламу
        if reklama == '1':
            print('Реклама')
            pass
        else:
            repost = get_repost(newsfeed) #проверка поста на репост
            if repost == True:
                print('Репост')
                pass
            else:
                g_post = get_post(newsfeed) #получение поста из vk
                print(g_post)
    
    time.sleep(stime)

#
