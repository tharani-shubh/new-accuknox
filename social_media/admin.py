from django.contrib import admin
from social_media.models import Member, Friendship

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'password')
    search_fields = ('email', 'name')


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_member', 'from_member', 'status')
    search_fields = ('id', 'status')


admin.site.register(Member, MemberAdmin)
admin.site.register(Friendship, FriendshipAdmin)
