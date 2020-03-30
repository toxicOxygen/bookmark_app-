from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField()
    created = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(get_user_model(),related_name='images_liked',blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("image_detail",args=[str(self.slug)])
    
    def get_like_url(self):
        return reverse('image_like',args=[str(self.pk)])
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image,self).save(*args,**kwargs)
