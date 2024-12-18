import requests
from urllib.parse import urlencode
from zipfile import ZipFile
import os
import socket
import logging
import datetime
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://disk.yandex.ru/d/W2BDKWLAZNBkiA'
in_game_error_text = "Загрузка не удалась. Посмотрите лог в папке с программой."
# проверка подключения к интернету
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

# Получаем загрузочную ссылку
def download():
    logger = logging.getLogger(__name__)
    today = datetime.datetime.today()
    # logging.basicConfig(
    #     filename=f"{today.day:02}-{today.month:02}-{today.year}_{today.hour:02}-{today.minute:02}.log",
    #     level=logging.INFO,
    #     filemode='w',
    #     format="%(asctime)s %(levelname)s %(message)s"
    # )
    logger.setLevel(logging.INFO)
    py_handler = logging.FileHandler(f"{today.day:02}-{today.month:02}-{today.year}_{today.hour:02}-{today.minute:02}.log", mode='w')
    py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    py_handler.setFormatter(py_formatter)
    logger.addHandler(py_handler)

    logger.info('Started')
    try:
        if is_connected():
            logger.info("Getting download link...")
            try:
                final_url = base_url + urlencode(dict(public_key=public_key))
                response = requests.get(final_url)
                download_url = response.json()['href']
            except Exception as e:
                logger.error(str(e))
                return False or in_game_error_text
            logger.info("Link received successfully")
            logger.info("Download has started.")
            download_response = requests.get(download_url)
            cache = "cache.7z"
            with open(cache, 'wb') as f:
                f.write(download_response.content)
            logger.info("Downloading is complete.")
            logger.info("Extract archive...")
            try:
                with ZipFile(cache, "r") as zf:
                    zf.extractall()
            except Exception as e:
                logger.error(str(e))
                return False or in_game_error_text
            logger.info("Archive is unpacked.")
            logger.info("Deleting cache...")
            try:
                os.remove(cache)
            except Exception as e:
                logger.error(str(e))
                return False or in_game_error_text
            logger.info("Cache deleted.")
            return True
        else:
            logger.error("No internet connection.")
            return False or in_game_error_text
    finally:
        logger.info('Finished')

