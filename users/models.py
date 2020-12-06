from django.db import models
from django.contrib.auth.models import User
#from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    p_skills = models.CharField(max_length=50, verbose_name='Primary Skills')
    s_skills = models.CharField(max_length=50, verbose_name='Secondary Skills')
    img = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Profile pic' )
    exp = models.PositiveIntegerField(verbose_name='Experience', null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        im = Image.open(self.img.path)
        if im.height>300 or im.width>300:
            op_size = (300,300)
            im.thumbnail(op_size)
            im.save(self.img.path)
    '''
