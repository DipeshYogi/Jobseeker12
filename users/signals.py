#####THIS IS TO LET DEFAULT PROFILE PIC WHENEVER A NEW USER IS CREATED
from django.db.models.signals import post_save #signal is fired when we save a form
from django.contrib.auth.models import User  #sends signal -->SENDER
from django.dispatch import receiver #Receiver
from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
    instance.profile.save() 
