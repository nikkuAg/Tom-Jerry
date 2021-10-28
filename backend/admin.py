from django.contrib import admin
from .models import User, Request_Confirm, Request_Sent, Audit
# Register your models here.

admin.site.register(User)
admin.site.register(Request_Sent)
admin.site.register(Request_Confirm)
admin.site.register(Audit)
