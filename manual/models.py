from django.db import models

# Create your models here.

class WordDict(models.Model):
    # 단어 사전 DB 정의
    word = models.CharField(max_length=255, blank=False, null=True)
    desc = models.CharField(max_length=255, blank=False, null=True)
    word_type = models.CharField(max_length=255, blank=False, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)
            
    def __str__(self):
        return self.word

    class Meta:
        managed = True
        
class CompareWord(models.Model):
    # 이력 적재를 위한 DB 정의
    tester = models.CharField(max_length=255, blank=False, null=True) # input element
    origin_file = models.FileField(null=True, blank=True, upload_to='manual/%Y/%m/%d') # input element
    result_file = models.FileField(null=True, blank=True, upload_to='manual/%Y/%m/%d')
    result = models.TextField()
    desc = models.CharField(max_length=255) # input element
    comp = models.CharField(max_length=255)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.tester

    class Meta:
        managed = True
