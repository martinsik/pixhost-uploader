import os
from http.cookiejar import CookieJar
import requests
from lxml import html


PIXHOST_HOMEPAGE_URL = 'http://www.pixhost.org/'
PIXHOST_UPLOAD_URL = 'http://www.pixhost.org/classic-upload/'


def upload(images, adult=False):
    source_images = images if isinstance(images, list) else [images]

    params = {
        'content_type': int(adult),
        'tos': 'on'
    }

    # fake headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Referer': 'http://www.pixhost.org/classic-upload/',
        'Origin': 'http://www.pixhost.org',
        'Host': 'www.pixhost.org',
    }

    files = []
    # add images to parameter lists
    for img in source_images:
        if os.path.getsize(img) > pow(10, 7):
            raise TooLargeImageFormat()

        files.append(('img[]', (os.path.basename(img), open(img, 'rb'))))


    # make first request to the homepage to fill cookie jar with default cookies
    jar = CookieJar()
    requests.post(PIXHOST_HOMEPAGE_URL, cookies=jar, headers=headers)

    # upload images
    response = requests.post(PIXHOST_UPLOAD_URL, data=params, cookies=jar, headers=headers, files=files)

    for file in files:
        file[1][1].close()

    if response.status_code != 200:
        raise UploadFailed(response)

    # urls for uploaded images
    image_urls = []

    root = html.fromstring(response.text)

    main_div = root.xpath('//div[@id="text"]')

    # fetch small thumbnails
    all_small_thumbs = main_div[0].xpath('./a')

    for thumb_elm in all_small_thumbs:
        # we need to download the page with fullsize image
        full_size_preview_url = thumb_elm.attrib['href']
        preview_response = requests.get(full_size_preview_url, headers=headers, cookies=jar)
        preview_root = html.fromstring(preview_response.text)

        image_urls.append({
            'thumb_image': thumb_elm.xpath('./img')[0].attrib['src'],
            'full_size_image': preview_root.xpath('//img[@id="show_image"]')[0].attrib['src'],
            'page_url': full_size_preview_url  # you probably won't need this
        })

    return image_urls if isinstance(images, list) else image_urls[0]


class UploadFailed(Exception):
    pass


class TooLargeImageFormat(Exception):
    pass