import requests


def get_bus(url):
    """Function to call the API and get data"""
    try:
        r = requests.get(url)
        # If the response was successful, no Exception will be raised
        r.raise_for_status()
        
        buses = r.json()
    return buses
