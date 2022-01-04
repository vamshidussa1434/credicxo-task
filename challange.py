from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import URLError, HTTPError
from csv import reader
import json



fileName = 'Amazon Scraping - Sheet1.csv'
baseURL = 'https://www.amazon'
fileObj = open(fileName, newline='')
csvReader = reader(fileObj)
head = next(csvReader)
jsonData = []



def connectionToScrap(url):
    try:
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        imageDOM = page_soup.find(id='imgBlkFront')
        imageURL = imageDOM['src']
        titleDOM = page_soup.find(id='productTitle')
        title = titleDOM.text
        priceDOM = page_soup.find('span', {
            "class": 'a-size-base a-color-price a-color-price'
        })
        price = priceDOM.text
        productDetailsUL = page_soup.find('ul', {
            'class': 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list',
        })
        detailLIs = productDetailsUL.findAll('li')
        productDetails = {}
        for node in detailLIs:
            text = node.find('span').get_text()
            dataArray = text.replace(' ', '').split('\n')
            key = dataArray[0]
            value = dataArray[-1]
            productDetails[key] = value
            print(key, value)
        detailedObj = {
            price,
            title,
            productDetails,
            imageURL
        }
        jsonData.append(detailedObj)
    except HTTPError:
        pass
    except URLError:
        pass
# connectionToScrap('http://www.amazon.de/dp/000109825X')
for row in csvReader:
    country = row[-1]
    asin = row[-2]
    URLString = baseURL + '.' + country + '/dp/' + asin
    connectionToScrap(URLString)   