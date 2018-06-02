import django.dispatch
file_uploaded = django.dispatch.Signal(providing_args=["book"])
