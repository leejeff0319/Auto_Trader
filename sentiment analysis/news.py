from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def setup_selenium():
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_article_content(soup):
    '''Get text present from first <p> tag up to the first <h2> tag of each article'''
    content = []
    current_tag = soup.find('p')  

    while current_tag and current_tag.name != 'h2':
        if current_tag.name == 'p':
            content.append(current_tag.get_text(strip=True))
        current_tag = current_tag.find_next()  # Move to next tag
    
    return ' '.join(content)

def fetch_article(link):
    driver = setup_selenium()
    driver.get(link)
    article_soup = article_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get date and time of published article
    time_tag = article_soup.find('time')
    article_info = {
        'datetime': time_tag['datetime'] if time_tag else ''
    }

    # Get stocks affected


    # Get content
    content = fetch_article_content(article_soup)
    article_info['content'] = content
    
    driver.quit()
    return article_info

def scrape_yfinance_news():
    driver = setup_selenium()
    driver.get('https://finance.yahoo.com/news')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    class_name = "clamp tw-line-clamp-3 sm:tw-line-clamp-2 svelte-13zydns"

    links = [h3.find_parent('a')['href'] for h3 in soup.find_all('h3', class_=class_name)]
    driver.quit()

    news = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_link = {executor.submit(fetch_article, link): link for link in links}
        for future in as_completed(future_to_link):
            link = future_to_link[future]
            try:
                additional_details = future.result()
                article_details = {
                    'title': additional_details.get('title', ''),
                    'link': link
                }
                article_details.update(additional_details)  # Merge fetched details
                news.append(article_details)
            except Exception as e:
                print(f"Failed to fetch details for {link}: {str(e)}")

    # for h3 in soup.find_all('h3', class_=class_name):
    #     link = h3.find_parent('a', href=True)
    #     if link:
    #         title = h3.get_text(strip=True)
    #         full_link = f'https://finance.yahoo.com{link["href"]}' if link["href"].startswith('/') else link["href"]
    #         article_details = {
    #             'title': title,
    #             'link': full_link
    #         }
    #         additional_details = fetch_article(full_link)
    #         article_details.update(additional_details)
    #         news.append(article_details)
    # driver.quit()
    
    return news