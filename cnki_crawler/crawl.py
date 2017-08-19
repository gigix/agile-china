import subprocess

import os
os.makedirs('output', exist_ok=True)

# journal_id = 'YHJS' # 中国计算机用户
# journal_id = 'JSJS' # 计算机时代
start_year = 2006
journal_id = 'JSJC' # 计算机时代
# start_year = 1994
for year in range(start_year, 2017):
    with open('output/' + journal_id + '_' + str(year) + '.csv', 'w') as f:
        subprocess.call(['cnki_crawler_py/bin/python', 'toc_single_year.py', journal_id, str(year)], stdout=f)
