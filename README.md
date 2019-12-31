# Бот Telegram-канала "Чо там Вконтакте?"

## Задача бота копировать посты из новостной ленты Вконтакте и размещать их в Telegram.

### О боте:
 - Весь код написан на Python 3.7
 - Используемые методы из API Вконтакте: newsfeed.get, из Telegram API: sendMessage, sendPhoto, sendAnimation, sendAudio
 - Бот умеет копировать посты не только групп но и посты пользователей которые появляются в вашей ленте
 - Бот проверяет ленту новостей каждые 5 секунд
 - Кроме Telegram-канала можно копировать посты в Telegram-группу или в личные сообщения в Telegram
 - Скопированные посты в Telegram имеют две кнопки:
 	- "Ссылка на пост" это сформированная ссылка на пост Вконтакте
	- "Обсудить" это ссылка на вашу Telegram-группу
 - Бот использует только одно фото, видео, аудио, gif из поста
 - Бот не использует модули других ботов. Используются только модули requests и стандартные json, re, os, time
 - Бот не копирует посты с репостами и с пометкой "Реклама"
 - Бот не копирует опросы. Но копирует вопрос опроса
 
### Пример поста Вконтакте и в Telegram:
![Пример поста Вконтакте и в Telegram](https://github.com/tlgrmku/chotamvk/raw/master/Image.PNG)

### Как использовать бота самому?
 - Для начала Вам нужны:
	- Умение пользоваться поисковиком
	- Токен вашего аккаунта Вконтакте
	- Токен вашего Telegram-бота. Обращаемся к @BotFather
	- Username Telegram-группы/канала/человека куда бот будет отправлять посты (Бот должен быть админом на канале/группе)
	- Username Telegram-группы для кнопки обсуждений
	- Аккаунт на Heroku
	- Аккаунт на GitHub
 - В Heroku создаёте приложение, назовите его и укажите регион
 - В Reveal Config Vars (Settings) укажите свои KEY и VALUE (Ключи и значения)
 - В Deployment method (Deploy) выбирете GitHub, авторизуйтесь и укажите ссылку на этот репозиторий и нажмите Deploy Branch
 - Дождитесь завершения
 - В Configure Dynos (Overview) нажмите на карандаш, включите ползунок, и нажмите Confirm
 - Должно всё заработать :)
 
### Ключи в Heroku:
	VKTOKEN это токен Вконтакте
	TGTOKEN это токен Telegram-бота
	CHATFORBOT это username Telegram-группы/канала/человека куда бот будет отправлять посты
	*Пример: @chotamvk или -123456789012345 или 123456789*
	MYGROUP это username Telegram-группы для кнопки "Обсудить"
	*Пример: chotamvk или оставить пустым(кнопка будет не активна)*
	
### Пример KEY и VALUE в Heroku:
![Пример KEY и VALUE](https://github.com/tlgrmku/chotamvk/raw/master/Image2.png)

Автор tlgrmku.

Telegram канал где живёт бот: https://t.me/chotamvk
Telegram автора бота: https://t.me/tlgrmku
