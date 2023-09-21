import requests
from bs4 import BeautifulSoup

def getPage(url):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
       req = requests.get(url,headers=headers)
    except requests.exceptions.RequestException:
       return None
    return BeautifulSoup(req.text,'html.parser')

# Function to scrape reference links from a CVE ID page
def scrape_references(cve_id):
    try:
        # Construct the URL with the provided CVE ID
        url = f'https://vulmon.com/vulnerabilitydetails?qid={cve_id}'

        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor (a) tags with an href starting with 'https://www.exploit-db'
        exploit_links = []
        for link in soup.find_all('a', href=lambda href: href and href.startswith(f'/exploitdetails?qidtp=exploitdb')):
            href = link.get('href')
            if href:
                exploit_links.append(href)

        return exploit_links

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def download_content(url, save_path):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)

        # Save the content to the specified path
        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def exploit_info(href):
    
    url=f"https://vulmon.com{href}"
    
    soup = getPage(f"{url}")
    if soup:
   # Extract the relevant information
     title=soup.select_one('h1.titleclass').text
     list =soup.select('div.list>div.item')[0:3]
     download =soup.find('a', href=lambda href: href and href.startswith(f'https://www.exploit-db.com/download'))['href']
     info_list=[]
     for ls in list:
         info_list.append(ls.text)
     
     return title,info_list
    else:
      print("Section not found on the page.")
      return None
 
 


def get_info_from_links(cve_id):
    links=scrape_references(cve_id)
    info=[]
    if links:
        for link in links:
            info.append(exploit_info(link))
        return info
    else:
        links ="Not Found"
        return links
    
print(get_info_from_links('cve-2017-0144'))