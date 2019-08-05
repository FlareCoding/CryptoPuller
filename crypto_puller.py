import os.path
from urllib.request import Request, urlopen
import json

headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' }

def get_json_data_from_url(addr):
    req = Request(addr, None, headers)
    html_data = urlopen(req).read()
    json_obj = json.loads(html_data.decode('utf-8'))
    return json_obj


class NanopoolPuller:
    def __init__(self, wallet_address, worker_name):
        self.__wallet_address = wallet_address
        self.__worker_name = worker_name
        self.__headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' }
        self.__nanopool_calculated_hashrate_address = 'https://eth.nanopool.org/api/v1/hashrate/{}/{}'.format(wallet_address, worker_name)
        self.__nanopool_last_reported_hashrate_address = 'https://api.nanopool.org/v1/eth/reportedhashrate/{}'.format(wallet_address)
        self.__nanpool_eth_balance_address = 'https://api.nanopool.org/v1/eth/balance/{}'.format(wallet_address)
        self.__ether_balance = 0
        self.__calculated_hashrate = 0
        self.__last_reported_hashrate = 0
        self.__connection_status = False

    def get_eth_balance(self) -> float:
        return self.__ether_balance

    def get_calculated_hashrate(self) -> float:
        return self.__calculated_hashrate

    def get_last_reported_hashrate(self) -> float:
        return self.__last_reported_hashrate

    def update_data(self):
        # getting eth balance
        json_obj = get_json_data_from_url(self.__nanpool_eth_balance_address)
        if json_obj['status'] == True:
            self.__ether_balance = json_obj['data']
            self.__connection_status = True
        else:
            self.__connection_status = False
            self.__ether_balance = -1

        # getting calculated hashrate
        json_obj = get_json_data_from_url(self.__nanopool_calculated_hashrate_address)
        if json_obj['status'] == True:
            self.__calculated_hashrate = json_obj['data']
        else:
            self.__calculated_hashrate = -1

        # getting last reported hashrate
        json_obj = get_json_data_from_url(self.__nanopool_last_reported_hashrate_address)
        if json_obj['status'] == True:
            self.__last_reported_hashrate = json_obj['data']
        else:
            self.__last_reported_hashrate = -1

    def print_account_data(self):
        print("\n============ Wallet ID: {} ============".format(self.__wallet_address))
        print("Connection Status: {}".format(self.__connection_status))
        print("Worker Name: {}".format(self.__worker_name))
        print("Calculated Hashrate: {}MH/s".format(self.__calculated_hashrate))
        print("Last Reported Hashrate: {}MH/s".format(self.__last_reported_hashrate))
        print("Current Balance: {} eth.".format(self.__ether_balance))

    def get_account_data_as_string(self) -> str:
        output = 'Wallet ID: {}\n\n'.format(self.__wallet_address)
        output += "Connection Status: {}\n".format(str(self.__connection_status))
        output += "Worker name: {}\n".format(self.__worker_name)
        output += "Calculated Hashrate: {}MH/s\n".format(str(self.__calculated_hashrate))
        output += "Last Reported Hashrate: {}MH/s\n".format(str(self.__last_reported_hashrate))
        output += "Current Balance: {} eth.\n\n".format(str(self.__ether_balance))
        return output


class CryptowatPuller:
    def __init__(self):
        self.__bitcoin_market_summary_address = 'https://api.cryptowat.ch/markets/coinbase-pro/btcusd/summary'
        self.bitcoin_market_price_data = None

        self.__ethereum_market_summary_address = 'https://api.cryptowat.ch/markets/coinbase-pro/ethusd/summary'
        self.ethereum_market_price_data = None

    def update_data(self):
        # getting market summary
        json_obj = get_json_data_from_url(self.__bitcoin_market_summary_address)
        self.bitcoin_market_price_data = json_obj['result']['price']

        json_obj = get_json_data_from_url(self.__ethereum_market_summary_address)
        self.ethereum_market_price_data = json_obj['result']['price']

    def print_market_price_data(self, market_price_data, tagline_currency_name):
        info = market_price_data
        print("------ " + tagline_currency_name + " Price Info ------")
        print("Last: {}".format(info['last']))
        print("High: {}".format(info['high']))
        print("Low:  {}".format(info['low']))
        print("Percentage Change: {}".format(info['change']['percentage']))
        print("Absolute   Change: {}\n".format(info['change']['absolute']))

    def get_market_price_data_as_string(self, market_price_data, tagline_currency_name) -> str:
        info = market_price_data
        output = "------" + tagline_currency_name + " Price Info ------\n\n"
        output += "Last: {}\n".format(str(info['last']))
        output += "High: {}\n".format(str(info['high']))
        output += "Low: {}\n".format(str(info['low']))
        output += "Percentage Change: {}\n".format(str(info['change']['percentage']))
        output += "Absolute   Change: {}\n\n".format(str(info['change']['absolute']))
        return output
