from django.db import models
# python manage.py dumpdata quiz.Category quiz.Question quiz.Option > db.json
# python manage.py loaddata db.json

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Question(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['name', 'category']
        ordering = ['created_at']
    
    def __str__(self):
        return self.name


class Option(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=255)
    isAnswer = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['question', 'name', 'isAnswer']
        ordering = ['created_at']

    def __str__(self):
        return self.question.name