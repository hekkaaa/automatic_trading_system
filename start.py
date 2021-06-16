import requests
import time
import os.path
from DataFormatCorrection.UpdateData import *

cryptomoney = 'BTC_ETH'
name_table = f'tradehistory_{cryptomoney}_{realdatatame()}'

def returnTradeHistory():

    while True:
        #header
        cryptomoney = 'BTC_ETH'
        params = (
            ('command', 'returnTradeHistory'),
            ('currencyPair', cryptomoney),
        )
        ############

        name_table = f'tradehistory_{cryptomoney}_{realdatatame()}'
        # name_table = 'tradehistory_btc_eth_14_06_2021'
        name_table = name_table.lower()
        logdatanamemarket = f'tradehstory{realdatatame()}.txt'
        logdatanametech = f'techlog{realdatatame()}.txt'

        #Проверка существования таблицы за текущую дату.
        check_table_db = chectablefromDB(name_table)

        if check_table_db:
            print('file here!')
            # дополнение лога в бесконечном цикле.

            #Проверка даты последней записи
            lastdatetimetrade = update_str_for_datatime(check_last_date_edit_table(name_table))

            while True:
                # Блок обновления дат
                name_table = f'tradehistory_{cryptomoney}_{realdatatame()}'
                # name_table = 'tradehistory_btc_eth_16_06_2021'
                name_table = name_table.lower()
                logdatanametech = f'techlog{realdatatame()}.txt'
                print('Последняя дата')
                print(lastdatetimetrade)
                lastdatetimetrade = cycleupdatelogmarket_sql(lastdatetimetrade, params,logdatanametech,name_table)
                time.sleep(2)

        else:
            # marketlog = open(logdatanamemarket, 'w')
            # marketlog.close()

            response = requests.get('https://poloniex.com/public', params=params)
            if (response.status_code):
                #Создание новой таблицы
                create_table_sql(name_table)
                #Первичное наполнение таблицы
                lastdatetimetrade = firststartreturnhistoryTrade_sql(response,logdatanametech, name_table)

                # дополнение лога в бесконечном цикле.
                i = 0
                while True:
                    time.sleep(2)
                    lastdatetimetrade = cycleupdatelogmarket_sql(lastdatetimetrade, params,logdatanametech,name_table)

                print('SCRIPT DONE')
            else:
                print("Error server response: " + response.status_code)
                print('_' * 60)
                requestJSON = ''.join(map(str, response.json()))  # пребразование list в str для нормального чтения в лог.
                outserverlocallog = "GET \nServer status NOT\nJSON: " + requestJSON + '\n' + '_' * 60

                # запись в технический лог
                techlog = open(logdatanametech, 'w')
                techlog.write(outserverlocallog)
                techlog.close()


def test_sql_json():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="111111",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()
        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f"""SELECT * FROM {name_table}"""

        cursor.execute(insert_query)
        f = cursor.fetchall()
        return f

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()





