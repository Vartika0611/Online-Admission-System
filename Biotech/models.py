from django.db import models

# Create your models here.
class Enquiry(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=50)
    contactno=models.CharField(max_length=15)
    enqtext=models.CharField(max_length=500)
    regdate=models.DateTimeField()
class Login(models.Model):
    usertype=models.CharField(max_length=50)
    userid=models.CharField(max_length=100)
    password=models.CharField(max_length=16)  

class session(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    session=models.CharField(max_length=15)
    sessiondate=models.DateTimeField()

class Course(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    course_session=models.CharField(max_length=15)
    course_name=models.CharField(max_length=100)
    course_duration=models.CharField(max_length=50)
    course_fees=models.IntegerField(max_length=50)
    course_date=models.DateField()

class tbl_student(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=5)
    email=models.CharField(max_length=100)
    mobile=models.CharField(max_length=14)
    password=models.CharField(max_length=16)
    fname=models.CharField(max_length=200,null=True)
    mname=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=300,null=True)
    addharno=models.IntegerField( null=True)
    addharpic=models.FileField(upload_to='Docment_verification',null=True)
    session=models.CharField(max_length=30,null=True)
    course=models.CharField(max_length=200,null=True)
    course_duration=models.CharField(max_length=100,null=True)
    course_fees=models.CharField(max_length=10)
    hs_percent=models.CharField(max_length=10,null=True)
    hs_marksheet=models.FileField(upload_to='Docment_verification',null=True)
    inter_percent=models.CharField(max_length=10,null=True)
    inter_marksheet=models.FileField(upload_to='Docment_verification',null=True)
    profile_pic=models.FileField(upload_to='Docment_verification',null=True)
    sing=models.FileField(upload_to='Docment_verification',null=True)
    form_status=models.CharField(max_length=30,null=True)
    fees=models.CharField(max_length=20)
    fees_status=models.CharField(max_length=50)
    fees_sc=models.FileField(null=True,upload_to='myimage')
    



