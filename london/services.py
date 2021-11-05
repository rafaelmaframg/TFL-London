import requests
from requests.exceptions import HTTPError


def get_bus(url):
    """Function to call the API and get data"""
    try:
        r = requests.get(url)
        # If the response was successful, no Exception will be raised
        r.raise_for_status()
    except HTTPError as err:#<class 'requests.exceptions.HTTPError'>
        return err
    except Exception as excp:#<class 'UnboundLocalError'>
        return excp
    else:
        return r.json()
