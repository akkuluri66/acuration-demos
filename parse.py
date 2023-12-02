import xml.etree.ElementTree as ET
import requests
from concurrent.futures import ThreadPoolExecutor
import os
from bs4 import BeautifulSoup
import re

def parse_sitemap(sitemap_path):
    url_list = set()
    try:
        # Parse the XML file
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # Find all URL elements within the sitemap
        for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            url_list.add(loc)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    return list(url_list) 
urls = parse_sitemap(r"C:\Users\akkul\OneDrive\Desktop\MyAcuration\enelx_sitemap.xml")

print(len(urls))

def clean_html_and_extract_text(html_text):
    try:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')

        # Remove HTML tags and get plain text
        text = soup.get_text(separator=' ', strip=True)

        # Remove special characters and extra whitespaces
        cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove non-alphanumeric characters

        # Normalize the text (convert to lowercase)
        cleaned_text = cleaned_text.lower()

    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        return None

    return cleaned_text
def crawl_url(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            extracted_text = clean_html_and_extract_text(html_content)
            
            # Sanitize the URL to create a valid filename
            filename = url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
            
            # Store the HTML content and extracted text in separate files within the folder
            save_to_file(html_content, folder_path, f"{filename}_html.html")
            save_to_file(extracted_text, folder_path, f"{filename}_extracted_text.txt")
        else:
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching content from {url}: {e}")

def save_to_file(content, folder_path, filename):
    try:
        # Create directory and intermediate directories if they don't exist
        os.makedirs(folder_path, exist_ok=True)

        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error saving content to file: {e}")

# Example usage of crawl_url function
for url in urls:
    crawl_url(url, r"C:\Users\akkul\OneDrive\Desktop\MyAcuration\Html_text")


print("DONE!...")
