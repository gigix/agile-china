from pyquery import PyQuery as pq

for page in range(0, 300):
    list_page_document = pq(url='http://www.infoq.com/cn/articles/' + str(page * 12))
    article_elements = list_page_document('.news_type1') + list_page_document('.news_type2')
    for index in range(0, len(article_elements)):
        article_element = article_elements.eq(index)
        title_link = article_element.find('h2 a')
        title = title_link.text()
        url = 'http://www.infoq.com' + title_link.attr('href')
        author_element = article_element.find('.author')
        published_date = author_element.text().split('\n')[-1].split(' ')[0].strip()
        print(title + '\t' + published_date + '\t' + url)
