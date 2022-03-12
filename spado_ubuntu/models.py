from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
# import 
import random
from datetime import datetime
# Create your models here.

class Issue(models.Model):
    problem = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ['problem']

    def __str__(self):
        return self.problem


class PostImage(models.Model):
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)


class Account(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100) # DISABLED
    is_valid = models.BooleanField(default=False) # DISABLED (DEFAULT=True)
    liked_tags = TaggableManager(blank=True)
    status = models.CharField(max_length=12, blank=False, null=False, default="Working")
    status_indicator = models.CharField(max_length=15, blank=False, null=False, default="Available")
    community = models.ManyToManyField(User, blank=True, related_name='community')
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='images/profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_posts(self):
        return Post.objects.filter(author=self)

    def __str__(self):
        return "Auth_Token:"+(self.auth_token)+"User name:"+self.user_name.username+";Valid user:"+str(self.is_valid)+";Created on:"+str(self.created_at)

class Comment(models.Model):

    descr = models.TextField(null=False, blank=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False)
    likes = models.ManyToManyField(User, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    
    def time_since(self):
        c_time = datetime.utcnow() 
        if c_time.year == self.created_on.year:
            if c_time.month == self.created_on.month:
                if c_time.day == self.created_on.day:
                    if c_time.hour == self.created_on.hour:

                        if c_time.minute == self.created_on.minute:

                            return "Just now"
                        else:
                            print('*'*16)
                            print(f"c_time.minute = {c_time.minute}, self.created_on.minute = {self.created_on.minute}")
                            res = str(c_time.minute - self.created_on.minute)
                            return res + ' minute' +'s'*(int(res) > 1) + ' ago'
                    else:
                        res = str(c_time.hour - self.created_on.hour)
                        return res + ' hour' +'s'*(int(res) > 1) + ' ago'

                else:
                    res = str(c_time.day - self.created_on.day)
                    return res + ' day' +'s'*(int(res) > 1) + ' ago'

            else:
                res = str(c_time.month - self.created_on.month)
                return res + ' month' +'s'*(int(res) > 1) + ' ago'

        else:

            res = str(c_time.year - self.created_on.year)
            return res + ' year' +'s'*(int(res) > 1) + ' ago'

    def __str__(self):
        return str(self.author.user_name.username) + " | " + str(self.descr if len(self.descr) < 20 else self.descr[:20])



class Post(models.Model):


    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    # username = author.username
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    descr = RichTextField(blank=False, null=False)
    likes = models.ManyToManyField(User, related_name="liked_by", blank=True)
    dislikes = models.ManyToManyField(User, related_name="disliked_by", blank=True)
    
    comments = models.ManyToManyField(Comment, blank=True)

    # images = models.ManyToManyField(PostImage, related_name="post_image")
    image_1 = models.ImageField(upload_to='images/posts/images_1 %y/%m/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='images/posts/images_2 %y/ %m/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='images/posts/images_3 %y/ %m/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='images/posts/images_4 %y/ %m/', blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    
    # class Meta:
    #     ordering = ['likes']

    def time_since(self):
        c_time = datetime.utcnow() 
        if c_time.year == self.created_on.year:
            if c_time.month == self.created_on.month:
                if c_time.day == self.created_on.day:
                    if c_time.hour == self.created_on.hour:

                        if c_time.minute == self.created_on.minute:

                            return "Just now"
                        else:
                            print('*'*16)
                            print(f"c_time.minute = {c_time.minute}, self.created_on.minute = {self.created_on.minute}")
                            res = str(c_time.minute - self.created_on.minute)
                            return res + ' minute' +'s'*(int(res) > 1) + ' ago'
                    else:
                        res = str(c_time.hour - self.created_on.hour)
                        return res + ' hour' +'s'*(int(res) > 1) + ' ago'

                else:
                    res = str(c_time.day - self.created_on.day)
                    return res + ' day' +'s'*(int(res) > 1) + ' ago'

            else:
                res = str(c_time.month - self.created_on.month)
                return res + ' month' +'s'*(int(res) > 1) + ' ago'

        else:

            res = str(c_time.year - self.created_on.year)
            return res + ' year' +'s'*(int(res) > 1) + ' ago'

        # if c_time.minute == self.created_on.minute:
        #     return "Just now"

        # else:# below returning appended 's' only if timezone(Hr, Min, Sec, etc..) is > 1
        #     if c_time.hour == self.created_on.hour:
        #         res = c_time.minute - self.created_on.minute
        #         return str(res) + " minute"+ "s"*(res>1) +" ago"

        #     else:
        #         if c_time.day == self.created_on.day:
        #             res = c_time.hour - self.created_on.hour
        #             return str(res) + " hour"+ "s"*(res>1) +" ago"
        #         else:
        #             if c_time.month == self.created_on.month:
        #                 res = c_time.day - self.created_on.day
        #                 return str(res) + " day"+ "s"*(res > 1) +" ago"
        #             else:
        #                 if c_time.year == self.created_on.year:
        #                     res = c_time.month - self.created_on.month
        #                     return str(res) + ' year'+ "s"*(res>1) +' ago'

# func.need_time(as_=invoke, call_args={'in':'0', 'overflow':'{PYTHON.None}'})


    def __str__(self):
        return str(self.author) + " | " + str(self.title)


class user_post_action(models.Model):
    # Thik about it
    # Maybe we link to another table colmns furtherwards
    # (-)
    user = models.ForeignKey(User, on_delete=models.CASCADE, name="user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, name="post")
    action = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return str(self.user.pk) + " | " + str(self.post.pk) + " | " + str(self.action)


class Feedback(models.Model):
    sent_by = models.ForeignKey(User, on_delete=models.PROTECT)
    issues = models.ManyToManyField(Issue)
    experiance = models.CharField(max_length=8)

    def __str__(self):
        all_issues = ", ".join(str(iss) for iss in self.issues.all())
        return str(self.sent_by.username) + ' | ' + str(self.experiance) + ' | ' + str(all_issues)