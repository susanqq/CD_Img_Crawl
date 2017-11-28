
from imdb import IMDb
from lxml import html
import requests
import urllib
import re
import math
import logging
import signal

def handler(signum, frame):
    print("the process is dead")
    raise Exception("end of time")

def get_ID(ia, name):
    try:
        ia.search_person(name)
    # except IMDbDataAccessError, e:
    #     logging.basicConfig(filename='IMDBError.log',level=logging.INFO)
    #     logging.info('no response for %s' % e)
    #     ID = 'None'
    except:
        logging.basicConfig(filename='missing.log',level=logging.INFO)
        logging.info('no response for %s' % name)
        ID ='None'
    else:
        if len(ia.search_person(name)) == 0:
            logging.basicConfig(filename='missing.log',level=logging.INFO)
            logging.info('missing celebrity %s' % name)
            ID = 'None'
        else:
            person = ia.search_person(name)[0]
            ID =person.personID

# Load celebrities name list, search their IMDB ID    
    return ID

def get_PersonInfo(homepage, ID):

    url = homepage +ID +'/'
# Get their Birth of data, Dead of data (if avaiable) and Borned Country 
    page = requests.get(url)
    tree = html.document_fromstring(page.content)
    BoD_tmp= tree.xpath('//div[@id="name-born-info"]/time/@datetime')
    if len(BoD_tmp) == 0:
        BoD_tmp.append(str(0000))
        print('No Birth of Date Information')
    Country_tmp = tree.xpath('//div[@id="name-born-info"]/a/text()')
    if len(Country_tmp) == 0:
        Country_tmp.append(str(0000))
        print('No Country Information')
    Country = Country_tmp[0].replace('/', '')
    BoD = BoD_tmp[0].replace('/', '')
    return BoD, Country
def get_BioImg(homepage, ID):

    url = homepage +ID +'/'
    page = requests.get(url)
    tree = html.document_fromstring(page.content)
    img_src = tree.xpath('//div[@class="image"]/a/img/@src')
    
    return img_src[0]
def save_img(url,savepath):

    urllib.urlretrieve(url,savepath)

def get_num_gallery(ID, homepage, url):
    url = homepage +ID +'/'
    root_url = url + 'mediaindex?ref_=nm_mv_close'
    print(root_url)
    s = requests.Session()
    #gallery_page = requests.get(root_url)
    try:
        gallery_page = s.get(root_url, timeout=1000)        
    except requests.exceptions.ConnectionError:
        logging.basicConfig(filename='noresponse.log',level=logging.INFO)
        logging.info('no response for %s' % root_url)
        logging.error('Connection error when downloading image %s'% ID)
        count = 0
    except requests.exceptions.Timeout:
        logging.info('time out for %s' % root_url)
        logging.error('Timeout when downloading image %s' % root_url)
        count = 0
    else:
        gallery_tree = html.document_fromstring(gallery_page.content) 
        try:
            n_img =gallery_tree.xpath('//div[@class="media_index_pagination leftright"]/div[@id="left"]/text()')[0]
        except:
            count = 0
        else:
            if n_img.isdigit():
                count = int(n_img)
            else:
                count = re.findall(r'\d+', n_img)[-1]
    return count
def get_all_imgs(n_img, homepage, ID, mutil_skip=False, Time_skip=False):
    imgs_info=[]
    
    url = homepage +ID +'/'
    signal.signal(signal.SIGALRM, handler)
    if int(n_img) < 48:
        root_url = url + 'mediaindex?ref_=nm_mv_close'
        #print(root_url)
        session = requests.Session()
        signal.alarm(200)
        imgs_info = _get_imgs_info(url,root_url, session)
    else:
        n_page = int(math.ceil(int(n_img)/48))
        session = requests.Session()
        if n_page > 4:
            mutil_skip = True
            Time_skip = True
        for i in range(n_page):
            root_url = url + 'mediaindex?page='+str(i+1)+'&ref_=nm_mv_close'
            signal.alarm(200)
            continue
            try:
                imgs_info.extend(_get_imgs_info(url, root_url, session, mutil_skip=mutil_skip, Time_skip=Time_skip))
            except:
                print('time out')
                continue
     
    return imgs_info
# save all gallarg imags based on the list of img url

def _get_imgs_info(url, root_url, session, mutil_skip=False, Time_skip=False):

    imgs_info = []
    img_info = dict()

    gallery_page = session.get(root_url)
    #***************************#

    gallery_tree = html.document_fromstring(gallery_page.content) 
   
    for i, info in enumerate(gallery_tree.xpath('//div[@class= "media_index_thumb_list"]/a/@href')):
        img_info=dict()
        img_id = info.split('/')[-1].split('?')[0]
        subimg_url =  url + 'mediaviewer/' + img_id
        print(subimg_url)
        #subimg_page = requests.get(subimg_url)
        try:
            subimg_page = session.get(subimg_url, timeout=1000)        
        except requests.exceptions.ConnectionError:
            logging.basicConfig(filename='noresponse.log',level=logging.INFO)
            logging.info('no response for %s' % subimg_url)
            logging.error('Connection error when downloading image %s'% ID)
            continue
        except requests.exceptions.Timeout:
            logging.info('time out for %s' % subimg_url)
            logging.error('Timeout when downloading image %s' % subimg_url)
            continue
            
        else:
            subimg_tree = html.document_fromstring(subimg_page.content)
            
            img_src = subimg_tree.xpath('//meta[@itemprop="image"]/@content')
            img_high_src = img_src[0].split('@')[0] + '._V1_.jpg'
            img_descpt = subimg_tree.xpath('//meta[@itemprop="description"]/@content')
            if mutil_skip:
                if len(img_descpt[0].split(',')) > 3 or len(img_descpt[0].split('and')) > 2:
                    continue
            if Time_skip:
                if len(re.findall(r'\d+', img_descpt[0])) == 0:
                    continue
            img_info['description'] = img_descpt
            img_info['original'] = img_high_src
            img_info['low'] = img_src

        imgs_info.append(img_info)

    return imgs_info




    
