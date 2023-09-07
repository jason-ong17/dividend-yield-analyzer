import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = r"C:\Users\jason\OneDrive\Documents\PycharmProjects\chromedriver-win64\chromedriver.exe"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)


# Scrape tickers from tradingview.com's high dividend page into a list
def get_tickers():
    driver.get('https://www.tradingview.com/markets/stocks-usa/market-movers-high-dividend/')
    ticker_list = []
    for i in range(1, 101):
        symbol = driver.find_element(By.XPATH, f'/html/body/div[3]/div[4]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/td[1]/span/a').text
        ticker_list.append(symbol)
    return ticker_list


# Formats all numbers and percentages into floats
def clean_data(data):
    if data == 'n/a':
        return data
    else:
        try:
            if '$' in data:
                data = data.replace('$', '')
            if '%' in data:
                data = data.replace('%', '')
            if ',' in data:
                data = data.replace(',', '')
        except TypeError:
            pass
        return float(data)


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker
        self.current_price = 0
        self.dividend_yield = 0
        self.annual_dividend = 0
        self.payout_frequency = ""
        self.dividend_growth = 0
        self.avg_eps = 0

    # Take a ticker string as input and updates the ticker's dividend info
    def get_div_info(self, ticker):
        try:
            driver.get(f'https://stockanalysis.com/stocks/{ticker}/dividend/')
            current_price = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div[1]').text
            dividend_yield = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[2]/div[1]/div').text
            annual_dividend = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[2]/div[2]/div').text
            payout_frequency = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[2]/div[4]/div').text
            dividend_growth = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[2]/div[6]/div').text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                current_price = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div[1]').text
                dividend_yield = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[1]/div[1]/div').text
                annual_dividend = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[1]/div[2]/div').text
                payout_frequency = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[1]/div[4]/div').text
                dividend_growth = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div/div[1]/div[6]/div').text
            except selenium.common.exceptions.NoSuchElementException:
                current_price, dividend_yield, annual_dividend, payout_frequency, dividend_growth = 0, 0, 0, "n/a", 0
        self.current_price = clean_data(current_price)
        self.dividend_yield = clean_data(dividend_yield)
        self.annual_dividend = clean_data(annual_dividend)
        self.payout_frequency = payout_frequency
        self.dividend_growth = clean_data(dividend_growth)

    # # Take a ticker string and a number of years to lookback as input and updates the ticker's diluted eps info
    # def get_eps_info(self, ticker, eps_lookback):
    #     # # Using seekingalpha.com
    #     # try:
    #     #     driver.get(f'https://seekingalpha.com/symbol/{ticker}/income-statement')
    #     #     eps_list = []
    #     #     if driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/div/main/div[2]/div/div[3]/div/div/section/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[32]/th').text\
    #     #             == 'Diluted EPS':
    #     #         for i in range(7, eps_lookback+7):
    #     #             eps = clean_data(driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/div/main/div[2]/div/div[3]/div/div/section/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[32]/td[{i}]').text)
    #     #             print(eps)
    #     #             eps_list.append(eps)
    #     #         self.avg_eps = mean(eps_list)
    #     #     else:
    #     #         print(f'Different XPATH for {ticker}')
    #     # except selenium.common.exceptions.NoSuchElementException:
    #     #     self.error = True
    #     #     print(f'Error getting eps info for {ticker}')
    #
    #     # # Using stockanalysis.com
    #     # try:
    #     #     driver.get(f'https://stockanalysis.com/stocks/{ticker}/financials/')
    #     #     eps_list = []
    #     #     if driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[17]/td[1]/span').text\
    #     #             == 'EPS (Diluted)':
    #     #         for i in range(2, eps_lookback+2):
    #     #             eps = float(driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[17]/td[{i}]').text)
    #     #             eps_list.append(eps)
    #     #     elif driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[18]/td[1]/span').text\
    #     #             == 'EPS (Diluted)':
    #     #         for i in range(2, eps_lookback+2):
    #     #             eps = float(driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[18]/td[{i}]').text)
    #     #             eps_list.append(eps)
    #     #     elif driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[19]/td[1]/span').text\
    #     #             == 'EPS (Diluted)':
    #     #         for i in range(2, eps_lookback+2):
    #     #             eps = float(driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[19]/td[{i}]').text)
    #     #             eps_list.append(eps)
    #     #     elif driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[20]/td[1]/span').text\
    #     #             == 'EPS (Diluted)':
    #     #         for i in range(2, eps_lookback+2):
    #     #             eps = float(driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[20]/td[{i}]').text)
    #     #             eps_list.append(eps)
    #     #     elif driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[21]/td[1]/span').text\
    #     #             == 'EPS (Diluted)':
    #     #         for i in range(2, eps_lookback+2):
    #     #             eps = float(driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[5]/table/tbody/tr[21]/td[{i}]').text)
    #     #             eps_list.append(eps)
    #     #     else:
    #     #         eps_list = [0]
    #     #         self.error = True
    #     #         print(f'EPS is on a different row for {ticker}')
    #     #     self.avg_eps = mean(eps_list)
    #     # except selenium.common.exceptions.NoSuchElementException:
    #     #     self.error = True
    #     # except IndexError:
    #     #     self.error = True
    #     # except ValueError:
    #     #     self.error = True
