import requests
from lxml import html

script = '''
        headers = {
            ["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        splash:set_custom_headers(headers)
        splash.private_mode_enabled = false
        splash.images_enabled = false
        assert(splash:go(args.url))
        splash:wait(1)

        return {
            html = splash:html()
        }
'''
'''
Point to be noted while sending a request to the site:
1. We always have to use POST method
2. Set the url to the server location started by the splash container
3. and add run in the url to make requests communicate with splash
'''
response = requests.post(url="http://localhost:8050/run", json={
    "lua_source":script,
    "url":"https://www.gearbest.com/flash-sale.html"
})

# print(response.content)

## Now we can use lxml to parse
tree = html.fromstring(response.content)
products = tree.xpath("//div[contains(@class,'content')]")

'''
NOTE: The name string comes with \\n. This is not classfied as whitespace. so 
calling strip() wont work. We need to replace them by "". Then call strip()

'''

all_products = []
for product in products:
    
    item = {
        "name":product.xpath(".//div[contains(@class,'title')]/a/text()")[0].replace("\\n","").strip(),
        "url": product.xpath(".//div[contains(@class,'title')]/a/@href")[0],
        "new_price":product.xpath(".//div[contains(@class,'detail')]/span[1]/text()")[0],
        "mrp": product.xpath(".//div[contains(@class,'delete')]/del/del/text()")[0]
    }
    
    all_products.append(item)
                                  
