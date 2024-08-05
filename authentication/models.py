from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, password=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email)
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email,name, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  username = models.CharField(max_length=200,default="none")
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name',]

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

# class Notification(models.Model):
#     account_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         print('saving notification')
#         channel_layer = get_channel_layer()
#         notification_objs = Notification.objects.filter(is_read=False).count()
#         data = {'count': notification_objs, 'current_notification': self.message}
#         async_to_sync(channel_layer.group_send)(
#             "test_consumer_group", {
#                 "type": "send_notification",
#                 "value": json.dumps(data)
#             }
#         )
#         super(Notification, self).save(*args, **kwargs)
#     def __str__(self):
#         return self.message    

