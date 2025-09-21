#!../.venv/bin/python3 
import requests
import argparse
import lxml
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



#Day 1: Scraping the HackerNews' Titles  and links 

def get_titles(base_url,headers):
    print(f"[+] Starting to extract titles from: {base_url}")
    print(f"[+] Making HTTP request...")
    try:
        r= requests.get(base_url,headers=headers)
        print(f"[✓] Request successful (Status: {r.status_code})")
    except Exception as e:
        print(f"[✗] Request failed due to :{e}")
        exit(1)
    if r.status_code!=200:
        print(f"[✗] Failed to fetch {base_url}! Status code: {r.status_code}")
        exit(1)
    
    print(f"[+] Parsing HTML content...")
    soup=BeautifulSoup(r.text,"lxml")
    posts=soup.select(".body-post")
    print(f"[+] Found {len(posts)} posts to process")
    
    titles=[]
    for i, post in enumerate(posts, 1):
        title = post.select_one(".home-title")
        if title:
            title_text = title.get_text(strip=True)
            titles.append(title_text)
            print(f"[+] Extracted title {i}/{len(posts)}: {title_text[:60]}{'...' if len(title_text) > 60 else ''}")
        else:
            print(f"[!] No title found for post {i}")
    
    print(f"[✓] Successfully extracted {len(titles)} titles")
    return titles


def get_links(base_url,headers):
    print(f"[+] Starting to extract links from: {base_url}")
    print(f"[+] Making HTTP request...")

    try:
        r= requests.get(base_url,headers=headers)
        print(f"[✓] Request successful (Status: {r.status_code})")
    except Exception as e:
        print(f"[✗] Request failed due to :{e}")
        exit(1)
    if r.status_code!=200:
        print(f"[✗] Failed to fetch {base_url}! Status code: {r.status_code}")
        exit(1)
    
    print(f"[+] Parsing HTML content...")
    soup=BeautifulSoup(r.text,"lxml")
    a_tags=soup.find_all('a') # extract links from a tags 
    print(f"[+] Found {len(a_tags)} anchor tags to process")
    
    links=[a_tag['href'] for a_tag in a_tags if a_tag.get('href')]
    print(f"[+] Extracted {len(links)} raw links")
    
    return test_links(links, headers)

def test_links(urls,headers):
    print(f"[+] Starting link validation process...")
    print(f"[+] Testing {len(urls)} links for validity...")
    valid_urls=[]
    base_url="https://thehackernews.com"
    
    for i, url in enumerate(urls, 1):
        if url.startswith("https"):
            test_url=url
        else:
            test_url=f"{base_url}{url}"
        
        try:
            print(f"[+] Testing link {i}/{len(urls)}: {test_url[:50]}{'...' if len(test_url) > 50 else ''}")
            r=requests.get(test_url,headers=headers)
            if r.status_code==200:
                valid_urls.append(test_url)
                print(f"[✓] Valid link found ({len(valid_urls)} total)")
            else:
                print(f"[!] Invalid link (Status: {r.status_code})")
        except Exception as e:
            print(f"[!] Error testing link: {str(e)[:40]}{'...' if len(str(e)) > 40 else ''}")
            continue
    
    print(f"[✓] Link validation complete! Found {len(valid_urls)} valid links out of {len(urls)} tested")
    return valid_urls
            


def saver(data_list, filename, data_type):
    print(f"[+] Preparing to save {len(data_list)} {data_type}s to {filename}...")
    
    data = {}
    for i, item in enumerate(data_list):
        data.update({f"{data_type} {i}": item})
    
    print(f"[+] Writing data to file...")
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[✓] Successfully saved {len(data_list)} {data_type}s to {filename}")
        print(f"[+] File size: {len(json.dumps(data, indent=4))} bytes")
    except Exception as e:
        print(f"[✗] Error saving file: {e}")
        exit(1)
    


def main():
    print("=" * 60)
    print("🕷️  HACKER NEWS SCRAPER STARTED")
    print("=" * 60)
    
    parser=argparse.ArgumentParser(prog="Hacker News Scraper",description="This is a simple scrapper made for thehackernews.com website to scrap titles")
    parser.add_argument('-u','--url',help="Add the url under thehackernews domain")
    parser.add_argument('-t','--type',help="Choose the type of the scraper",choices=["link","title"])
    parser.add_argument('-o','--output',help="Save results to a json file (provide filename)")
    args=parser.parse_args()
    
    print(f"[+] Initializing scraper with random User-Agent...")
    headers={"User-Agent":UserAgent().random,"Accept-Language": "en-US,en;q=0.9"}
    print(f"[+] User-Agent: {headers['User-Agent'][:50]}{'...' if len(headers['User-Agent']) > 50 else ''}")

    if args.url:
        print(f"[+] Target URL: {args.url}")
        print(f"[+] Scraper type: {args.type}")
        if args.output:
            print(f"[+] Output file: {args.output}")
        else:
            print(f"[+] Output: Console only (no file will be saved)")
        print("-" * 60)
        
        if "thehackernews.com" in args.url:
            if args.type=="title":
                print(f"[+] Starting TITLE extraction...")
                titles = get_titles(args.url,headers=headers)
                
                print(f"\n[+] Displaying extracted titles:")
                print("-" * 40)
                for i, title in enumerate(titles, 1):
                    print(f"{i:2d}. {title}")
                print("-" * 40)
            
                if args.output:
                    saver(titles, args.output, "title")
                else:
                    print(f"[!] No output file specified. Results displayed above only.")
                    
            elif args.type=="link":
                print(f"[+] Starting LINK extraction...")
                links=get_links(args.url,headers=headers)
                
                print(f"\n[+] Displaying extracted links:")
                print("-" * 40)
                for i, link in enumerate(links, 1):
                    print(f"{i:2d}. {link}")
                print("-" * 40)
                
                if args.output:
                    saver(links, args.output, "link")
                else:
                    print(f"[!] No output file specified. Results displayed above only.")
        else:
            print("[✗] ERROR: Please provide a valid url under thehackernews domain")
            exit(1)
            
        print("\n" + "=" * 60)
        print("✅ SCRAPER COMPLETED SUCCESSFULLY")
        print("=" * 60)
    else:   
        parser.print_help()
        exit(1)

if __name__=="__main__":
    main()