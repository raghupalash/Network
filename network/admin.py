from django.contrib import admin
from .models import User, User_Following, Post

# Register your models here.
admin.site.register(User)
admin.site.register(User_Following)
admin.site.register(Post)