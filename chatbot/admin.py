from django.contrib import admin
from .models import ChatMessage

class ChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'response', 'timestamp']
    readonly_fields = ('user', 'message', 'response', 'timestamp')

admin.site.register(ChatMessage, ChatAdmin)
