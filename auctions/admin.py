from django.contrib import admin
from auctions.models import User, Lot, Bid, Comment


class LotAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "seller", "status", "winner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "lot", "buyer", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "lot", "author", "comment")

# Register your models here.
admin.site.register(Lot, LotAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)