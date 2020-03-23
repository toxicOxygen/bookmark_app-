from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

# Create your models here.

class CustomUser(AbstractUser):

    photo = models.ImageField(upload_to='profile/%Y/%m/%d/',blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    following = models.ManyToManyField('self',through='Contact',related_name='followers',symmetrical=False)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user_detail',args=[str(self.username),])


class Contact(models.Model):
    user_from = models.ForeignKey(get_user_model(),related_name='rel_from_set',on_delete=models.CASCADE)
    user_to = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)