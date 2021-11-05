from django.test import TestCase
import datetime
from requests.exceptions import HTTPError
from django.urls import reverse
from .models import Buses
from london.services import get_bus


class BusesModelTests(TestCase):
    def setUp(self):
        Buses.objects.create(line_name = 'Test-K1', destination_name = 'Test-Kingston',
                             vehicle_id = 'TesT123', expected_arrival = datetime.datetime.now(),
                             time_now=datetime.datetime.now())

        Buses.objects.create(line_name = 'Test-K2', destination_name = 'Test-Kingston2',
                             vehicle_id = 'TesT1234', expected_arrival = datetime.datetime.now(),
                             time_now=datetime.datetime.now())

    def test_buses_id(self):
        """Get Values Vehicle_Id From Objects"""
        bus1 = Buses.objects.get(line_name = 'Test-K1')
        bus2 = Buses.objects.get(line_name = 'Test-K2')
        self.assertEqual(bus1.vehicle_id, 'TesT123')
        self.assertEqual(bus2.vehicle_id, 'TesT1234')

    def test_buses_expected_arrival(self):
        """Get Values Destination_name From Objects"""
        bus1 = Buses.objects.get(line_name='Test-K1')
        bus2 = Buses.objects.get(line_name='Test-K2')
        self.assertEqual(bus1.destination_name, 'Test-Kingston')
        self.assertEqual(bus2.destination_name, 'Test-Kingston2')


class IndexViewTest(TestCase):
    """get test about response index"""
    def setUp(self):
        self.url = reverse('index')

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')


class TFLViewTest(TestCase):
    """get test about response API"""
    def setUp(self):
        self.url = reverse('api')

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TFLViewTest(TestCase):
    """get test about response Results"""
    def setUp(self):
        self.url = reverse('results')

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class Get_API_return(TestCase):
    """Get test about API return"""
    def setUp(self):
        self.r = get_bus('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals')
        self.r_error = get_bus('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals/222')

    def test_return_list(self):
        self.assertEqual(type(self.r), list)

    def test_return_error(self):
        self.assertEqual(type(self.r_error), HTTPError)
