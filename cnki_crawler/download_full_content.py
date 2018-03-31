import sys
import shutil
import json
import csv
import time
import os

import requests
from pyquery import PyQuery as PQ


def login(session, credentials):
    login_url = 'http://sso.cdclib.org/interlibSSO/interface/onecardLogin.jsp'
    payload = {'cmdACT': 'login', 'loginid': credentials['login_id'],
               'rdpasswd': credentials['password']}
    login_response = session.post(login_url, data=payload)
    print(login_response.status_code)


def download_files(session, list_file, dist_dir):
    with open(list_file) as input_csv:
        toc_reader = csv.reader(input_csv, delimiter='\t')
        for row in toc_reader:
            download_single_file(session, row, dist_dir)


def download_single_file(session, toc_row, dist_dir):
    article_url = toc_row[-1]
    article_title = toc_row[0]
    journal_name = toc_row[2]
    issue = toc_row[4]
    local_filename = dist_dir + journal_name + '-' + issue + '-' + article_title.replace('/', '-') + '.pdf'

    if os.path.isfile(local_filename) and os.stat(local_filename).st_size > 9593:
        print('File exist - %s' % local_filename)
        return

    article_response = session.get(article_url)
    article_document = PQ(article_response.text)

    current_path = article_response.url.split('detail.aspx?')[0]
    content_file_url = current_path + article_document('#QK_nav a').attr('href').strip() + '&dflag=pdfdown'

    print('Downloading %s' % local_filename)
    time.sleep(10)
    print(content_file_url)
    r = session.get(content_file_url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


if len(sys.argv) != 3:
    print('Args: list_file dist_dir')
    exit()

list_file = sys.argv[1]
dist_dir = sys.argv[2]

with open('config.json') as config_json:
    config = json.load(config_json)
credentials = config['credentials']

with requests.Session() as session:
    login(session, credentials)
    download_files(session, list_file, dist_dir)
