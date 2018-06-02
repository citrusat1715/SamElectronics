# In receivers.py
from django.dispatch import receiver
from .signals import *
from django.shortcuts import render, redirect
print(@receiver(file_uploaded))
def notify(sender, **kwargs):
    print('hello')
    return redirect('home')
