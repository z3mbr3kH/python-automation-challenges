#!/bin/python3 
import requests,argparse,lxml,json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



#Day 1: Scraping the HackerNews' Titles 

def scraper(base_url):
    headers={"User-Agent":UserAgent().random,"Accept-Language": "en-US,en;q=0.9"}
    try:

        r= requests.get(base_url,headers=headers)
    except Exception as e:
        print(f"Request failed due to :{e}")
    if r.status_code!=200:
        print(f"Failed getting the given page! Please try again")
        exit(1)
    soup=BeautifulSoup(r.text,"lxml")
    posts=soup.select(".body-post")
    titles=[]
    for post in posts:
        title = post.select_one(".home-title")
        titles.append(title.get_text(strip=True))
    return titles

def saver(titles,filename):
    data={}
    i=0
    for title in titles:
        data.update({f"title {i}":title})
        i+=1
    with open(filename,"w") as f:
        json.dump(data,f,indent=4)
    print(f"[+] Titles saved to {filename} file")

def main():
    parser=argparse.ArgumentParser(prog="Hacker News Scraper",description="This is a simple scrapper made for thehackernews.com website to scrap titles")
    parser.add_argument('-u','--url',help="Add the url under thehackernews domain")
    parser.add_argument('-o','--output',help="Save results to a json file (provide filename)")
    args=parser.parse_args()
    if args.url:
        if "thehackernews.com" in args.url:
            titles = scraper(args.url)
            for title in titles:
                print(title)
            
            if args.output:
                saver(titles, args.output)
        else:
            print("Please provide a valid url under thehackernews domain")
            exit(1)
    else:   
        parser.print_help()
        exit(1)

if __name__=="__main__":
    main()