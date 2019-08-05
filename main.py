from crypto_puller import NanopoolPuller, CryptowatPuller
from config_loader import ConfigLoader
import sms
import time
import datetime
from threading import Thread

config = ConfigLoader()
nanopool_puller = NanopoolPuller(config.nanopool_wallet_id, config.nanopool_worker_name)
cryptowat_puller = CryptowatPuller()

ethereum_critical_price_notified = False

def update_data():
    print("Gathered Nanopool Data . . .")
    nanopool_puller.update_data()
    print("Gathered Cryptowat Data . . .")
    cryptowat_puller.update_data()

def send_sms_response():
    print("[*] Preparing to send SMS response [*]")
    sms.send_sms(config.destination_phone_number, config.destination_phone_provider, config.gmail_address_login, config.gmail_address_pass, nanopool_puller.get_account_data_as_string())
    print("[+] Account Data Sent Successfully [+]")

    sms.send_sms(config.destination_phone_number, config.destination_phone_provider, config.gmail_address_login, config.gmail_address_pass, cryptowat_puller.get_market_price_data_as_string(cryptowat_puller.bitcoin_market_price_data, "Bitcoin"))
    print("[+] Bitcoin Market Data Sent Successfully [+]")

    sms.send_sms(config.destination_phone_number, config.destination_phone_provider, config.gmail_address_login, config.gmail_address_pass, cryptowat_puller.get_market_price_data_as_string(cryptowat_puller.ethereum_market_price_data, "Ethereum"))
    print("[+] Ethereum Market Data Sent Successfully [+]\n\n")

def data_updating_loop():
    while True:
        time.sleep(8)
        update_data()

def ethereum_price_check():
    global ethereum_critical_price_notified
    while True:
        time.sleep(8)
        last_price = float(cryptowat_puller.ethereum_market_price_data['last'])
        if last_price < 100 and (not ethereum_critical_price_notified):
            sms.send_sms(config.destination_phone_number, config.destination_phone_provider, config.gmail_address_login, config.gmail_address_pass, "WARNING! Ethereum price dropped below $100!\nEthereum Price: $" + str(last_price) + "\n")
            ethereum_critical_price_notified = True
        elif last_price >= 100:
            ethereum_critical_price_notified = False

def main_loop():
    print("============ CryptoPuller Started ============\n")
    
    update_data()
    print("")
    
    data_updating_thread = Thread(target = data_updating_loop)
    data_updating_thread.daemon = True
    data_updating_thread.start()

    ethereum_price_checking_thread = Thread(target = ethereum_price_check)
    ethereum_price_checking_thread.daemon = True
    ethereum_price_checking_thread.start()

    while True:
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        send_sms_response()
        time.sleep(float(config.response_time_in_minutes) * 60)

if __name__ == '__main__':
    main_loop()