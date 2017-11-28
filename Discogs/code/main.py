# -*- coding: utf-8 -*-

from lxml import html, etree
import requests
import os
import argparse
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import urllib.request

def main(args):

    homepage = 'https://www.discogs.com'
    save_path = args.savepath
    num_page = 200
    save_dict = dict()
    for round in range(int(args.num_round)):
    # this website is dynamic, to fetch all possible images, we have to run several round
        for i in range(num_page):
            url = homepage + '/search/?page=' + str(i+1)
            print('analysis the webpage', url)
            CD_info = get_cd_info(url, save_dict=save_dict,savepath=save_path)
            while CD_info is None:
                print('empty,retry')
                CD_info = get_cd_info(url,save_dict=save_dict,savepath=save_path)
            save_dict.update(CD_info)
    print('the length of the dict is', len(save_dict))
    save_info(args.save_name,save_dict)

def save_info(filename, info_dict, is_only_CD_name=True):
    with open(filename,'w') as file:
        for CD_name, Img_url in info_dict.items():
            if is_only_CD_name:
                save_item = CD_name + '\n'
            else:
                save_item = CD_name + '\n' + Img_url
            file.write(str(save_item))
        

def get_cd_info(url, save_dict, savepath = None, if_save_img=True):

    page = requests.get(url,headers={'User-Agent':'test'})
    tree = html.document_fromstring(page.content)
    musicnames = tree.xpath("//div/h4/a/@title")
    artists = tree.xpath("//div/h5/span/a/text()")
    if len(musicnames) == 0:
        return None
    else: 
        img_url = tree.xpath('//div/a/span/img/@data-src')
        title = [artist+':'+musicname for artist, musicname in zip(artists, musicnames)]
        
        save_dict = dict(zip(title, img_url))

        if if_save_img:
            save_img(save_dict,savepath)
        return save_dict

def save_img(save_dict, savepath):
    keys = save_dict.keys()
    for key in keys:    
        url = save_dict[key]
        img_folder = os.path.join(savepath,key)
        
        print('the img_folder', img_folder)
        
        if "default" in url:
            print('pass the invail image', url)
            pass
        else:

            if not os.path.exists(img_folder):
                try:
                    os.makedirs(img_folder)       
                except Exception as e:
                    print('makeing folder error',e)
                    img_folder = img_folder.split(':')[-1]
                    os.makedirs(img_folder)
                                    
            savename = os.path.join(img_folder, key.replace('/','_') +'.jpg')
            if os.path.exists(savename):
                pass
                print('image already exist, skip')
            else:
                try:
                    urllib.request.urlretrieve(url,savename)
                except Exception as e:
                    print(e)
                
if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Crawling image based on person name')
    parse.add_argument('-savepath', default='dataset', help='image save folder')
    parse.add_argument('-num_round', default=10, help='how many round to run this code')
    parse.add_argument('-save_name', default='CD_info.txt', help='how many round to run this code')
    args = parse.parse_args()
    main(args)
