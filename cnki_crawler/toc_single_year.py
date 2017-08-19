from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_to_lib(driver, login_id, password):
    driver.get('http://sso.cdclib.org/interlibSSO/main/')

    login_id_input = driver.find_element_by_name('loginid')
    login_id_input.clear()
    login_id_input.send_keys(login_id)

    password_input = driver.find_element_by_name('rdpasswd')
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element_by_name('loginbutton')
    login_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="../goto/6"]')))


def extract_link_from_element(a):
    return {'url': a.get_attribute('href'), 'text': a.text}


def crawl_year(journal_id, year):
    driver.get(
        'http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kns55/oldNavi/n_issue.aspx?NaviID=100&BaseID='
        + journal_id + '&Field=year&Value=' + year)
    link_to_issues = driver.find_elements_by_css_selector('#lblIssue li a')
    issues = list(map(extract_link_from_element, link_to_issues))
    for issue in issues:
        crawl_issue(year, issue)


def crawl_issue(year, issue):
    driver.get(issue['url'])
    journal_name = driver.find_element_by_id('baseinfo_chName').text

    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    articles = []
    while True:
        link_to_articles = driver.find_elements_by_css_selector('.GridTableContent > tbody > tr > td > a')
        articles += list(map(extract_link_from_element, link_to_articles))
        try:
            link_to_next_page = driver.find_element_by_xpath('//a[text()="下页"]')
            link_to_next_page.click()
        except NoSuchElementException:
            break
    driver.switch_to.default_content()
    for article in articles:
        print(article['text'] + '\t' + article['url'] + '\t' + journal_name + '\t' + str(year) + '\t' + issue['text'])
        # crawl_article(article)

# def crawl_article(article):
#     driver.get(article['url'])
#     jname = driver.find_element_by_id('jname').text
#     issue = driver.find_element_by_id('jnq').text
#     title = driver.find_element_by_id('chTitle').text
#     author = driver.find_element_by_class_name('author').text
#     summary = driver.find_element_by_id('ChDivSummary').text
#     keywords = driver.find_element_by_id('ChDivKeyWord').text
#     article_info = {
#         'journal': jname, 'issue': issue, 'title': title, 'author': author, 'summary': summary, 'keywords': keywords
#     }
#     print(jname + '\t' + issue + '\t' + author + '\t' + summary + '\t' + keywords)


import sys

if len(sys.argv) != 3:
    print("Args: journal_id, year")
    exit()

import json

with open('config.json') as config_json:
    config = json.load(config_json)
credentials = config['credentials']

driver = webdriver.Firefox()
login_to_lib(driver, credentials['login_id'], credentials['password'])

journal_id = sys.argv[1]
year = sys.argv[2]
crawl_year(journal_id, year)

driver.close()
