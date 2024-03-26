from django.db import models
from django.utils import timezone
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class TicketQR(models.Model):
    user = models.CharField(max_length=100)
    flight = models.CharField(max_length=100)
    flight_ddate = models.DateField()
    flight_adate = models.DateField()
    total_fare = models.FloatField()
    status = models.CharField(max_length=50)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # A flag to check if the object is new
        is_new = self._state.adding
        
        # Initially save the instance to ensure it has an ID for barcode generation.
        super().save(*args, **kwargs)

        qr_data = f"{self.user}, {self.flight}, {self.flight_ddate}, {self.flight_adate}, {self.total_fare}, {self.status}"
        
        if not self.qr_code:
            qr_img = qrcode.make(qr_data)
            qr_buf = BytesIO()
            qr_img.save(qr_buf, format='PNG')
            self.qr_code.save(f"qr_{self.id}.png", File(qr_buf), save=False)
            qr_buf.close()

        if not self.barcode:
            barcode_buf = BytesIO()
            EAN13(str(self.id).zfill(12), writer=ImageWriter()).write(barcode_buf)
            self.barcode.save(f"barcode_{self.id}.png", File(barcode_buf), save=False)
            barcode_buf.close()

        # If the object was new, it has already been saved with an ID and QR/barcode images.
        # If it was an existing object being updated, there's no need for a second save here,
        # unless other fields not related to QR/barcode are being updated in the same operation.
        if not is_new:
            super().save(*args, **kwargs)  # Consider commenting this out if not needed.


    def __str__(self):
        return f"{self.flight} | {self.user}"
