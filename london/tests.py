from django.test import TestCase
import datetime
from django.urls import reverse
from .models import Buses

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
        self.url = reverse('tfl')

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
