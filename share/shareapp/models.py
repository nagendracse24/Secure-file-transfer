from django.db import models
from django.contrib.auth.hashers import make_password,check_password


class Users(models.Model):
    username= models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    is_admin = models.IntegerField(default=0)

def initData():
        user1 = Users.objects.create(username='leandra@rvce.edu.in', password=make_password('rvce@1234'), is_admin=0)
        user2 = Users.objects.create(username='ashish@rvce.edu.in', password=make_password('rvce@5678'), is_admin=0)
        user3= Users.objects.create(username='admin@rvce.edu.in', password=make_password('admin@rvce'), is_admin=1)
        user1.save()
        user2.save()
        user3.save()

# initData()
