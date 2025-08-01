from django.db import models
from django.contrib.auth.models import User
import string

# Create your models here.
base62_str=string.digits+string.ascii_letters

def encode_base62(num):
    if num==0:
        return base62_str[0]
    else:
        base=[]
        while num:
            num,rem=divmod(num,62)
            base.append(base62_str[rem])
        return ''.join(reversed(base))    


class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url=models.URLField()
    short_code=models.CharField(max_length=15,unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('user', 'original_url')

def __str__(self):
    return f"{self.original_url} --> {self.short_code}"
