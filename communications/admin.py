from django.contrib import admin

from communications.models import PrivateRoomChatImage, PrivateChatRoom, PrivateRoomChatMessage

# Register your models here.

admin.site.register(PrivateChatRoom)
admin.site.register(PrivateRoomChatMessage)
admin.site.register(PrivateRoomChatImage)
