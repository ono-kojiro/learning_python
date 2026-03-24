from django.test import TestCase
from rest_framework.test import APIClient
from asset.models import Device
from asset.models import NIC

class NICAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.device = Device.objects.create(name="Server01", serial_number="ABC123")

    def test_create_nic(self):

        data = {
            "device": self.device.id,
            "name": "eth0",
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "ip_address": "192.168.1.10"
        }

        response = self.client.post("/api/nics/", data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(NIC.objects.count(), 1)
        self.assertEqual(NIC.objects.first().name, "eth0")

