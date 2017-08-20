with open('tag_clouds/RJSJ_2014_summary.txt') as text_file:
    text = text_file.read()

text = text.replace('<正>', ' ')

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
filterpunt = lambda s: ''.join(filter(lambda x: x not in punct, s))
text = filterpunt(text)


# import thulac
#
#
# tagger = thulac.thulac(seg_only=True, filt=True)
# seg_list = tagger.cut(text)
#

import jieba

seg_list = jieba.lcut(text, cut_all=False)

# for index in range(0, 100):
#     print(seg_list[index])

from collections import Counter

data = dict(Counter(seg_list))

print(len(data))

top_100_tags = sorted(list(data.items()), key=lambda tag: tag[1])

for index in range(0, 100):
    print(top_100_tags[index * -1])