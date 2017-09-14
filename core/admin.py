from django.contrib import admin
from .models import Permit, Development, Offset, OffsetImplementationTime

admin.site.register(Permit)
admin.site.register(Development)
admin.site.register(Offset)
admin.site.register(OffsetImplementationTime)
