# pip3 install opencv-python
# pip install requests
import cv2
import numpy as np
import time
import sqlite3
from safe_bot_token import bot_token
import requests
from time import sleep

detection_images = ['5-1.png', '5-2.png', '5-3.png', '5-4.png',
                    '5-5.png', '5-6.png', '5-7.png', '5-8.png',
                    '6-1.png', '6-2.png', '6-3.png', '6-4.png',
                    '6-5.png', '6-6.png', '6-7.png', '6-8.png', ]

cameraIndex = 0  # 0 for laptop webcam, 1 for external webcam
saving = False  # save the image (True) or not, only show (False)
looking = True
tele_message_count = 5
tele_message_delay_sec = 3
match_threshold = 0.8
init_start_delay_sec = 3.0
pause_sec_camera = 0.75


def webcam_read(webcam):
    check, frame = webcam.read()
    print(check)
    print(frame)
    time.sleep(pause_sec_camera)
    cv2.imshow("Capturing", frame)
    return check, frame


def is_found(img_rgb, template_file):
    template = cv2.imread(template_file)
    w, h = template.shape[:-1]
    found = False

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = match_threshold
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        found = True
        cv2.rectangle(
            img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    return found, img_rgb, template_file[0]


def main():
    webcam = cv2.VideoCapture(cameraIndex)
    webcam_read(webcam)
    time.sleep(init_start_delay_sec)

    while looking:
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            camimg = timestr + '.png'
            found = False

            check, frame = webcam_read(webcam)

            if saving:
                cv2.imwrite(filename=camimg, img=frame)  # no need to save file
                img_rgb = cv2.imread(camimg)  # no need to read un-saved file
            else:
                img_rgb = frame

            for detection_image in detection_images:
                found, img_rgb, lvl = is_found(img_rgb, detection_image)
                if found:
                    break

            if found:
                cv2.imwrite(timestr + '_lvl_' + lvl + '.png', img_rgb)
                txt = ('POLLUTION LVL ' + lvl)
                print(txt)

                telegram_alarm(lvl)

                webcam.release()
                cv2.destroyAllWindows()
                break

            key = cv2.waitKey(1)
            if key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except (KeyboardInterrupt):
            webcam.release()
            cv2.destroyAllWindows()
            break


def telegram_alarm(lvl):
    conn = sqlite3.connect("user_info.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()

    cursor.execute(f"SELECT id FROM user")
    data = cursor.fetchall()

    alarm = f'Внимание! В Видном произошло загрязнение воздуха! Уровень {lvl} из 6'

    for i in range(0, tele_message_count):
        for chatId in data:
            bot_send_link = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatId[0]}&text={alarm}'
            requests.get(bot_send_link)
            print(bot_send_link)
            sleep(tele_message_delay_sec)


main()
