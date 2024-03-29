from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from .utils import resolve_ipo_allotment

class UserAdmin(ImportExportActionModelAdmin):
    list_display = ('username','email')
    fieldsets = (
        (None, {
            "fields": (
                ('username'), ('first_name', 'last_name'), ('email'), 'is_active'
            ),
        }),
    )
    
class PortfolioAdmin(ImportExportActionModelAdmin):
    list_display = ('rank', 'user_id', 'cash', 'net_worth', 'is_hidden')
    actions = ['increase_cap']

    def increase_cap(self, request, queryset):
        queryset.update(cash=10000000)
        self.message_user(request, 'Increased cap to 1 CR')
    increase_cap.short_description = 'Increase cap'
    class Meta:
        ordering = ['rank']

class CompanyAdmin(ImportExportActionModelAdmin):
    list_display = ('company_name', 'total_no_shares', 'is_listed')

class IPOAdmin(ImportExportActionModelAdmin):
    list_display = ('company', 'high_cap', 'low_cap', 'lot_size', 'total_volume', 'final_issue_price', 'shares_alloted', 'cash_received')

class SubsAdmin(ImportExportActionModelAdmin):
    list_display = ('user', 'company', 'quantity', 'offer_bid')
    actions = ['resolve_ipo']

    def resolve_ipo(self, request, queryset):
        resolve_ipo_allotment()
        self.message_user(request, 'Function called successfully')
    resolve_ipo.short_description = 'IPO allotment'

class BuyOrderAdmin(ImportExportActionModelAdmin):
    list_display = ('company', 'user', 'time_placed', 'quantity', 'bid_price')

class SellOrderAdmin(ImportExportActionModelAdmin):
    list_display = ('company', 'user', 'time_placed', 'quantity', 'ask_price')

class CompanySharesAdmin(ImportExportActionModelAdmin):
    list_display = ('company', 'profile', 'shares')

class MarketAdmin(ImportExportActionModelAdmin):
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
