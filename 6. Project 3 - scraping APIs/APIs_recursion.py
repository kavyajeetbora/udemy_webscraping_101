import requests
import json
from fake_useragent import UserAgent
import pprint
from urllib.parse import urljoin
import sqlite3

def generate_payload(pageNo=1):

    '''
    This function returns payload of a particular page number
    '''
    payload = json.dumps({
      "p": pageNo,
      "s": 72,
      "view": "allView",
      "geoTargetEnabled": False,
      "abtest": [
        "tier2",
        "showNewCategories"
      ],
      "deviceType": "desktop",
      "id": [
        "350006"
      ],
      "requestType": "tier3",
      "sort": "Top Sellers",
      "couponStoreId": "15196",
      "storeId": "15196"
    })
    return payload

def extract_all_data():

    '''
    This function returns the data in json format of a particular page number
    of https://www.walgreens.com/productsearch/v3/products/search
    '''
    ua = UserAgent()
    url = "https://www.walgreens.com/productsearch/v3/products/search"

    headers = {
      'content-type': 'application/json',
      'User-Agent': ua.random
    }

    extracted_products = [] ## store the json data in this list

    n = 1
    response = requests.post(url=url, headers=headers, data=generate_payload(n))
    products_is_there = "products" in response.json()
    while products_is_there:
        print("pageNumber:",n)
        ## extract all the all the data
        data = response.json()
        products = data['products']
        for product_info in products:
            product_info = product_info["productInfo"]
            pr = {
                "id" : product_info["prodId"],
                "name" : product_info["productDisplayName"],
                "price" : product_info["priceInfo"]["regularPrice"],
                "size" : product_info["productSize"],
                "product_url" : urljoin(url,product_info["productURL"]),
                "img_url" : urljoin(url,product_info["imageUrl"]),
                "rating" : product_info['averageRating']
            }
            extracted_products.append(pr)
        ## then change the page number and request:
        n = n+1
        ## now send request to the new page and get the response:
        response = requests.post(url=url, headers=headers, data=generate_payload(n))
        products_is_there = "products" in response.json()

    return extracted_products


if __name__ == "__main__":
    data = extract_all_data()
    print("total products extracted:",len(data))
    pprint.pprint(data)
    try:
        ## create a sql connection
        connection = sqlite3.connect("wallgreens.db")
        ## create a cursor using which we will execute our queries
        cursor = connection.cursor()
        
        cursor.execute('''
                       CREATE TABLE products (
                           id TEXT PRIMARY KEY,
                           name TEXT,
                           price TEXT,
                           size TEXT,
                           product_url TEXT,
                           img_url TEXT,
                           rating TEXT
                           )
                       
                       ''')
       
        connection.commit()
    except sqlite3.OperationalError as e:
        print(e)
        
        
    ## Now lets insert the data into the database
    try:
        for product in data:
            cursor.execute('''
                           INSERT INTO products (id, name,price,size,product_url,img_url,rating)
                           VALUES (?,?,?,?,?,?,?)
                           ''', (
                                   product["id"],
                                   product["name"],
                                   product["price"],
                                   product["size"],
                                   product["product_url"],
                                   product["img_url"],
                                   product["rating"],
                                )
                           )
        
        connection.commit()
    except sqlite3.IntegrityError:
        pass
    
    
    connection.close()
   
    
    
