import subprocess

# journal_id = 'YHJS' # 中国计算机用户
# journal_id = 'JSJS' # 计算机时代
# journal_id = 'JSJC' # 计算机工程
# journal_id = 'XTYY' # 计算机系统应用
# journal_id = 'XXJS' # 信息化建设
# journal_id = 'XXXT' # 信息系统工程
# journal_id = 'RJSJ' # 软件世界
journal_id = 'XDJS' # 现代计算机

# start_year = 2010
start_year = 2015
for year in range(start_year, 2016):
    with open('toc/' + journal_id + '_' + str(year) + '.csv', 'w') as f:
        subprocess.call(['../agile_china_py_env/bin/python', 'toc_single_year.py', journal_id, str(year)], stdout=f)
