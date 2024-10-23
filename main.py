import os.path as osp
from content_crawler import crawl_content

# Debug stuff
import logging as lg
from traceback import format_exc

logger = lg.getLogger('Debug Info')
logger.setLevel(lg.DEBUG)

# create file handler that logs debug and higher level messages
fh = lg.FileHandler(osp.join('.', 'log', 'debug.log'))
fh.setLevel(lg.DEBUG)

ch = lg.StreamHandler()
ch.setLevel(lg.ERROR)

formatter = lg.Formatter('%(levelname)s:\n\t%(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


format_debug = lambda url, traceback: f'''Could not crawl
{url}
    at line {i}
{'=' * len(traceback)}\n{traceback}\n{'=' * len(traceback)}'''

# Crawling
error_path = osp.join('.', 'log', 'error_links.txt')
with open(osp.join('.', 'links.txt')) as file:
    text = [line.rstrip('\n') for line in file.readlines()]
start = 200
end = 375
for i, url in enumerate(text[start:end], start=start):
    try:
        crawl_content(url)
        print(f'{i - start + 1} success crawl')
    except Exception as e:
        traceback = format_exc()
        logger.debug(format_debug(url, traceback))
        with open(error_path, 'a') as file:
            file.write(f'{url}\n')