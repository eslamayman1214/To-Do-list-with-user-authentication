from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(                                        # null,balnk by defualt --> false
        User,on_delete = models.CASCADE, null = True, blank = True) #null True--> can be null in db, blank true--> not required in the form
    title = models.CharField(max_length =200)
    description = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
     
    def __str__(self):  # offical reprsentation of the model
        return self.title
    
    class Meta:
        ordering = ['complete']             #order upon complete status yes/no 