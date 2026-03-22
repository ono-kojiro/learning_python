from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class NIC(models.Model):
    device = models.ForeignKey(
            Device,
            null=True,
            blank=True,
            related_name='nics',
            on_delete=models.CASCADE
    )

    name = models.CharField(max_length=50)  # eth0, em1, igb0 など
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.device:
            return f"{self.device.name} - {self.name}"
        else :
            return f"(no device) - {self.name}"

