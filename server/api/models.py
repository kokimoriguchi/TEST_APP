from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


# importしたmodels.ModelはDjangoのモデルを定義するためのクラス
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # __str__()メソッドは、オブジェクトを表す文字列を返す
    def __str__(self):
        return self.question_text

    def published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # models.CASCADE: Question が削除されたら外部キーで紐付いている Choice も一緒に削除する
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
