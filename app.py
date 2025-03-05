import requests 

#organizar código
def fetch_page(url):
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "https://www.mercadolivre.com.br/apple-iphone-16-plus-512-gb-branco-distribuidor-autorizado/p/MLB1040287820#polycard_client=search-nordic&searchVariation=MLB1040287820&wid=MLB3858683633&position=10&search_layout=stack&type=product&tracking_id=aadf8510-74ec-4306-a961-782d45fafa36&sid=search"   
    page_content = fetch_page()
    print(page_content)