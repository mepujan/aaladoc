from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=400)
    tags = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_cat_url(self):
        return reverse("Forum:category", kwargs={'name': self.name})


class Article(models.Model):
    written_by = models.CharField(max_length=300)
    designation = models.TextField()
    institution = models.TextField()
    title = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    body = RichTextField()
    slug = models.CharField(max_length=400, unique=True, default="slug")
    date = models.DateField(auto_created=True)
    image = models.ImageField(upload_to='media', null=True)
    no_comments = models.IntegerField(default=0, blank=True)
    trending = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    views = models.PositiveBigIntegerField(default=0)

    def count_comments(self):
        pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Forum:blog", kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-date',)


class ArticleComments(models.Model):
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_feed_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    commentor_name = models.CharField(max_length=200, blank=True)
    is_doctor = models.CharField(max_length=5, blank=True)
    commentor_image = models.ImageField(upload_to="media", blank=True)

    def save(self, *args, **kwargs):
        print("image =", self.commentor_image)
        if self.commentor_name == '':
            self.commentor_name = self.comment_by.username

        if self.is_doctor == '':
            self.is_doctor = str(self.comment_by.is_staff)

        if self.commentor_image == '':
            self.commentor_image = self.comment_by.profile_pic
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.comment_by.username)

    class Meta:
        ordering = ('-created',)


class Question(models.Model):
    question = models.TextField()
    asked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    no_comments = models.IntegerField(default=0)
    verify = models.BooleanField(default=False)
    isAnonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    questionaire_image = models.ImageField(upload_to='media', blank=True)
    is_doctor = models.CharField(max_length=5, blank=True)
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return str(self.question)

    def save(self, *args, **kwargs):
        if self.questionaire_image == '':
            self.questionaire_image = self.asked_by.profile_pic
        if self.is_doctor == '':
            self.is_doctor = str(self.asked_by.is_staff)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class QuestionComments(models.Model):
    comment_feed_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    comments = models.TextField()
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    commentor_name = models.CharField(max_length=200, blank=True)
    commentor_image = models.ImageField(upload_to='media', blank=True)
    is_doctor = models.CharField(max_length=5, blank=True)

    def save(self, *args, **kwargs):

        if self.commentor_name == '':
            self.commentor_name = self.comment_by.username

        if self.is_doctor == '':
            self.is_doctor = str(self.comment_by.is_staff)

        if self.commentor_image == '':
            self.commentor_image = self.comment_by.profile_pic
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.comment_by.username

    class Meta:
        ordering = ('-created',)



class ArticleLiked(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} has liked {self.article.title}"

    class Meta:
        verbose_name_plural = "Liked Article"
        ordering = ("-created",)
