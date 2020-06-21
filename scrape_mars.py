# scrape_mars.py
# Author: James Ye

import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def scrape():
    # get the browser ready
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #### ---- NASA Mars News ---------------

    # url of NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
 
    browser.visit(news_url)
    time.sleep(5)

    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')

    news_results = news_soup.find_all('div', class_='list_text')
    latest_news = news_results[0]

    news_title = latest_news.find('div', class_='content_title').text
    print(f"news_title: {news_title}")
    news_p = latest_news.find('div', class_='article_teaser_body').text
    print(f"news_p: {news_p}")

    ### ---- JPL Mars Space Images - Featured Image -------

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)

    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info', wait_time=1)
    browser.click_link_by_partial_text('more info')
    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" + soup_jpl.find('img', class_='main_image')['src']
    print(f"featured_image_url: {featured_image_url}")

    ### ---- Mars Weather -------------------------------------
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(2)

    # find the first span element with text starting with 'InSight sol'
    mars_weather = browser.find_by_xpath('//span[starts-with(text(),"InSight sol")]').first.text
    print(f"mars_weather: {mars_weather}")

    ### ---- Mars Facts -------------------------------------
    space_facts_url = "https://space-facts.com/mars/"
    mars_facts_tables = pd.read_html(space_facts_url)
    df = mars_facts_tables[1]
    df.columns = ['Attributes', 'Mars', 'Earth']
    #df.columns = ['Attributes', 'Value']
    mars_facts_html = df.to_html(index=False)
    print(f"mars_facts_html:  {mars_facts_html} ")

    ### ---- Mars Hemispheres -------------------------------------
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    time.sleep(5)

    hem_soup = bs(browser.html, 'html.parser')
    description_divs = hem_soup.find_all('div', class_='description')

    # get titles and links to full size image page
    links = []
    titles = []
    for div in description_divs:
        link = "https://astrogeology.usgs.gov" + div.find('a', 'itemLink product-item')['href']
        print(link)
        links.append(link)
        title = div.find('h3').text.replace(" Enhanced", "")
        print(title)
        titles.append(title)

    # get image urls
    image_urls = []
    for link in links:
        browser.visit(link)
        time.sleep(2)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
        print(image_url)
        image_urls.append(image_url)

    hemisphere_image_urls = []
    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i], 'img_url':image_urls[i]})

    print(f"hemisphere_image_urls: {hemisphere_image_urls}")

    # close browser
    browser.quit()

    # pack the return dictionary
    data_dict = {
        'news_title' : news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'mars_facts_html' : mars_facts_html,
        'hemisphere_image_urls' : hemisphere_image_urls
    }

    return data_dict


if __name__ == "__main__":
    scrape()
