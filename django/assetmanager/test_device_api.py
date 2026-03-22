from django.test import TestCase
from rest_framework.test import APIClient
from asset.models import Device

class DeviceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_device(self):
        data = {
            "name": "Server01",
            "serial_number": "ABC123"
        }

        response = self.client.post("/api/devices/", data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(Device.objects.first().name, "Server01")

    def test_bulk_create_devices(self):
        for i in range(10):
            data = {
                "name": f"Device{i}",
                "serial_number": f"SN{i:04d}"
            }
            response = self.client.post("/api/devices/", data, format='json')
            self.assertEqual(response.status_code, 201)

        self.assertEqual(Device.objects.count(), 10)


