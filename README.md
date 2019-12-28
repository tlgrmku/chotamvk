# Бот Telegram-канала "Чо там Вконтакте?"

## Задача бота копировать посты из новостной ленты Вконтакте и размещать их в Telegram.

### Возможности:
 - Весь код написан на Python 3.7
 - Бот не использует модули других ботов. Используются только модули requests и стандартные json, re, os, time
 - Используемые методы из API Вконтакте: newsfeed.get, из Telegram API: sendMessage, sendPhoto, sendAnimation, sendAudio
 - Бот не копирует посты с репостами и с пометкой "Реклама"
 - Бот умеет копировать посты не только групп но и посты пользователей которые появляются в вашей ленте 
 - Бот проверяет ленту новостей каждые 5 секунд.
 - Кроме Telegram-канала можно копировать посты в Telegram-группу или в личные сообщения в Telegram.
 - Скопированные посты в Telegram имеют две кнопки:
	- "Обсудить" это ссылка на вашу Telegram-группу.
	- "Ссылка на пост" это сформированная ссылка на пост Вконтакте.

### Как использовать бота самому?
 - Для начала Вам нужны:
	- Умение пользоваться поисковиком.
	- Токен Вконтакте.
	- Токен Telegram-бота. Обращаемся к @BotFather
	- Имя или id Telegram-группы/канала/человека куда бот будет отправлять посты.
	- Имя или id Telegram-группы для кнопки обсуждений.
	- Аккаунт на Heroku.

### Ключи в Heroku:
	VKTOKEN это токен Вконтакте
	TGTOKEN это токен Telegram-бота
	CHATFORBOT это id или username Telegram-группы/канала/человека куда бот будет отправлять посты
	*Пример: @chotamvk*
	MYGROUP это id или username Telegram-группы/канала/человека для кнопки "Обсудить"
	*Пример: tg://resolve?domain=chotamvk*
	
Автор tlgrmku.

Telegram канал где живёт бот: https://t.me/chotamvk
Telegram автора бота: https://t.me/tlgrmku
