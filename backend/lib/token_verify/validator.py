from urllib import urlopen


def load_keys():
    json_url = urlopen(
        'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')
