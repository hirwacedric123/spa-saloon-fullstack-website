from django.contrib import admin
from .models import ContactMessage
from .models import Subscriber
from django import forms
from django.conf import settings


admin.site.register(ContactMessage)
admin.site.register(Subscriber)
