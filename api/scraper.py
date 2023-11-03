import requests
from bs4 import BeautifulSoup

def scrape(question: str)-> list:
    # removing question mark from the text
    txt = question.split('?')

    # changing the text to query format
    tmp_search_txt = ''
    for each in txt:
        if each:
            tmp_search_txt+= each 
    search_txt = ''
    for each in tmp_search_txt.split():
        search_txt+=each+'+'
    search_txt = search_txt[:-1]

    # Urls
    urls = []
    url1 = 'https://www.google.com/search?q='+search_txt
    urls.append(url1)
    url2 = 'https://www.bing.com/search?q='+search_txt
    urls.append(url2)

    contents = []

    for e_url in urls:
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(e_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the page content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                text_content = soup.get_text()
                contents.append(text_content)
        except:
            pass

    return contents