#%%
from bs4 import BeautifulSoup
import requests

from time import time

#%%


def find_title(head):
    title = head.find('meta', {'property' : "og:title"})
    if title != None:
        return(title['content'])
    title = head.find('meta', {'name' : "twitter:title"})
    if title != None:
        return(title['content'])
    else:
        return None

def find_desc(head):
    desc = head.find('meta', {'property' : "og:description"})
    if desc != None:
        return(desc['content'])
    desc = head.find('meta', {'name' : "twitter:description"})
    if desc != None:
        return(desc['content'])
    desc = head.find('meta', {'name' : "description"})
    if desc != None:
        return(desc['content'])
    else:
        return None

def find_domain(head):
    domain = head.find('link', {'rel' : "canonical"})
    if domain != None:
        return(domain['href'])
    domain = head.find('meta', {'property' : "og:url"})
    if domain != None:
        return(domain['content'])
    else:
        return None
        
def find_img(head):
    img = head.find('meta', {'property' : "og:image"})
    if img != None:
        return(img['content'])
    img = head.find('link', {'rel' : "image_src"})
    if img != None:
        return(img['href'])
    img = head.find('meta', {'name' : "twitter:image"})
    if img != None:
        return(img['content'])
    else:
        return None
        
def link_routine(url):
    ts = time()
    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    head = soup.find('head')
    info = {}
    try:
        info['title'] = find_title(head)
        info['desc'] = find_desc(head)
        info['domain'] = find_domain(head)
        info['img'] = find_img(head)
    except:
        return None
    print(url, ' took %2.3f seconds' % (time() - ts))
    return info


# %%


# %%
