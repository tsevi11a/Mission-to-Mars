#pip install splinter
#pip install webdriver-manager

# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Set executable path 
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# **Title and Summary**
# Create function to scrape news title and paragraph summary
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Look for the <div /> tag and its descendent (select_one returns the first match)
        slide_elem = news_soup.select_one('div.list_text') 

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text() #gets just the text (i.e. in above result, all HTML stuff included)

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# **Featured Images**
# Create function to scrape the featured image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1] #indexing to stipulate to click second button
    full_image_elem.click()

    # The above code loads a new page, so we need to parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# **Mars Facts**
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0] #creates new df from HTML table
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth'] #assigning columns
    df.set_index('Description', inplace=True) #set description column as the index
    
    #convert df back to HTML ready code and add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # List all image links
    links = browser.find_by_css('a.product-item img')

    # Loop through image URLs
    for i in range(len(links)):
        hemisphere = {}
        
        # Loop through elements
        browser.find_by_css('a.product-item img')[i].click()
        
        # Get the href for image URLs
        sample_imgs = browser.links.find_by_text('Sample').first
        
        # Get Hemisphere titles
        hem_title = browser.find_by_css('h2.title').text
        
        # Add to hemisphere dictionary
        hemisphere['img_url'] = sample_imgs['href']
        hemisphere['title'] = hem_title  
        
        # Add hemisphere to hemisphere_image_urls
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate back to the beginning to get the next hemisphere image
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())










