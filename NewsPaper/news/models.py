from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models import Sum



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        sum_post_rating =Post.objects.filter(id=self.user_id).aggregate(Sum('rating'))
        sum_pos = sum_post_rating['rating__sum'] * 3
        sum_author_comment_rating = Comment.objects.filter(id=self.user_id).aggregate(Sum('rating'))
        sum_comment_rating = Comment.objects.filter(id=self.user_id).aggregate(Sum('rating'))
        self.rating= sum_pos + sum_author_comment_rating['rating__sum'] + sum_comment_rating['rating__sum']
        self.save()


class Category(models.Model):
    name_cat = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscriber', blank=True)

    def __str__(self):
        return f'{self.name_cat}'


class Post(models.Model):
    news = 'NS'
    article = 'AR'
    CAT_CHOISE = [
        (news, 'новость'),
        (article, 'статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choise = models.CharField(max_length=2, choices=CAT_CHOISE, default=article)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text
        if self.choise == Post.article:
            return text[0:123] + "..."


    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        # получить название поста
        return f'{self.title}. {self.text[:124]} ...'

    def message_subscriber(self):
        return f'Новая статья - "{self.title}" в разделе "{self.category.first()}" '

class PostCategory(models.Model):
    past = models.ForeignKey(Post, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        # получить название поста
        return f'{self.post}. {self.category}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='com1')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='com2')
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        # return self.commentPost.author.authorUser.username  # получить имя автора поста
        return f'{self.user.username}'