import requests 
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3

#organizar código
def fetch_page():
    url = "https://www.mercadolivre.com.br/apple-iphone-16-plus-512-gb-branco-distribuidor-autorizado/p/MLB1040287820#polycard_client=search-nordic&searchVariation=MLB1040287820&wid=MLB3858683633&position=10&search_layout=stack&type=product&tracking_id=aadf8510-74ec-4306-a961-782d45fafa36&sid=search" 
    response = requests.get(url)
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html,'html.parser')
    product_name = soup.find('h1', class_= 'ui-pdp-title').get_text()
    #parseando os tipos de valores
    prices: list = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price:int =(prices[0].get_text()).replace('.', '')
    new_price:int =(prices[1].get_text()).replace('.', '')
    installment_price:int =(prices[2].get_text()).replace('.', '')
    #.replace('.', '') remove o ponto digito milhar

    #variável para saber o momento da coleta e envio para o banco
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
        'timestamp': timestamp
    }


def create_connection(db_name= 'iphone_prices.db'):
    """Cria uma conexão com o banco de dados PostgreSQL."""
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TIMESTAMP
        )
    ''')
    conn.commit()


def save_to_database(conn, product_info):
    new_row = pd.DataFrame([product_info])
    new_row.to_sql('prices', conn, if_exists='append', index = False)

if __name__ == "__main__":  

    conn = create_connection()
    setup_database(conn)

    df=pd.DataFrame()

    while True:
        page_content = fetch_page()
        produto_info=parse_page(page_content)
        save_to_database(conn, produto_info)
        print("Dados salvos no banco de dados", produto_info)
        time.sleep(20)