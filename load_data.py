import re
from langchain_community.document_loaders import RecursiveUrlLoader
import bs4
from typing import List
from langchain_core.documents import Document

#-----------------EXTRACT TEXT------------------------#
def bs4_extractor(html: str) -> str:
    soup = bs4.SoupStrainer(name=("h1","h3", "h2", "p", "ol",))
    soup = bs4.BeautifulSoup(html, "html.parser", parse_only=soup)
    soup = re.sub(r"think-cell Suite has arrived. Discover your library and new tools.\n   \n  Resources  \n", "", soup.text).strip()
    soup = re.sub(r'\n+', ' ', soup).strip()
    soup = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', soup)
    soup = re.sub(r'Share Products Order Download Resources Career Company', '', soup)
    return soup

#-------------EXTRACT METADATA -----------------------#
def custom_metadata_extractor(html: str, url: str) -> dict:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    image_urls = []

    for picture in soup.find_all('picture'):
        jpg_url = None

        # Check all <source> tags for jpg
        for source in picture.find_all('source'):
            src = source.get('srcset', '')
            if '.jpg' in src:
                jpg_url = src
                break  # take the first .jpg and stop

        # Fallback to <img> tag if no .jpg found in <source>
        if not jpg_url:
            img_tag = picture.find('img')
            if img_tag and '.jpg' in img_tag.get('src', ''):
                jpg_url = img_tag['src']

        if jpg_url:
            image_urls.append(jpg_url)

    return {'source': url, 'image_urls': image_urls}

#----------------LOAD DATA FROM ALL LINKS---------------#
def load_data(URL: str, BASE_URL: str)-> List[Document]:
    loader = RecursiveUrlLoader(
        URL,
        max_depth=6,
        extractor=bs4_extractor,
        metadata_extractor=custom_metadata_extractor,
        check_response_status=True,
        prevent_outside=True,
        base_url=BASE_URL
    )
    return loader.load()