from django.db import models
import uuid


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

class User_table(models.Model):
    user_id =models.CharField(primary_key=True)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    gender = models.IntegerField(null=True)
    nationality = models.CharField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True)
    country_code = models.CharField(null=True)
    user_type = models.IntegerField(null=True)
    created_by = models.CharField(null=True)
    created_time = models.DateTimeField(null=True) 
    modified_by = models.CharField(null=True)
    modified_time = models.DateTimeField(null=True)
    hidden = models.BooleanField(null=True)
    password_hash = models.CharField(null=True)

    # class Meta:
    #     db_table = "user_table"

class LookupTable(models.Model):
    id = models.CharField(primary_key=True)
    master_key = models.CharField()
    key = models.CharField()
    value = models.IntegerField()