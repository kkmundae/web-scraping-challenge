# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### NASA Mars News 

    # Visit url for NASA Mars News -- Latest News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    # Parse HTML with Beautiful Soup  
    soup = BeautifulSoup(html, "html.parser")

    # Get article title and paragraph text
    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    ### JPL Mars Space Image

    # Visit url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Go to 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    # Go to 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    # Get featured image
    a = image_soup.find('figure', class_='lede')
    image_url_2 = a.find('a')['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url_2}'

    ### Mars Facts

    # Visit Mars Facts webpage for interesting facts about Mars
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    tables = pd.read_html(facts_url)
    facts = tables[0]

    # Assign columns and index
    facts.columns = ['Description', 'Value']
    facts.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string
    facts = facts.to_html(classes="table table-striped")

    ### Mars Hemispheres

    # Visit USGS webpage for Mars hemispehere images
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    hemi_soup = BeautifulSoup(html, 'html.parser')

    # Create dictionary to store titles & links to images
    hemi_image_urls = []

    # Retrieve all elements that contain image information
    hemi_all = hemi_soup.find('div', class_='result-list')
    mars_hemis = hemi_all.find_all('div', class_='item')

    # Iterate through each image
    for i in mars_hemis:
        title = i.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = i.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemi_image_urls.append({"title": title, "img_url": image_url})

    ### Store Data

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts": facts,
        "hemisphere_image_urls": hemi_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()
