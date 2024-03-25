import csv  
import requests  #handle module for making HTTP requests
from bs4 import BeautifulSoup #for webscrapping
from urllib.parse import urlparse,urljoin 

def extract_all_links(url, timeout = 20):
    try:
        response = requests.get(url,timeout=timeout) #send http get request to the pre
        if response.status_code == 200:   #check if response successful
            soup = BeautifulSoup(response.text,'html.parser') #parse the content of response
            links = [a['href'] for a in soup.find_all('a',href = True)] #extract all href
            links = [urljoin(url,link)for link in links]
            return links
        else:
            print(f"Failed to retrieve data from '{url}'. Status code: {response.status_code}")
            return[]
    except(requests.exceptions.RequestException,requests.exceptions.Timeout) as e:
        print(f"Error connecting to {url}: {e}")  #print error msg
        return[]

def save_links_to_csv(links, csv_filename):
    
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) #create a csv writer object
        csv_writer.writerow(['Link'])   #wrte the header row 
        for link in links:
            csv_writer.writerow([link])  #write each link to csv file
                     
def is_social_media_url(url):
    
    social_media_domain = ['twitter.com','facebook.com','instagram.com']
    for domain in social_media_domain:
        if domain in url:
            return True
    return False

def extract_specific_content(url, timeout = 20):
    
    try:
        response  = requests.get(url,timeout=timeout) #get http req
        response.raise_for_status()   #to html content parse
        soup = BeautifulSoup(response.text,'html.parser')
        
        if is_social_media_url(url):
            print(f"Skipping {url} because it's a social media link.")
            return None, None, None, None ,None , 'Category not found'
        
        heading_element = soup.find('h1', class_='alith_post_title')
        author_element = soup.find('div', class_ = 'article_author_name')
        publication_date_element = soup.find('div', class_='article_date')
        content_container = soup.find('div', class_ = 'post-content')
        
        heading = heading_element.text.strip() if heading_element else 'Heading not found' 
        author = author_element.text.strip() if author_element else 'author not found'
        publication_date_raw = publication_date_element.text.strip() if publication_date_element else 'date not found'
        publication_date = publication_date_raw.replace('Published:','').strip() 
        content = content_container.get_text(separator=' ',strip= True) if content_container else 'contetnt not found'
        
        url_parts= urlparse(url).path.split('/')
        category = next((part for part in url_parts if part), 'Category not found')
        
        return heading, author, publication_date, content, url, category
    
    except(requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        print(f'Failed to retrive content from {url}. Error: {e}')
        return None , None, None, None , url , 'Category not found'
    
    
def save_to_csv(data, csv_file_path):
    
    with open(csv_file_path, 'a', newline= '', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Heading' ,'Author','publication_date','Source','content','Link','Category'])
        csv_writer.writerow(data)
        


def main():
    csv_file_path = 'Jimalayn_time_data.csv'
    with open(csv_file_path, 'w', newline='', encoding= 'utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Heading' ,'Author','publication_date','Source','content','Link','Category'])
        
    url = 'https://thehimalayantimes.com/'
    links = extract_all_links(url)
    csv_filename = 'data_links.csv'
    save_links_to_csv(links, csv_filename)
    
    with open(csv_filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        urls = [row['Link'] for row in reader]
        
        
    for url in urls:
        if not urlparse(url).scheme: # parse does split 
            url = urljoin('https://', url)
            
        if urlparse(url).netloc and not is_social_media_url(url):   #netloc does extract without https 
            try:
                heading, author , publication_date, content, link, category = extract_specific_content(url)
                if heading is not None and author is not None and content is not None:
                    data_to_save = [heading,author,publication_date,'Himalayn times', content, link, category]
                    print(f"Data for{url}:\nHeading: {heading}\nAuthor: {author}\nPublication Date:{publication_date}\nSource: The_Himalayn_times\nContent: {content}\nLinks: {link}\n Category : {category}\n")
                    save_to_csv(data_to_save, csv_file_path)
                    print(f"Data Saved for {url}")
            except Exception as e:
                print(f"Error processing {url}: {e}")
        
        else:
            print(f"Invalid URL format or social media link : {url}")
            
            
if __name__ == "__main__":
    main()
                    
                    
                    
            
        
    

        
        
    
        
        

        
        
    
            


        



