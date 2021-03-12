#!/usr/bin/env python3
import requests
import validators
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from urllib.request import urlopen
import urllib.request
from urllib.parse import quote
from pprint import pprint


def get_links(my_url, extension='') -> list:
    """Gets the links from a url. Optionally matches a particular extension

    :param my_url: The URL at which links to be extracted are located
    :param extension: The extension inside the target links. Set this to 'pdf' for only targetting pdf links
    :returns: A list of links

    """
    links = []
    html = urlopen(my_url).read()
    html_page = bs(html, features="lxml")
    og_url = html_page.find("meta",  property = "og:url")
    base = urlparse(my_url)
    print("base",base)
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        if extension != '':
            if current_link.endswith(extension):
                if og_url:
                    print("currentLink",current_link)
                    links.append(og_url["content"] + current_link)
                else:
                    links.append(base.scheme + "://" + base.netloc + current_link)
        else:
            links.append(current_link)

    return links


def get_pdf(link, dest_folder):
    """Gets the pdf at a particular http(s) url

    :param link: The link which points to a pdf file
    :param dest_folder: The folder to which the file is to be saved
    :returns:

    """
    try:
        r = requests.get(link)
        dest = dest_folder + '/' + link.split('/')[-1] + '.pdf'
        with open(dest, 'wb') as outfile:
            outfile.write(r.content)
            print('\n--> Getting {} and saving to {}...'.format(link, dest))
    except Exception as e:
        print("\n--> Unable to download the file: {} \n".format(e))


def main(mainUrl, dest_folder):
    """ Gets links from a url, then appends /pdf/ after the 'doi' element in the URL, then fetches each pdf from it.
    Was done to fetch all PDFs from a conference website. The default URL gets all PDFs from the HRI 2021 website ToC page

    :param mainUrl: The URL at which the PDF pointing links are located
    :param dest_folder: The folder in which all downloads are to be saved
    :returns:

    """
    urls = get_links(mainUrl)

    urls_new = []
    for u in urls:
        a = u.split('/')
        if 'doi' in a:
            a.insert(a.index('doi')+1, 'pdf')
            urls_new.append('/'.join(a))

    print('\nObtained {} links'.format(len(urls_new)))
    for url in urls_new[1:]:
        try:
            get_pdf(url, dest_folder)
        except Exception as e:
            continue


# the main default function call
main('https://humanrobotinteraction.org/2021/toc.html', './pdfs')
