from pyquery import PyQuery    

document = PyQuery(filename = 'douban_agile_books.html')
search_result_tags = document('.result')

search_results = []
for index in range(0, len(search_result_tags)):
    tag = search_result_tags.eq(index)
    title = tag.find('.title a').text()
    try:
        publish_year = int(tag.find('.rating-info .subject-cast').text().split('/')[-1])
    except:
        publish_year = -1
    description = tag.find('p').text()
    search_results.append({'title': title, 'publish_year': publish_year, 'description': description})
    
print(len(search_results))

import csv

with open('douban_agile_books.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter="\t")
    writer.writerow(['title', 'publish_year', 'description'])
    for book in search_results:
        writer.writerow([book['title'], book['publish_year'], book['description']])