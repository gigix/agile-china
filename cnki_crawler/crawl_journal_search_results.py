import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
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


def crawl_search_results():
    driver.get('http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kns55/')
    
    ##### search for '软件工程'
    search_scope = Select(driver.find_element_by_id('txt_1_sel'))
    search_scope.select_by_visible_text('篇名')
    driver.find_element_by_id('txt_1_value1').send_keys('软件工程')
    
    ##### search for '敏捷+软件'
    # driver.find_element_by_id('txt_1_value1').send_keys('敏捷')
    # driver.find_element_by_id('txt_1_value2').send_keys('软件')
    
    driver.find_element_by_id('btnSearch').click()
    time.sleep(5)

    for page_number in range(1, 99):
        driver.get('http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kns55/brief/brief.aspx?'
                   'curpage={}&RecordsPerPage=100&dbPrefix=SCDB&turnpage=1&QueryID=0'.format(page_number))
        article_rows = driver.find_elements_by_css_selector('.GridTableContent > tbody > tr')[1:]
        for article_row in article_rows:
            columns = article_row.find_elements_by_tag_name('td')[1:]
            output = list(map(lambda column: column.text, columns))
            output.append(article_row.find_elements_by_css_selector('a')[1].get_attribute('href'))
            print('\t'.join(output))


import json

with open('config.json') as config_json:
    config = json.load(config_json)
credentials = config['credentials']

driver = webdriver.Firefox()
login_to_lib(driver, credentials['login_id'], credentials['password'])

crawl_search_results()

driver.close()
