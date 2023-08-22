import requests
import lxml
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to retreive the next page
def getNextPage(soup):
    
    if not soup.find('a', attrs={'class': 's-pagination-item s-pagination-button s-pagination-next s-pagination-disabled'}):
        url = 'https://www.amazon.in/' + str(soup.find('a', attrs={'class':'s-pagination-item s-pagination-button'}).get('href'))
        return url
    else:
        return

# Function to get the price of the product from the product page
def getPrice(soup):
    try:
        price = soup.find("span", attrs={"class":"a-price-whole"})
        # print(price)
        #price_value = price.string
        price_string = price.text.strip()
    except AttributeError:
        price_string = ""
    return price_string

# Function to get the star rating
def getRating(soup):
    try:
        rating = soup.find("span", attrs={"id":"acrPopover"}).find('span', attrs={'class':'a-size-base a-color-base'})
        #print(rating)
        #rating_value = rating.string
        rating_string = rating.text.strip()
    except AttributeError:
        rating_string = ""
    return rating_string

# Function to get the number of ratings.reviews
def getReviews(soup):
    try:
        reviews = soup.find("span", attrs={"id":"acrCustomerReviewText"})
        #reviews_value = reviews.string
        reviews_string = reviews.text.strip()
    except AttributeError:
        reviews_string = ""
    return reviews_string

# Function to get the product description [NOT APPLICABLE]
def getDescription(soup):
    try:
        desc = soup.find("div", attrs={"id":"feature-bullets"}).find('span', attrs={'class':'a-list-item'})
        #desc_value = desc.string
        desc_string = desc.text.strip()
    except AttributeError:
        desc_string = ""
    return desc_string

# Function to get the ASIN number/code
def getAsin(soup):
    # Since the ASIN number can be at two different areas on the page based on the product, two methods are applied to get the ASIN number
    try:
        asinList = soup.find("table", attrs={"id": "productDetails_detailBullets_sections1"}).find_all('th')
        asin_value = ""
        #print(manuList)
        for asin in asinList:
            try:
                if 'ASIN' in asin.text:
                    #print("yes")
                    asin_value = asin.find_next_sibling().text
                    #print(manu_value)
                    break
            except AttributeError:
                asin_string = ""
                break
        asin_string = asin_value.strip()
    except AttributeError:
        asin_string = ""
    if asin_string == "":
        try:
            asinList = soup.find("div", attrs={"id": "detailBullets_feature_div"}).find_all("span", attrs={'class': 'a-text-bold'})
            #print(manuList)
            for asin in asinList:
                try:
                    if 'ASIN' in asin.text:
                        #print("yes 2")
                        asin_value = asin.find_next_sibling().text
                        asin_string = asin_value.strip()
                        #print(manu_value)
                        break
                except AttributeError:
                    asin_string = ""
                    break
        except AttributeError:
            asin_string = ""
        
    return asin_string


def getManufacturer(soup):
    # Since the manufacturer name can be at two different areas on the page based on the product, two methods are applied to get the manufacturer name
    try:
        manuList = soup.find("table", attrs={"id": "productDetails_techSpec_section_1"}).find_all('th')
        manu_value = ""
        #print(manuList)
        for manu in manuList:
            try:
                if 'Manufacturer' in manu.text:
                    #print("yes")
                    manu_value = manu.find_next_sibling().text
                    #print(manu_value)
                    break
            except AttributeError:
                manu_string = ""
                break
        manu_string = manu_value.strip()
    except AttributeError:
        manu_string = ""
    if manu_string == "":
        # Check for attribute error if the name is not found
        try:
            manuList = soup.find("div", attrs={"id": "detailBullets_feature_div"}).find_all("span", attrs={'class': 'a-text-bold'})
            #print(manuList)
            for manu in manuList:
                try:
                    if 'Manufacturer' in manu.text:
                        #print("yes 2")
                        manu_value = manu.find_next_sibling().text
                        manu_string = manu_value.strip()
                        #print(manu_value)
                        break
                except AttributeError:
                    manu_string = ""
                    break
        except AttributeError:
            manu_string = ""

    return manu_string

# Function to get the title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":"productTitle"})
        titla_value = title.string
        title_string = titla_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

if __name__ == '__main__':
    # Dictionary to store the product details.
    productData = {'URL':[],
                   'Name':[],
                   'Price':[],
                   'Rating':[],
                   'Reviews':[],
                   'ASIN':[],
                   'Manufacturer':[]}
    
    # Headers
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
                'Accept-Language': 'en-US, en;q=0.5'})
    # URL
    product_urls = []
    URL = "https://www.amazon.in/s?k=bags&crid=L7FLEA6QV28S&sprefix=bag%2Caps%2C232&ref=nb_sb_noss_1"

    # keep fetching products while there are more pages
    while(True):
        webpage = requests.get(URL, headers=HEADERS)
        time.sleep(5)
        soup = BeautifulSoup(webpage.text, "html.parser")     
        # Fetch all the product links on the current page      
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
       
        for link in links:
            try:
                prod_link =  requests.get("https://amazon.in" + link.get('href'), headers=HEADERS)
                time.sleep(5)
                prod_soup = BeautifulSoup(prod_link.content, "lxml")
                
                productData["Name"].append(get_title(prod_soup))
                #print(get_title(prod_soup))
                productData["URL"].append(URL)
                productData["Price"].append(getPrice(prod_soup))
                #print(getPrice(prod_soup))
                productData["Rating"].append(getRating(prod_soup))
                #print(getRating(prod_soup))
                productData["Reviews"].append(getReviews(prod_soup))
                #print(getReviews(prod_soup))
                #productData["Description"].append(getDescription(prod_soup))
                #print(getDescription(prod_soup))
                productData["Manufacturer"].append(getManufacturer(prod_soup))
                #print(getManufacturer(prod_soup))
                productData["ASIN"].append(getAsin(prod_soup))
                #print(getAsin(prod_soup))
            except requests.exceptions.ConnectionError:
                requests.status_code = "Connection refused"
                print("Connection refused")
        print("Page done...")
        # Fetch the next page, if it exists
        try:
            URL = getNextPage(soup)
        except AttributeError:
            URL = None
        if not URL:
            break
    print(productData)

    # Convert the dictionary to a data frame and export to CSV format
    df = pd.DataFrame(productData)
    df.to_csv("Amazon_Bags_List.csv", encoding="utf-8")

            
       
   