from django.contrib import admin
from auctions.models import User, Lot, Bid, Comment


class LotAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "seller", "status", "winner")

# Register your models here.
admin.site.register(Lot, LotAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)