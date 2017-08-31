import subprocess

#### already crawled
# journal_id = 'YHJS' # 中国计算机用户
# journal_id = 'RJSJ' # 软件世界
# journal_id = 'XXJS' # 信息化建设
# journal_id = 'ITSJ' # 程序员
# journal_id = 'JSJS' # 计算机时代
# journal_id = 'JSJC' # 计算机工程
# journal_id = 'XTYY' # 计算机系统应用
# journal_id = 'XXXT' # 信息系统工程
# journal_id = 'XDJS' # 现代计算机

#### to be crawled

start_year = 1994
# start_year = 2007
for year in range(start_year, 2017):
    subprocess.call(['../agile_china_py_env/bin/python', 'details_single_year.py', journal_id, str(year)])
