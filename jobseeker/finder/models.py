from django.db import models


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

class User_table(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField()
    last_name = models.CharField()
    gender = models.IntegerField()
    nationality = models.CharField()
    email = models.EmailField()
    phone = models.CharField()
    country_code = models.CharField()
    user_type = models.IntegerField()
    created_by = models.IntegerField()
    created_time = models.DateTimeField() 
    modified_by = models.IntegerField()
    modified_time = models.DateTimeField()
    hidden = models.BooleanField()

    # class Meta:
    #     db_table = "user_table"

