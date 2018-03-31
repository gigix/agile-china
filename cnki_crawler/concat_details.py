import os

rootdir = './details'
output_file = './tmp/all_details.csv'

with open(output_file, 'w') as f:
    is_first_file = True
    for subdir, dirs, files in os.walk(rootdir):
        for detail_file in files:
            with open(os.path.join(subdir, detail_file)) as df:
                detail_content = df.read().split('\n')
            if(not is_first_file):
                detail_content = detail_content[1:]
            f.write('\n'.join(detail_content))
            is_first_file = False