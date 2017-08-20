import csv

def aggregate_content(journal_id, year, column):
    with open('details/{}/{}_{}.csv'.format(journal_id, journal_id, year), newline='') as details_file:
        details_reader = csv.reader(details_file, delimiter='\t')
        all_titles = '\n'.join(map(lambda row: row[column], details_reader))
        print(all_titles)

import sys

if len(sys.argv) != 4:
    print('args: journal_id, year, column')
    exit()

journal_id = sys.argv[1]
year = sys.argv[2]
column = int(sys.argv[3])

aggregate_content(journal_id, year, column)

# from wordcloud import WordCloud
#
# wordcloud = WordCloud().generate(all_titles)
#
# import matplotlib.pyplot as plt
#
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(all_titles)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
