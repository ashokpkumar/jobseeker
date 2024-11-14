from django.db import models
import uuid
from mongoengine import Document
from mongoengine.fields import BooleanField,DynamicField,EmailField,EmbeddedDocumentField,IntField,StringField

class User_table(models.Model):
    user_id =models.CharField(primary_key=True, max_length = 100)
    first_name = models.CharField(null=True, max_length = 100)
    last_name = models.CharField(null=True, max_length = 100)
    gender = models.IntegerField(null=True)
    nationality = models.CharField(null=True, max_length = 100)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True, max_length = 100)
    country_code = models.CharField(null=True, max_length = 100)
    user_type = models.IntegerField(null=True)
    created_by = models.CharField(null=True, max_length = 100)
    created_time = models.DateTimeField(null=True) 
    modified_by = models.CharField(null=True, max_length = 100)
    modified_time = models.DateTimeField(null=True)
    hidden = models.BooleanField(null=True)
    password_hash = models.CharField(null=True, max_length = 100)

class LookupTable(models.Model):
    id = models.CharField(primary_key=True, max_length = 100)
    master_key = models.CharField( max_length = 100)
    key = models.CharField( max_length = 100)
    value = models.IntegerField()

class MongoUser(Document):
    hidden = BooleanField()
    data = DynamicField()
    email = EmailField()
    number = IntField()
    name = StringField()
    meta = {'strict':False, "collection":'mongo_user', "db_alias":'sample_mflix'}

class Document(models.Model):
    title = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploads/')  # Files will be stored in the 'uploads/' directory in your bucket
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title