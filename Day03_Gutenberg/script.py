import requests,json,lxml
from fake_useragent import UserAgent
from bs4  import BeautifulSoup
import re
""" Function to extract the top 100 books with authors """
def get_data(baseUrl,headers):
    try:
        response = requests.get(baseUrl,headers=headers)
        if response.status_code!=200:
            print(f"Failed to request {baseUrl}. Status code: {response.status_code}")
            return None
    except Exception as e :
        print(f"Error requesting URL: {e}")
        return None
    
    try:
        soup = BeautifulSoup(response.text,"lxml")
        ol_element = soup.select_one('ol')
        
        if ol_element is None:
            print("Could not find ordered list on the page")
            return None
            
        data = [c.get_text(strip=True) for c in ol_element.find_all('li')]
        
        if not data:
            print("No list items found in the ordered list")
            return None
            
        return data
        
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None
    
def get_books(data):
    books_authors=dict()
    
    for c in data:
        
        match = re.search(r'\s+by\s+', c) #looking for 'by' to find the author name 
        if match:
            split_index = match.start() #where the match starts 
            book = c[:split_index].strip()
            author = c[match.end():].strip() #where the match ends 
            
            
            author = re.sub(r'\s*\(\d+\)$', '', author) # remove the number between () int the author's name
            
            books_authors[book] = author
        else:
            clean_title = re.sub(r'\s*\(\d+\)$', '', c.strip())  # remove the number between () int the title
            books_authors[clean_title] = "Author not found"
    
    return books_authors

# testing 
def main():
    headers={"User-Agent":UserAgent().random}
    baseUrl="https://www.gutenberg.org/browse/scores/top"
    data=get_data(baseUrl,headers)
    
    if data is None:
        print("Failed to retrieve book data")
        return
        
    books_authors = get_books(data)
    
    if not books_authors:
        print("No books found")
        return
    
    print(f"\nTop {len(books_authors)} Books from Project Gutenberg:")
    print("=" * 60)
    
    for i, (book, author) in enumerate(books_authors.items(), 1):
        print(f"{i:2d}. {book}")
        print(f"    Author: {author}")
        print()
if __name__=="__main__":
    main()