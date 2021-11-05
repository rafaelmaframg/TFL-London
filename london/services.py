import requests

def get_bus(url):
    """Function to call the API and get data"""
    r = requests.get(url)
    if r.status_code != 200:
        return "An error occured. Please try again later!"
    buses = r.json()
    return buses
