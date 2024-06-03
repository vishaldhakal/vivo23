from django.contrib import admin
from .models import Customer, Gift, MobilePhone, Offers, Sales, IMEINO, FixOffer, MobilePhone, RechargeCard, RechargeCardOffer


admin.site.register(Gift)
admin.site.register(Sales)
admin.site.register(IMEINO)
admin.site.register(FixOffer)
admin.site.register(MobilePhone)
admin.site.register(RechargeCard)
admin.site.register(RechargeCardOffer)


@admin.site.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = (
        "gift",
        "start_date",
        "end_date",
        "type_of_offer",
        "validto",
        "offer_condition_value",
        "quantity",
        "sale_numbers",
        "priority",
    )
    class Meta:
        model = Offers
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "shop_name",
        "sold_area",
        "phone_number",
        "phone_model",
        "sale_status",
        "gift",
        "imei",
        "date_of_purchase",
    )
    list_filter = (
        "date_of_purchase",
    )

    class Meta:
        model = Customer
