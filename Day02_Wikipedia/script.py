import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from weasyprint import HTML, CSS

# Day 2: Scraping Wikipedia featured article and external links


def get_article_link(base_url, headers):
    print(f"[→] Fetching Wikipedia main page: {base_url}")
    
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code != 200:
            print(f"[✗] Failed to fetch {base_url}! Status code: {response.status_code}")
            return
        print("[✓] Wikipedia main page fetched successfully")
    except Exception as e:
        print(f"[✗] Request failed: {e}")
        return

    print("[→] Parsing HTML to find featured article...")
    soup = BeautifulSoup(response.text, "lxml")
    
    featured_section = soup.select_one(".MainPageBG")
    if not featured_section:
        print("[✗] Could not find featured article section")
        return
    
    article_paragraph = featured_section.select_one('p')
    if not article_paragraph:
        print("[✗] Could not find article paragraph")
        return
    
    print("[→] Looking for article link in featured section...")
    article_links = article_paragraph.find_all('a')
    article_link = ""
    
    for link in article_links:
        link_text = link.text.lower().replace('\xa0', ' ')
        if "full article" in link_text or "this article" in link_text:
            article_link = f"https://en.wikipedia.org{link['href']}"
            break
    
    if article_link:
        print(f"[✓] Found featured article link: {article_link}")
        return article_link
    else:
        print("[✗] Could not find article link")
        return None


def extract_external_links(main_content):
    
    print("[→] Extracting external links from article...")
    external_links = set()
    a_tags = main_content.find_all('a')
    
    print(f"[→] Found {len(a_tags)} total links to analyze...")
    
    for a in a_tags:
        if a.get('href'):
            link = a['href']
            if link.startswith("https") and "wikipedia" not in link:
                external_links.add(link)
    
    print(f"[✓] Found {len(external_links)} external links")
    return external_links


def scrape_article(article_link, headers):
    print(f"[→] Starting to scrape article: {article_link}")
    
    try:
        print("[→] Fetching article content...")
        r = requests.get(article_link, headers=headers)
        if r.status_code != 200:
            print(f"[✗] Failed to fetch {article_link}! Status code: {r.status_code}")
            exit(1)
        print("[✓] Article content fetched successfully")
    except Exception as e:
        print(f"[✗] Request failed: {e}")
        exit(1)
    
    print("[→] Parsing HTML content...")
    soup = BeautifulSoup(r.text, "lxml")
    main_content = soup.select_one(".mw-content-ltr")
    
    if not main_content:
        print("[✗] Could not find main content section")
        exit(1)
    
    print("[✓] HTML content parsed successfully")
    content_html = str(main_content)
    

    external_links = extract_external_links(main_content)
    
    print("[→] Creating PDF from article content...")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Wikipedia Featured Article</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1, h2, h3 {{ color: #0645ad; }}
            p {{ line-height: 1.6; }}
        </style>
    </head>
    <body>
        {content_html}
    </body>
    </html>
    """
    
    try:
        HTML(string=html_content).write_pdf("Wikipedia_Featured_Article.pdf")
        print("[✓] Article saved as PDF: Wikipedia_Featured_Article.pdf")
    except Exception as e:
        print(f"[✗] An Error occurred while creating the pdf: {e}")
        exit(1)
    
    return external_links    




def main():
    print("=== Wikipedia Featured Article Scraper ===")
    print()
    
    base_url = "https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article"
    headers = {
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    article_link = get_article_link(base_url, headers)
    if article_link:
        print()
        external_links = scrape_article(article_link, headers=headers)
        
        print()
        print("=== External Links Found ===")
        if external_links:
            print(f"[✓] Found {len(external_links)} external links:")
            for i, link in enumerate(sorted(external_links), 1):
                print(f"  {i:2d}. {link}")
        else:
            print("[!] No external links found in the article")
    else:
        print("[✗] Could not proceed without article link")
        
    print()
    print("=== Scraping completed ===")


if __name__ == "__main__":
    main()