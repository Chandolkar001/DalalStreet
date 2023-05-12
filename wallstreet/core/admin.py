from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from .utils import resolve_ipo_allotment

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
    list_display = ('rank', 'user_id', 'cash', 'net_worth')

    class Meta:
        ordering = ['rank']

class CompanyAdmin(ImportExportActionModelAdmin):
    list_display = ('company_name', 'total_no_shares', 'is_listed')

class IPOAdmin(admin.ModelAdmin):
    list_display = ('company', 'high_cap', 'low_cap', 'lot_size', 'total_volume', 'final_issue_price', 'shares_alloted', 'cash_received')

class SubsAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'quantity', 'offer_bid')
    actions = ['resolve_ipo']

    def resolve_ipo(self, request, queryset):
        resolve_ipo_allotment()
        self.message_user(request, 'Function called successfully')
    resolve_ipo.short_description = 'IPO allotment'

class BuyOrderAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'time_placed', 'quantity', 'bid_price')

class SellOrderAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'time_placed', 'quantity', 'ask_price')

class CompanySharesAdmin(admin.ModelAdmin):
    list_display = ('company', 'profile', 'shares')

class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'market_on')

admin.site.register(Market, MarketAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, PortfolioAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(IPO, IPOAdmin)
admin.site.register(Subscription, SubsAdmin)
admin.site.register(BuyOrder, BuyOrderAdmin)
admin.site.register(SellOrder, SellOrderAdmin)
admin.site.register(CompanyShares, CompanySharesAdmin)
admin.site.register(UserHistory)
# admin.site.register(News)
