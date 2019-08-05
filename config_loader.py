import os

class ConfigLoader():
    def __init__(self):
        config_file = open("config.txt", "r")
        conf = config_file.readlines()
        config_file.close()
        for line in conf:
            if line.startswith("#"):
                continue

            if line.startswith("nanopool_wallet_id: "):
                self.nanopool_wallet_id = line[20:-1]

            if line.startswith("nanopool_worker_name: "):
                self.nanopool_worker_name = line[22:-1]

            if line.startswith("destination_phone_number: "):
                self.destination_phone_number = line[26:-1]

            if line.startswith("destination_phone_provider: "):
                self.destination_phone_provider = line[28:-1]

            if line.startswith("response_time_in_minutes: "):
                self.response_time_in_minutes = line[26:-1]

            if line.startswith("gmail_address_login: "):
                self.gmail_address_login = line[21:-1]

            if line.startswith("gmail_address_pass: "):
                self.gmail_address_pass = line[20:-1]
