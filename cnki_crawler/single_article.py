import requests
from pyquery import PyQuery as PQ

with requests.Session() as session:
    login_url = 'http://sso.cdclib.org/interlibSSO/interface/onecardLogin.jsp'
    payload = {'cmdACT': 'login', 'loginid': '510216198009200817', 'rdpasswd': '981121'}
    login_response = session.post(login_url, data=payload)

    article_base_url = 'http://sso.cdclib.org/interlibSSO/goto/6/=06190596Z93/kcms/detail/'
    article_url = article_base_url + 'detail.aspx?dbCode=cjfq&filename=JSJC1994S1000&dbname=CJFD9498'
    article_response = session.get(article_url)
    article_document = PQ(article_response.text)

    title = article_document('#chTitle').text()
    pdf_links = article_document('#QK_nav a')
    print(title)
    for pdf_link in pdf_links.items():
        if pdf_link.text() == 'PDF下载':
            pdf_url = article_base_url + pdf_link.attr('href').strip()
            pdf_response = session.get(pdf_url)
            pdf_content = pdf_response.content
            with open('tmp/sample.pdf', 'wb') as pdf_file:
                pdf_file.write(pdf_content)
