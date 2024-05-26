from django.db import models
import uuid

class ATMSite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    site_id = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    contact_details = models.JSONField()
    
    class Meta:
        db_table = 'atm_site'

class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    atm_site = models.ForeignKey(ATMSite, on_delete=models.CASCADE, related_name='state')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'state'

    
class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    atm_site = models.ForeignKey(ATMSite, on_delete=models.CASCADE, related_name='city')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'city'
