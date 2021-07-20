import sqlite3
import pandas as pd
from datetime import datetime as dt
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

default_args = {'owner': 'airflow'}

path = "/Users/victorcunha/Codes/pff2_dl_airflow/"
path_db = path+"pff_mask.db"
path_temp_csv = path+"_temp.csv"


dag = DAG(
    dag_id='pff_etl',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(1),
)

path = "/Users/victorcunha/Codes/pff2_dl_airflow/"
path_db = path+"pff_mask.db"
path_temp_csv = path+"_temp.csv"

def find_aura_3m(browser, BASE_URL):
    browser.get(BASE_URL)
    try:
        name_div = browser.find_element_by_css_selector('div.name-product')
        name = name_div.text
    except NoSuchElementException:
        name = None
    try:
        link = name_div.find_element_by_css_selector('a')
        link = link.get_attribute('href')
    except Exception as e:
        link = None
    try:
        price_span = browser.find_element_by_css_selector('span.best-price')
        price = (price_span.text)
        status = 'produto disponível'
    except NoSuchElementException:
        no_price_span = browser.find_element_by_css_selector('.bt-product-unavailable')
        price = 0
        status = no_price_span.text.lower()
    return name, link, price, status

def _extract():
    opt = Options()
    opt.headless = True
    date = dt.now().strftime('%Y-%m-%d')
    BASE_URL = 'https://www.loja3m.com.br/busca?ft=aura%209320'

    browser = Firefox(options=opt)
    name, link, price, status = find_aura_3m(browser, BASE_URL)
    browser.quit()


    with open(path_temp_csv, 'w') as f:
        f.write(f'date,name,price,status,link\n')
        f.write(f'{date},{name},{price},{status},{link}\n')

def _transform():
    dataset_df = pd.read_csv(path_temp_csv)

    dataset_df.status.replace({'produto disponível':1, 'produto indisponível':0}, inplace=True)

    dataset_df.to_csv(
        path_temp_csv,
        index=False
    )

def _load():
    #conectando com o banco de dados Data Wharehouse.
    connect_db = sqlite3.connect(path_db)
    
    #lendo os dados a partir dos arquivos csv.
    dataset_df = pd.read_csv(path_temp_csv)

    #carregando os dados no banco de dados.
    dataset_df.to_sql("pff_masks", connect_db, if_exists="append", index=False)


extract_task = PythonOperator(
    task_id="extract", python_callable=_extract, dag=dag
)

transform_task = PythonOperator(
    task_id="transform", python_callable=_transform, dag=dag
)

load_task = PythonOperator(
    task_id="load", python_callable=_load, dag=dag
)

extract_task >> transform_task >> load_task
