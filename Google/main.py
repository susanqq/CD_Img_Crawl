# -*- coding: utf-8 -*-
#crawl celebrities with name list and key words
import logging
import sys
import os
import argparse
from datetime import date


from icrawler.builtin import (BaiduImageCrawler, BingImageCrawler,
                              FlickrImageCrawler, GoogleImageCrawler,
                              GreedyImageCrawler, UrlListCrawler)


def test_google(keyword,folder,count):
    google_crawler = GoogleImageCrawler(
        downloader_threads=4,
        storage={'root_dir': folder},
        log_level=logging.INFO)
    google_crawler.crawl(
        keyword,
        max_num=int(count),
        date_min=date(2000, 1, 1),
        date_max=date(2017, 11, 15))

def main(args):
    if not os.path.isfile(args.l):
        print("CD name list file doesn't exist")
        exit()
    else:
        print("craweling CD image from %s" % args.l)
    #c_rank: for each identity in an age group, c_rank image will be downloaded
    count = args.c

    for name in open(args.l):
        t = name.strip()
        print('the fetch item name is', t)
        folder = 'images/' + t
        if not os.path.exists(folder):
            os.makedirs(folder)
        keyword = 'CD' + ' ' + t
        print('the keyword is', keyword)        
        test_google(keyword,folder,count)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Crawling image based on person name')
    parse.add_argument('-l', default='CD_info.txt', help='the text filename of the celebrity name list')
    parse.add_argument('-c', default='5', help='the crawle image count for each age group')
    
    args = parse.parse_args()
    main(args)
