from django.db import models
import sys
sys.path.append('../')
from accounts.models import User

# Create your models here.

class Studio(models.Model):
    name = models.CharField('スタジオ名',max_length=255)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    personCount = models.IntegerField('人数')
    user = models.ForeignKey(User,verbose_name="予約者",on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio,verbose_name="スタジオ",on_delete=models.CASCADE)
    created_at = models.DateTimeField("予約完了日時",auto_now_add=True)
    updated_at = models.DateTimeField("変更日時",auto_now=True)