from my_scripts.selenium_controler import Controler
import datetime
import pandas as pd
import os

class YahooScrapper:
    def __init__(self, downloads_folder:str='/Users/mariano/Downloads') -> None:
        self.controlador = Controler()
        self.downloads_folder = downloads_folder # Para saber dónde se va a descargar el archivo y poderlo mover
  
    def __get_historical_url(self, stock:str, fecha_inicio:datetime.datetime, fecha_fin:datetime.datetime):
        int_inicio = int(fecha_inicio.timestamp())
        int_fin = int(fecha_fin.timestamp())
        return f'https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={int_inicio}&period2={int_fin}&interval=1d&events=history'
    
    def __get_bet_url(self, stock:str):
        return  f'https://finance.yahoo.com/quote/{stock}'
    
    def __open_data(self, stock:str) -> pd.DataFrame:
        '''
        Esta función lee los datos descargados y elimina el csv de las descargas.
        '''
        # TODO: Verificar que el archivo sí esté en las descargas
        # TODO: Verificar que no haya más versiones del archivo. Eg. DIS (1).csv y DIS.csv, habría que descargar la última versión
        # Ahorita voy a suponer que solo está el bueno (DIS.csv)
        # Hay que esperar a que el archivo se haya descargado
        filename = f'{self.downloads_folder}/{stock}.csv'

        file_exists = False
        i = 1
        while not file_exists:
            file_exists = f'{stock}.csv' in os.listdir(self.downloads_folder)
            i += 1
            if i > 1000:
                print(f'No data was found for {stock}')
                return pd.DataFrame()
        
        downloaded_data = pd.read_csv(filename)
        # Eliminamos los datos
        os.remove(filename)
        return downloaded_data

    def get_historical_data_datetime(self, stock:str, fecha_inicio:datetime.datetime, fecha_fin:datetime.datetime) -> pd.DataFrame:
        '''
        Esta función recibe una fecha de inicio y una de final, así como el stock que se desea buscar y
        genera un csv con los datos descargados, lo guarda en downloads folder, lo lee y regresa un dataframe.
        Elimina el csv.
        '''
        # Generamos el url de descarga
        url = self.__get_historical_url(stock=stock, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        # Esto va a descargar los datos
        self.controlador.open_url(url)
        # Leemos los datos
        return self.__open_data(stock=stock)
    
    def get_historical_data(self, stock:str, fecha_inicio:str, fecha_fin:str, dayfirst:bool=True) -> pd.DataFrame:
        '''
        Esta función funciona igual, pero con fechas en formato string
        '''
        datetime_inicio = pd.to_datetime(fecha_inicio, dayfirst=dayfirst)
        datetime_fin = pd.to_datetime(fecha_fin, dayfirst=dayfirst)

        return self.get_historical_data_datetime(stock=stock, fecha_inicio=datetime_inicio, fecha_fin=datetime_fin)
    
    def get_beta(self, stock:str):
        '''
        Esta función regresa la beta de un stock
        '''
        url = self.__get_bet_url(stock=stock)
        self.controlador.open_url(url)
        return self.controlador.get_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]').text
        

if __name__ == '__main__':
    print('scrappers.py is running as main')
