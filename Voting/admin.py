from django.contrib import admin
from .models import Votechecksum, Voting
# Register your models here.

admin.site.register(Voting)
admin.site.register(Votechecksum)
