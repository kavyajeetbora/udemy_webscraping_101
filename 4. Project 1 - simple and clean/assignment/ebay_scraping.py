import requests
from lxml import html
import json

if __name__ == "__main__":
    ## reqeusting html content of the website from ebay.com
    response = requests.get(url="https://www.ebay.com/globaldeals/trending/all",
                headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"})

    # parsing the html text into lxml tree object
    tree = html.fromstring(response.text)


    ## scraping the data of products from website
    products = tree.xpath("//div[@class='dne-itemtile-detail']")
    all_products = []

    for product in products:

        ## Extract the name, price and url of each product:
        product_name = product.xpath(".//span/text()")[0]
        product_url = product.xpath(".//a/@href")[0]
        price = product.xpath(".//span/text()")[1]

        ## now store the data of each product into a dictionary:
        json_data = {"product_name":product_name,
                    "url":product_url,
                    "price":price}

        all_products.append(json_data)

    ## Saving the data into json file
    with open("global_products.json", "w") as f:
        f.write(json.dumps(all_products))
