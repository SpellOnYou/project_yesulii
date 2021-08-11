from django.contrib import admin

from concert.models import ConcertList

#admin.site.register(ConcertList)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title','place','date','time','link')
    list_filter = ('place', 'date')

admin.site.register(ConcertList, ConcertAdmin)
