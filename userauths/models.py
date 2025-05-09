from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from django.dispatch import receiver


from PIL import Image
from shortuuid.django_fields import ShortUUIDField
import os 


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

GENDER = (
    ("female", "Female"),
    ("male", "Male"),
)

TITLE = (
    ("Mr", "Mr"),
    ("Mrs", "Mrs"),
    ("Miss", "Miss"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)

    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)


    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    
    identity_type = models.CharField(choices=IDENTITY_TYPE, default="national_id_card", max_length=100, null=True, blank=True)
    identity_image = models.ImageField(upload_to=user_directory_path, default="id.jpg", null=True, blank=True)

    facebook = models.URLField(default="https://facebook.com/", null=True, blank=True)
    twitter = models.URLField(default="https://twitter.com/", null=True, blank=True)
    wallet = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"
        
    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
            
        super(Profile, self).save(*args, **kwargs) 
    
    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" />' % (self.image))

    
    
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


@receiver(models.signals.pre_delete, sender=Profile)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)

