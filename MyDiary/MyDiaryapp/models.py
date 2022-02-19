from django.db import models

# Create your models here.
class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=320,null=False,blank=False)
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    gender = models.CharField(default="null",max_length=50,null=False,blank=False)
    mobile_no = models.CharField(max_length=50,null=False,blank=False)
    password = models.CharField(max_length=300,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default="True")

    class Meta:
        db_table = 'user_login'

class Tokens(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    valid_upto = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Signup, related_name='TOKEN', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tokens'

class Journals(models.Model):
    id = models.AutoField(primary_key=True)
    journal = models.ForeignKey(Signup,related_name='JOURNAL',on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,null=False,blank=False)
    cover = models.URLField(null=True, blank=True)
    isset_password = models.BooleanField(default="False")
    password = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'journals'

class Pages(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Journals, related_name='PAGE', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        db_table = 'pages'

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(Pages, related_name='IMAGE', on_delete=models.CASCADE, blank=True, null=True)
    cover = models.ImageField()

    class Meta:
        db_table = 'images'
