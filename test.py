import requests
import pandas as pd
import sys

products = []


def get_source_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,be-BY;q=0.8,be;q=0.7,en-GB;q=0.6,en;q=0.5,ru-BY;q=0.4,en-US;q=0.3,pl;q=0.2',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': 'https://www.wildberries.by/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross_site',
        'User-Agent': 'Your User_Agent',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115""',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }

    response = requests.get(url, headers=headers)

    return response.json()


def prepare_items(response):
    products_raw = response.get('data', {}).get('products', None)

    if products_raw is not None and len(products_raw) > 0:
        for product in products_raw:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': product.get('priceU', None) / 100 if product.get('priceU', None) is not None else None,
                'salePriceU': product.get('salePriceU', None) / 100 if product.get('salePriceU',
                                                                                   None) is not None else None,
            })

    else:
        sys.exit()

    return products


def main():
    pr = []
    for i in range(1, 5):
        print('page:', i, '...')
        response = get_source_html(
            url=f'https://search.wb.ru/exactmatch/sng/common/v4/search?query=%D0%B1%D1%83%D1%82%D1%81%D1%8B%20%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5&resultset=catalog&limit=100&sort=popular&page={i}&appType=128&curr=byn&lang=ru&dest=-59208&regions=1,4,22,30,31,33,40,48,66,68,69,70,80,83,114&spp=0 ')
        pr = prepare_items(response)
        print('         page:', i, ' - completed')

    pd.DataFrame(pr).to_excel('productsW.xlsx', index=False)

    # test-1 - запись каждой страницы сайта на отдельный лист
    # df = pd.DataFrame(products)
    # with pd.ExcelWriter('productsW.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
    #     df.to_excel(writer, sheet_name="Sheet1")

    # test-3
    # pd.DataFrame(products).to_csv('products.csv', index=False)
    #
    # df = pd.DataFrame(products)
    # append_df_to_excel('productsW.xlsx', df, index=False, headr=None)
    # time.sleep(1)


if __name__ == "__main__":
    main()
