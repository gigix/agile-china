#!/usr/bin/env bash

#python aggregate_content.py RJSJ 1994 0 > tag_clouds/RJSJ_1994_title.txt && \
#python aggregate_content.py RJSJ 2004 0 > tag_clouds/RJSJ_2004_title.txt && \
#python aggregate_content.py RJSJ 2014 0 > tag_clouds/RJSJ_2014_title.txt && \
#python aggregate_content.py RJSJ 1994 6 > tag_clouds/RJSJ_1994_summary.txt && \
#python aggregate_content.py RJSJ 2004 6 > tag_clouds/RJSJ_2004_summary.txt && \
#python aggregate_content.py RJSJ 2014 6 > tag_clouds/RJSJ_2014_summary.txt

python aggregate_content.py XXJS 1998 0 > tag_clouds/XXJS_1998_title.txt && \
python aggregate_content.py XXJS 1998 6 > tag_clouds/XXJS_1998_summary.txt && \
python aggregate_content.py XXJS 2007 0 > tag_clouds/XXJS_2007_title.txt && \
python aggregate_content.py XXJS 2007 6 > tag_clouds/XXJS_2007_summary.txt && \
python aggregate_content.py XXJS 2016 0 > tag_clouds/XXJS_2016_title.txt && \
python aggregate_content.py XXJS 2016 6 > tag_clouds/XXJS_2016_summary.txt
