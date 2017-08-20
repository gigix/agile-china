import os
import sys
import csv
import json
import requests
from urllib.parse import urlparse, parse_qs
from pyquery import PyQuery as PQ


def details_dir(journal_id):
    return 'details/' + journal_id

def login(session, credentials):
    login_url = 'http://sso.cdclib.org/interlibSSO/interface/onecardLogin.jsp'
    payload = {'cmdACT': 'login', 'loginid': credentials['login_id'], 'rdpasswd': credentials['password']}
    login_response = session.post(login_url, data=payload)
    print(login_response.status_code)


def crawl_single_article(session, journal_id, row, details_file):
    title = row[0]
    url = row[1]
    journal_name = row[2]
    year = row[3]
    issue = row[4]

    # original url
    # http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kns55/detail.aspx?\
    # QueryID=40&CurRec=20&dbcode=cjfq&dbname=CJFD9498&filename=JSJC401.019
    queries = parse_qs(urlparse(url).query)
    dbCode = queries['dbcode'][0]
    filename = queries['filename'][0]
    dbname = queries['dbname'][0]

    print('<{}> - <{}> {}'.format(title, journal_name, issue))

    article_base_url = 'http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kcms/detail/'
    article_url = article_base_url + 'detail.aspx?dbCode={}&filename={}&dbname={}'.format(dbCode, filename, dbname)

    ##### don't run this when another crawler session is running #####
    article_response = session.get(article_url)
    article_document = PQ(article_response.text)

    author = article_document('.author').text().replace('\n', ' ')
    keywords = article_document('#ChDivKeyWord').text().replace('\n', ' ')
    summary = article_document('#ChDivSummary').text().replace('\n', ' ')

    print('\t {}\n\t {}\n\t {}'.format(author, keywords, summary))

    pdf_filename = '{}_{}.pdf'.format(issue, title).replace(' ', '+').replace('/', '+')
    pdf_links = article_document('#QK_nav a')
    for pdf_link in pdf_links.items():
        if pdf_link.text() == 'PDF下载':
            pdf_url = article_base_url + pdf_link.attr('href').strip()
            ##### pdf download is limited #####
            # pdf_response = session.get(pdf_url)
            # pdf_content = pdf_response.content
            # with open('{}/{}'.format(details_dir(journal_id), pdf_filename), 'wb') as pdf_file:
            #     pdf_file.write(pdf_content)

    details_file.writelines('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        title, journal_name, year, issue, author, keywords, summary, pdf_filename, article_url))


def crawl_details(session, journal_id, year):
    toc_file_path = 'toc/' + journal_id + '_' + year + '.csv'
    with open(toc_file_path, newline='') as toc_file:
        toc_reader = csv.reader(toc_file, delimiter='\t')
        os.makedirs(details_dir(journal_id), exist_ok=True)
        details_file_path = details_dir(journal_id) + '/' + journal_id + '_' + year + '.csv'
        with open(details_file_path, 'w') as details_file:
            details_file.writelines(
                'title\tjournal_name\tyear\tissue\tauthor\tkeywords\tsummary\tpdf_filename\tarticle_url\n')
            for row in toc_reader:
                crawl_single_article(session, journal_id, row, details_file)


if len(sys.argv) != 3:
    print("Args: journal_id, year")
    exit()
journal_id = sys.argv[1]
year = sys.argv[2]

with open('config.json') as config_json:
    config = json.load(config_json)
credentials = config['credentials']

with requests.Session() as session:
    login(session, credentials)
    crawl_details(session, journal_id, year)
