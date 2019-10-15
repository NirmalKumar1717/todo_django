from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    


    def __str__(self):
        return self.username

class Todo(models.Model):
    text = models.CharField(max_length =50)
    complete = models.BooleanField(default=False)

def __str__(self):
    return self.text