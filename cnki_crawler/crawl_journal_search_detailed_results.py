import sys
import json
import csv

import requests
from pyquery import PyQuery as PQ


def login(session, credentials):
    login_url = 'http://sso.cdclib.org/interlibSSO/interface/onecardLogin.jsp'
    payload = {'cmdACT': 'login', 'loginid': credentials['login_id'], 'rdpasswd': credentials['password']}
    login_response = session.post(login_url, data=payload)
    print(login_response.status_code)


def crawl_single_article(session, toc_row, output_csv):
    article_url = toc_row[-1]
    ##### don't run this when another crawler session is running #####
    article_response = session.get(article_url)
    article_document = PQ(article_response.text)

    keywords = article_document('#ChDivKeyWord').text().replace('\n', ' ')
    summary = article_document('#ChDivSummary').text().replace('\n', ' ')

    print('{}: {}'.format(toc_row[0], keywords))
    details_row = toc_row + [summary, keywords]
    output_csv.writelines('\t'.join(details_row) + '\n')


def crawl_details(session, toc_file, detail_file):
    with open(toc_file) as input_csv:
        toc_reader = csv.reader(input_csv, delimiter='\t')
        with open(detail_file, 'w') as output_csv:
            for row in toc_reader:
                crawl_single_article(session, row, output_csv)


if len(sys.argv) != 3:
    print('Args: toc_file detail_file')
    exit()

toc_file = sys.argv[1]
detail_file = sys.argv[2]

with open('config.json') as config_json:
    config = json.load(config_json)
credentials = config['credentials']

with requests.Session() as session:
    login(session, credentials)
    crawl_details(session, toc_file, detail_file)
