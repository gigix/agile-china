import subprocess

journal_id = 'YHJS' # 中国计算机用户
# journal_id = 'JSJS' # 计算机时代
# journal_id = 'JSJC' # 计算机工程
# start_year = 2010
start_year = 1994
for year in range(start_year, 2017):
    subprocess.call(['../agile_china_py_env/bin/python', 'details_single_year.py', journal_id, str(year)])
