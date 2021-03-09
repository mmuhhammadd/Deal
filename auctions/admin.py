from django.contrib import admin
from .models import Listings, Bids, Comments, Categories, Watchlist

class CategoriesAdmin(admin.ModelAdmin):
    Detail_display = ("category")

# Register your models here.
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Watchlist)