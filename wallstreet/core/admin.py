from django.contrib import admin
from .models import User, Portfolio

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')
    fieldsets = (
        (None, {
            "fields": (
                ('username'), ('first_name', 'last_name'), ('email'), 'is_active'
            ),
        }),
    )
    
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


admin.site.register(User, UserAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
