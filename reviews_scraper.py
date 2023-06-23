#import the libraries
import os
import time
import numpy as np
import pandas as pd
import math

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#create a function to scrape any Glassdoor company review page
#the code  works in Jun 2023 but the html content of Glassdoor webpages changes 
#please inspect the webpage and make the necessary changes to html tags 

def review_scraper(url):
    #scraping the web page content
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser") 

    #define some lists
    Summary=[]
    Date_n_JobTitle=[]
    Date=[]
    JobTitle=[]
    AuthorLocation=[]
    OverallRating=[]
    Pros=[]
    Cons=[]  

  #get the Summary
    for x in soup.find_all('h2', {'class':'mb-xxsm mt-0 css-93svrw el6ke055'}):
        Summary.append(x.text)

  #get the Posted Date and Job Title
    for x in soup.find_all('span', {'class':'middle common__EiReviewDetailsStyle__newGrey'}):
        Date_n_JobTitle.append(x.text)

  #get the Posted Date
    for x in Date_n_JobTitle:
        Date.append(x.split(' -')[0])

  #get Job Title
    for x in Date_n_JobTitle:
        JobTitle.append(x.split(' -')[1])

  #get Author Location
    for x in soup.find_all('span', {'class':'middle'}):
        AuthorLocation.append(x.text)

  #get Overall Rating
    for x in soup.find_all('span', {'class':'ratingNumber mr-xsm'}):
        OverallRating.append(float(x.text))

  #get Pros
    for x in soup.find_all('span', {'data-test':'pros'}):
        Pros.append(x.text)

  #get Cons
    for x in soup.find_all('span', {'data-test':'cons'}):
        Cons.append(x.text)

  #combining together
    Reviews = pd.DataFrame(list(zip(Summary, Date, JobTitle, AuthorLocation, OverallRating, Pros, Cons)), 
                    columns = ['Summary', 'Date', 'JobTitle', 'AuthorLocation', 'OverallRating', 'Pros', 'Cons'])
  
    return Reviews

#paste the url to the first page of the company's Glassdoor reviews
input_url="https://www.glassdoor.com/Reviews/Gates-Corporation-Reviews-E2794.htm"

#scraping the first page content
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(input_url+str(1)+".htm?sort.sortType=RD&sort.ascending=false",headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html.parser") 

#check the total number of reviews
countReviews = soup.find('div', {'data-test':'pagination-footer-text'}).text
countReviews = float(countReviews.split(' Reviews')[0].split('of ')[1].replace(',',''))

#calculate the max number of pages (assuming 10 reviews a page)
countPages = math.ceil(countReviews/10)

#setting maxPage to 1 for testing first page. Uncomment line right below it to scrape all pages.
maxPage = 1
#maxPage = countPages + 1

#scraping multiple pages of company glassdoor review
#requests.get(input_url, headers = {'User-agent': 'your bot 0.1'})

output = review_scraper(input_url+str(1)+".htm?sort.sortType=RD&sort.ascending=false")
for x in range(2,maxPage):
    url = input_url+"_P"+str(x)+".htm?sort.sortType=RD&sort.ascending=false"
    #req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    reviews = review_scraper(url)
    output = pd.concat([output, reviews], ignore_index=True)
    time.sleep(15)     #timeout to avoid HTTP errors   


#display the output
display(output)

#save to csv
output.to_csv('output.csv', index=False)
