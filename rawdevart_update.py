from myutil.util import *
import json
import os
from rawdevart_download import process_chapter_page

from rawdevart_download import MANGA_LIST_JSON_FILEPATH
from rawdevart_download import DOWNLOAD_DIR
from rawdevart_download import CHAPTER_LIST_JSON_NAME

MANGA_URL_TEMPLATE = 'https://rawdevart.com/comic/%s/'
CHAPTER_URL_TEMPLATE = 'https://rawdevart.com/comic/%s/%s/'


def get_manga_list_data_json():
    manga_list = []
    if os.path.exists(MANGA_LIST_JSON_FILEPATH):
        with open(MANGA_LIST_JSON_FILEPATH, 'r', encoding='utf-8') as f:
            manga_list = json.loads(f.read())
    return manga_list


def get_last_downloaded_chapter(manga_dir):
    chapter_list = []
    with open(manga_dir + '/' + CHAPTER_LIST_JSON_NAME, 'r', encoding='utf-8') as f:
        chapter_list = json.loads(f.read())
    if len(chapter_list) > 0:
        return chapter_list[0]
    else:
        return None


# Input Example: /comic/live-dungeon/chapter-25-2/
def get_chapter_url_name(text):
    split1 = text.split('/')
    if len(split1) == 5:
        return split1[3]
    else:
        return None


def run():
    manga_list = get_manga_list_data_json()
    for manga in manga_list:
        latest_chapter = get_last_downloaded_chapter(DOWNLOAD_DIR + '/' + str(manga['id']))
        if latest_chapter is None:
            continue
        manga_url = MANGA_URL_TEMPLATE % manga['url']
        manga_soup = get_soup(manga_url)
        chapter_divs = manga_soup.find_all('div', {'class': ['list-group-item', 'list-group-item-action', 'rounded-0']})
        for chapter_div in chapter_divs:
            chapter_partial_url = chapter_div.find('a')['href']
            chapter_url_name = get_chapter_url_name(chapter_partial_url)
            if chapter_url_name is None:
                print('Chapter URL name - Website format has been changed!')
                return
            if chapter_url_name == latest_chapter['url']:
                break
            chapter_url = CHAPTER_URL_TEMPLATE % (manga['url'], chapter_url_name)
            chapter_soup = get_soup(chapter_url)
            process_chapter_page(manga['id'], manga['url'], chapter_url_name, chapter_soup)


if __name__ == '__main__':
    run()
