from django.contrib.auth import get_user_model
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
class Business(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    stage = models.CharField(max_length=255,  blank=True)

    def __str__(self):
        return self.business_name or 'Incomplete Profile'

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('start', 'Start'),
        ('manage', 'Manage'),
        ('growth', 'Growth'),
    )
    
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=128)
    resource = models.CharField(max_length=512)
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserIntegration(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=256)
    business_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'service', 'business_id')

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.status}"

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=1024)
    body = models.TextField()
    time = models.DateTimeField(blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=256,blank=True)
    from_user = models.CharField(max_length=256,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        print('saving notification')
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(read_at__isnull=True).count()
        data = {'count': notification_objs, 'current_notification': self.subject}
        async_to_sync(channel_layer.group_send)(
            "test_consumer_group", {
                "type": "send_notification",
                "value": json.dumps(data)
            }
        )
        super(Notification, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.subject

    

class Setting(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    business_id = models.BigIntegerField()
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
