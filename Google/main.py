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



# def test_google(keyword,folder,count):
#     #folder = 'google/'+folder
#     google_crawler = GoogleImageCrawler(folder, log_level=logging.INFO)
#     google_crawler.crawl(keyword, 0, count, date(2000, 1, 1),
#                          date(2017, 1, 20), 1, 1, 4)


def test_bing(keyword,folder,count):
    bing_crawler = BingImageCrawler(folder)
    bing_crawler.crawl(keyword, 0, count, 1, 1, 4)


def test_baidu(keyword,folder):
    baidu_crawler = BaiduImageCrawler(folder)
    baidu_crawler.crawl(keyword, 0, count, 1, 1, 4)


def test_flickr(keyword,folder,count):
    #folder = 'flicker/'+folder
    flickr_crawler = FlickrImageCrawler('983677f73df07199d3bc575c08a77c6b',
                                        folder)
    flickr_crawler.crawl(max_num=10, downloader_thr_num=4, tags=keyword,
                         tag_mode='all', group_id='68012010@N00')


def test_greedy(keyword,folder):
    greedy_crawler = GreedyImageCrawler(folder)
    greedy_crawler.crawl('bbc.com/sport', 1, 4, 1, min_size=(200, 200))


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
        print t
        folder = 'images/' + t
        if not os.path.exists(folder):
            os.makedirs(folder)
        keyword = 'CD' + ' ' + t
        print('the keyword is', keyword)
        # if len(sys.argv) == 1:
        #     dst = 'all'
        # else:
        #     dst = sys.argv[1:]
        # if 'all' in dst:
        #     dst = ['google', 'bing','flickr']
        # if 'google' in dst:
        test_google(keyword,folder,count)
        # if 'bing' in dst:
        #     test_bing(keyword,folder,count)
        # if 'baidu' in dst:
        #     test_baidu(keyword,folder,count)
        # if 'flickr' in dst:
        #     test_flickr(keyword,folder,count)
        # if 'greedy' in dst:
        #     test_greedy(keyword,folder,count)


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Crawling image based on person name')
    parse.add_argument('-l', default='CD_info.txt', help='the text filename of the celebrity name list')
    parse.add_argument('-c', default='5', help='the crawle image count for each age group')
    
    args = parse.parse_args()
    main(args)
