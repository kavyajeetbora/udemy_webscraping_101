import requests
import json
from fake_useragent import UserAgent
import pprint
from urllib.parse import urljoin

if __name__ == "__main__":

    ua = UserAgent()

    url = "https://www.walgreens.com/productsearch/v3/products/search"

    payload = json.dumps({
      "p": 3,
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

    headers = {
      'content-type': 'application/json',
      'User-Agent': ua.random
    }

    response = requests.post(url=url, headers=headers, data=payload)
    data = response.json()
    products = data['products']

    extracted_products = []

    for product_info in products:

        pr = {
            "id" : product_info["productInfo"]["prodId"],
            "name" : product_info["productInfo"]["productDisplayName"],
            "price" : product_info["productInfo"]["priceInfo"]["regularPrice"],
            "size" : product_info["productInfo"]["productSize"],
            "product_url" : urljoin(url,product_info["productInfo"]["productURL"]),
            "img_url" : urljoin(url,product_info["productInfo"]["imageUrl"]),
            "rating" : product_info["productInfo"]['averageRating']
        }
        extracted_products.append(pr)


    pprint.pprint(extracted_products)
