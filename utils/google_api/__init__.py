import os


def get_google_api_key():
    '''get google api key from env, or from local file'''
    try:
        # if unix, read the api key from the os environment
        if os.name == 'posix' and 'GOOGLE_API_KEY' in os.environ:
            api_key = os.environ['GOOGLE_API_KEY']
        # if windows, read the api key from the file
        else:
            with open("/etc/google_api_key.txt", "r") as f:
                api_key = f.read()
    except (FileNotFoundError, KeyError):
        raise Exception("No api key found in file")
    return api_key


from googletrans import Translator
from utils.google_api.google_maps import GoogleMapsAPI


translator = Translator()
google_maps_api = GoogleMapsAPI()
