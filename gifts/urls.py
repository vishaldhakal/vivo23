from django import views
from django.contrib import admin
from django.urls import path
from .views import customer_dashboard, convallrec,getNcellUsed,customerlists,getNcell500Used,removerec,getNcell500, download_customers_with_gifts, download_customers_without_gifts, home, index, dashboard, upload_recharge_cards,uploadIMEI, registerCustomer,deleteAllImeis,adminIndex,uploadIMEInos,indexWithError,downloadData,downloadDataToday,downloadDataYesterday,reuseIMEI,exportSummary

urlpatterns = [
    path('', index,name='index'),
    path('dash/', adminIndex,name = 'adminIndexx'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('customerlists/', customerlists, name='customerlists'),
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', home, name='home'),
    path('removerec/', removerec, name='removerec'),

    path('download_customers_with_gifts/', download_customers_with_gifts,
         name='download_customers_with_gifts'),
    path('download_customers_without_gifts/', download_customers_without_gifts,
         name='download_customers_without_gifts'),
    path('upload-recharge-cards/', upload_recharge_cards,
         name='upload_recharge_cards'),
    path('uploadimei/', uploadIMEInos, name='uploadimei'),
    path('upload/', uploadIMEI,name = 'uploaddd'),
    path('delete-all-imei/', deleteAllImeis,name = 'deleteimeis'),
    path('', indexWithError,name = 'indexWithError'),
    path('output/', registerCustomer,name = 'register_customer'),
    path('export/', downloadData,name = 'down'),
    path('reuseimei/<str>/', reuseIMEI,name = 'reuseIMEI'),
    path('export-today/', downloadDataToday,name = 'down-today'),
    path('export-summary/', exportSummary,name = 'exportSummary'),
    path('recc/', convallrec,name = 'convallrec'),
    path('export-yesterday/', downloadDataYesterday,name = 'down-yest'),
    path('get-ncell-500/', getNcell500,name = 'getNcell500'),
    path('get-ncell-500-used/', getNcell500Used,name = 'getNcell500Used'),
    path('get-used-ncell/', getNcellUsed,name = 'getNcellUsed'),
]
