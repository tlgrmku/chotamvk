# Бот Telegram-канала "Чо там Вконтакте?"

## Задача бота копировать посты из новостной ленты Вконтакте и размещать их в Telegram.

### О боте:
 - Весь код написан на Python 3.7.4
 - Используемые методы из API Вконтакте: newsfeed.get, из Telegram API: sendMessage, sendPhoto, sendAnimation.
 - Бот умеет копировать посты групп и посты пользователей из вашей ленты новостей.
 - Бот проверяет ленту новостей через заданное количество секунд.
 - Бот отправляет скопированные посты в Telegram-канал, в Telegram-группу или в личные сообщения.
 - Каждый пост в Telegram имеет кнопку-ссылку на оригинальный пост Вконтакте.
 - Бот использует только одно фото, видео или gif из поста.
 - Бот не использует модули других ботов. Используются модули requests, json, re, os, time, random.
 - Бот игнорирует посты с репостами и с пометкой "Реклама".
 - Бот не копирует опрос полностью. Только вопрос.
 - Бот работает днём в указанное время с (STARTHOUR) по (ENDHOUR) часов.
 - Бот ночью спит и не отправляет запросы.
 - Бот использует два (VKTOKEN, VKTOKEN2) токена Вконтакте.


>Для периода с 07:00 до 01:00 (UTC+5) нужно выставить 2 и 19

>Можно использовать один токен Вконтакте указав его в (VKTOKEN) и в (VKTOKEN2)

### Пример поста Вконтакте и в Telegram:
![Пример поста Вконтакте и в Telegram](https://github.com/tlgrmku/chotamvk/raw/master/Image.PNG)

### Как использовать бота самому?
 - Для начала Вам нужны:
	- Два токена вашего аккаунта Вконтакте
	- Токен вашего Telegram-бота. Обращаемся к @BotFather
	- Username Telegram-группы/канала/человека куда бот будет отправлять посты (Бот должен быть админом на канале/группе)
	- Аккаунт на Heroku
	- Аккаунт на GitHub
 - В Heroku создаёте приложение, назовите его и укажите регион
 - В Reveal Config Vars (Settings) укажите свои ключи и значения (KEY и VALUE)
 - Залогиньтесь в GitHub и сделайте Fork этого репозитория
 - В Deployment method (Deploy) выбирете GitHub, укажите ссылку на репозиторий и нажмите Deploy Branch
 - Дождитесь завершения
 - В Configure Dynos (Overview) нажмите на карандаш, включите ползунок, и нажмите Confirm
 - Должно всё заработать :)
 
### KEY в Heroku:
	VKTOKEN это первый токен Вконтакте
	VKTOKEN2 это второй токен Вконтакте
	TGTOKEN это токен Telegram-бота
	CHATFORBOT это username Telegram-группы/канала/человека куда бот отправит посты
	STARTHOUR это время в часах когда бот начинает работу
	ENDHOUR это время в часах когда бот заканчивает работу
	STIME это время в секундах через которое отправляются запросы когда бот работает
	STIME2 это время в секундах через которое бот напоминает о себе в консоли когда спит
	
### Пример KEY и VALUE в Heroku:
![Пример KEY и VALUE](https://github.com/tlgrmku/chotamvk/raw/master/Image2.png)

> Telegram канал где живёт бот: https://t.me/chotamvk

> Telegram автора бота: https://t.me/tlgrmku
