# gas_alarm

# Предназначение: 
будить человека повторяющимся звуком уведомлений Телеграма чтобы закрыть окна квартиры если ночью прилетает дым лесных пожаров (или какой-то другой)

# Процесс:
- скрипт alarm.py (используя камеру) наблюдает за индикацией устройства для контроля загрязнения воздуха 
- используется OpenCV для определения "мигания" красных уровней загрязнения (5 и 6, на основе поиска шаблонов - файлы 5.png, 6.png), отправляет уведомления в Телеграм-бота
- Телеграм-бот предоставляет пользователям сервис подписки\отписки, отправляет уведомления о загрязнении подписанным пользователям

Скрипт-"наблюдатель" и бот заупщены круглосуточно, но т.к. контроллер стоит на кухне - то иногда реагирует на процессы готовки (показывает 5), поэтому принудительно ограничено время срабатывания, с 0 до 7 утра МСК (только ночью по "красной" индикаци отправляются уведомления). 

=====================================

# Purpose: 
to wake human up using repeating sound of Telegram notifications to close flat`s windows in case smoke of forest fires (or any other kind) arrived in night

# Process:
- script (using camera) capture indications of air pollution control device 
- using OpenCV to detect "blinking" of red ones indicators (grades 5 and 6, based on templates - files 5.png, 6.png) and send notifications to Telegram bot
- Telegram bot provides user subscribe / unsubscribe service, sending 5-6 grades notifications to subscribed users

Capturing cript and bot are running 24x7, but controller set up at kitchen and sometimes showing 5th grade, so reaction time constrained to period starting 0 to 7 morning MSK (notifications by "red" grade sent only at night)

=====================================

# Расположение \ Location

![](https://github.com/Wolfram-180/gas_alarm/blob/master/environment/wall1.jpg?raw=true)
![](https://github.com/Wolfram-180/gas_alarm/blob/master/environment/wall2.jpg?raw=true)

# Пример уведомления \ Notification example

![](https://github.com/Wolfram-180/gas_alarm/blob/master/environment/5_lvl_detected.png?raw=true)
