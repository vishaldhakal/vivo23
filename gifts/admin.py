from django.contrib import admin
from .models import Customer, Gift, MobilePhone, Offers, Sales, IMEINO, FixOffer, MobilePhone, RechargeCard, RechargeCardOffer
from unfold.admin import ModelAdmin



class CustomAdminClass(ModelAdmin):
    pass

admin.site.register(Gift, CustomAdminClass)
admin.site.register(Sales, ModelAdmin)
admin.site.register(Offers, ModelAdmin)
admin.site.register(IMEINO, ModelAdmin)
admin.site.register(FixOffer, ModelAdmin)
admin.site.register(MobilePhone, ModelAdmin)
admin.site.register(RechargeCard, ModelAdmin)
admin.site.register(RechargeCardOffer, ModelAdmin)



@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = (
        "customer_name",
        "shop_name",
        "sold_area",
        "phone_number",
        "phone_model",
        "sale_status",
        "gift",
        "recharge_card",
        "ntc_recharge_card",
        "imei",
        "date_of_purchase",
        "how_know_about_campaign",
    )
    list_filter = (
        "date_of_purchase",
    )

    class Meta:
        model = Customer
