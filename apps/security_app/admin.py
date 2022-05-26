from django.contrib import admin
from .models import Sharer

class ListingSharers( admin.ModelAdmin ):
    list_display = ('id','user', 'code', 'limit_visits', 'limit_datetime','public')
    list_display_links = ('id','user')
    search_fields = ('user',)
    list_editable = ('limit_visits','limit_datetime','public')
    list_per_page = 30

admin.site.register(Sharer,ListingSharers)