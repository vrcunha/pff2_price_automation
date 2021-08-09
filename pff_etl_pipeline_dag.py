import os
import os.path
import telegram
from dotenv import load_dotenv
import sqlite3
import pandas as pd
from datetime import datetime as dt
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

default_args = {'owner': 'Victor'}

path = "/Users/victorcunha/Codes/pff2_dl_airflow/"
path_db = path+"pff_mask.db"
path_env = path+'.env'
path_temp_csv = path+"_temp.csv"

load_dotenv(path_env)

dag = DAG(
    dag_id='etl_pff2_telegram',
    default_args=default_args,
    schedule_interval='*/10 * * * *',
    start_date=dt(2021, 8, 2),
    tags=['ETL_BOT'],
)

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
        price = price_span.text
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
        f.write(f'date;name;price;status;link\n')
        f.write(f'{date};{name};{price};{status};{link}\n')

def _transform():
    dataset_df = pd.read_csv(path_temp_csv, sep=';')
    
    try:
        if 'R$' in dataset_df.iloc[0,2]:
                dataset_df.iloc[0,2] = dataset_df.iloc[0,2].replace('R$', '').strip()
        if ',' and '.' in dataset_df.iloc[0,2]:
            dataset_df.iloc[0,2] = dataset_df.iloc[0,2].replace('.', '').replace(',', '.')
        dataset_df.price = pd.to_numeric(dataset_df.price, downcast="float").map('{:,.2f}'.format)
    except TypeError:
        dataset_df.price = pd.to_numeric(dataset_df.price, downcast="float").map('{:,.2f}'.format)

    dataset_df.status.replace({'produto disponível':1, 'produto indisponível':0}, inplace=True)

    dataset_df.to_csv(
        path_temp_csv,
        index=False
    )

def _load():
    connect_db = sqlite3.connect(path_db)
    
    dataset_df = pd.read_csv(path_temp_csv)

    dataset_df.to_sql("pff_masks", connect_db, if_exists="append", index=False)

def telegram_msg(chat, token):
    df = pd.read_csv(path_temp_csv)
    if df.status.values != [0]:
        msg = f'O produto {df.iloc[0,1]} -> Disponível\n{df.iloc[0,4]}'
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat, text=msg)

extract_task = PythonOperator(
    task_id="extract", python_callable=_extract, dag=dag
)

transform_task = PythonOperator(
    task_id="transform", python_callable=_transform, dag=dag
)

load_task = PythonOperator(
    task_id="load", python_callable=_load, dag=dag
)

telegram_task = PythonOperator(
    task_id="telegram",
    op_args=[
        os.getenv('TELEGRAM_GROUP_ID'), 
        os.getenv('TELEGRAM_TOKEN')
    ],
    python_callable=telegram_msg,
    dag=dag
)

extract_task >> transform_task >> load_task >> telegram_task
