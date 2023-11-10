from .models import RechargeCard
from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime
from django import forms
from .models import Customer, MobilePhone, RechargeCard
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from .models import Customer, Sales, Offers, Gift, IMEINO, FixOffer, RechargeCardOffer, RechargeCard, MobilePhone
from datetime import date, timedelta
import csv
from json import dumps
from datetime import date, datetime
import random

def removerec(request):
    recs = RechargeCard.objects.all()
    recs.delete()
    return HttpResponse("Deleted")

def index(request):
    phone_models = MobilePhone.objects.all()

    error_message = request.session.pop('error_message', None)
    gift_message = request.session.pop('gift_message', None)

    context = {
        'phone_models': phone_models,
    }

    if error_message:
        context['error'] = error_message
    
    if gift_message:
        context['gift'] = gift_message

    return render(request, 'index.html', context)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def adminIndex(request):
    customerss = Customer.objects.all()
    ctx = {
        "customers": customerss
    }
    return render(request, "admin2/index.html", ctx)


def indexWithError(request):
    ctx = {
        "error": "Invalid IMEI"
    }
    return render(request, "index.html", ctx)


def uploadIMEI(request):
    with open('datas.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            okk = IMEINO.objects.create(imei_no=row[0])
            okk.save()
    ctx = {
        "error": "Invalid Uploaded"
    }
    return render(request, "index.html", ctx)


def deleteAllImeis(request):
    allimeis = IMEINO.objects.all()
    allimeis.delete()

    ctx = {
        "error": "All IMEI Deleted"
    }
    return render(request, "index.html", ctx)


def uploadIMEInos(request):
    if request.method == 'POST':
        filee = request.FILES['csv_file']
        file_data = filee.read().decode('utf-8')
        lines = file_data.split('\n')

        imei_objects = []

        for line in lines:
            line = line.strip()
            if line:
                # Validate IMEI format (15 digits)
                if len(line) == 15 and line.isdigit():
                    if IMEINO.objects.filter(imei_no=line).exists():
                        pass
                    else:
                        imei_objects.append(IMEINO(imei_no=line))
                else:
                    ctx = {'error': f'Invalid IMEI format: {line}'}
                    return render(request, 'index.html', ctx)

        # Batch insert the valid IMEI numbers
        IMEINO.objects.bulk_create(imei_objects)

        ctx = {'success': 'IMEI Uploaded'}
        return render(request, 'index.html', ctx)

    return render(request, 'upload_imei.html')

def removeDublicateImeis(request):
    imeis = IMEINO.objects.all()
    for imei in imeis:
        if IMEINO.objects.filter(imei_no=imei.imei_no).count() > 1:
            todel = IMEINO.objects.get(used=False)
            todel.delete()
    return HttpResponse("Dublicate IMEI Removed")


def reuseIMEI(request, str):
    okk = IMEINO.objects.get(imei_no=str)
    okk.used = False
    okk.save()
    ctx = {
        "error": "Invalid IMEI"
    }
    return render(request, "index.html", ctx)

def getAllImeis(request):
    #in csv
    imeis = IMEINO.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="allimeis.csv"'
    writer = csv.writer(response)
    writer.writerow(['imei_no','used'])
    for imei in imeis:
        writer.writerow([imei.imei_no,imei.used])
    return response

def upload_recharge_cards(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')

        if csv_file:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                cardno = row['cardno']
                provider = row['provider']
                amount = int(row['amount'])
                image_url = row.get('image', None)

                # Create a new RechargeCard object and save it
                recharge_card = RechargeCard(
                    cardno=cardno,
                    provider=provider,
                    amount=amount,
                    image=image_url
                )
                recharge_card.save()

            return redirect('dashboard')

    return render(request, 'upload_recharge_cards.html')


def customer_dashboard(request):
    # Retrieve all customers from the database
    customers = Customer.objects.all()
    customers_with_gifts = Customer.objects.filter(gift__isnull=False)
    customers_without_gifts = Customer.objects.filter(gift__isnull=True)

    context = {
        'customers': customers,
        'customers_with_gifts': customers_with_gifts,
        'customers_without_gifts': customers_without_gifts,
    }

    return render(request, 'customer_dashboard.html', context)


def customerlists():
    datalist = list(Customer.objects.all().values('customer_name', 'shop_name', 'sold_area', 'phone_number', 'phone_model',
                    'sale_status', 'prize_details', 'imei', 'gift__name', 'date_of_purchase', 'how_know_about_campaign'))
    return JsonResponse(datalist, safe=False)


def dashboard(request):
    datalist = list(Customer.objects.all().values('customer_name', 'shop_name', 'sold_area', 'phone_number', 'phone_model',
                    'sale_status', 'prize_details', 'imei', 'gift__name', 'date_of_purchase', 'how_know_about_campaign','ntc_recharge_card','amount_of_card','recharge_card','profession'))
    data = dumps(datalist, default=json_serial)
    return render(request, 'table2.html', {"data": data})


def download_customers_with_gifts(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Create a base queryset for customers with gifts
    queryset = Customer.objects.filter(gift__isnull=False)

    if start_date and end_date:
        # Filter data within the specified date range
        queryset = queryset.filter(
            date_of_purchase__range=(start_date, end_date))

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_with_gifts.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Shop Name', 'Sold Area', 'Phone Number', 'Phone Model',
                     'Sale Status', 'Prize Details', 'IMEI', 'Gift', 'Date of Purchase', 'How Know About Campaign', 'NTC Recharge Card', 'Amount of Ntc Card', 'Profession', 'Ncell Recharge Card'])

    # Write the data rows
    for customer in queryset:
        writer.writerow([customer.customer_name, customer.shop_name, customer.sold_area, customer.phone_number, customer.phone_model,
                         customer.sale_status, customer.prize_details, customer.imei, customer.gift, customer.date_of_purchase, customer.how_know_about_campaign, customer.ntc_recharge_card, customer.amount_of_card, customer.profession, customer.recharge_card])

    return response


def download_customers_without_gifts(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Create a base queryset for customers without gifts
    queryset = Customer.objects.filter(gift__isnull=True)

    if start_date and end_date:
        # Filter data within the specified date range
        queryset = queryset.filter(
            date_of_purchase__range=(start_date, end_date))

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_without_gifts.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Shop Name', 'Sold Area', 'Phone Number', 'Phone Model',
                     'Sale Status', 'Prize Details', 'IMEI', 'Gift', 'Date of Purchase', 'How Know About Campaign', 'NTC Recharge Card', 'Amount of Ntc Card', 'Profession', 'Ncell Recharge Card'])

    # Write the data rows
    for customer in queryset:
        writer.writerow([customer.customer_name, customer.shop_name, customer.sold_area, customer.phone_number, customer.phone_model,
                         customer.sale_status, customer.prize_details, customer.imei, customer.gift, customer.date_of_purchase, customer.how_know_about_campaign, customer.ntc_recharge_card, customer.amount_of_card, customer.profession, customer.recharge_card])

    return response


def home(request):
    context = {
    }
    return render(request, 'home.html', context)


""" def uploadCustomer2(request):
    with open('datas2.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            if(row[5]!=''):
                gifts = Gift.objects.get(name=row[5])
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7],gift=gifts)
                customer.save()
            else:
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7])
                customer.save()
            
            try:
                imeiii = IMEINO.objects.get(imei_no=row[6])
                imeiii.used = True
                imeiii.save()
            except:
                pass
    ctx = {
        "error":"Invalid IMEI"
    }
    return render(request, "index.html",ctx) """


def downloadData(request):
    # Get all data from UserDetail Databse Table
    users = Customer.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign', 'ntc_recharge_card', 'amount_of_ntc','profession','ncell_recharge_card'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
    return response


def exportSummary(request):
    saless = Sales.objects.all()
    

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="summary.csv"'

    #Get the count of each of the gifts on each sales day along with ntc_recharge card, its amount and recharge_card
    writer = csv.writer(response)
    writer.writerow(['date','card_provider','amount','count'])
    for sales in saless:
        ntc_50 = Customer.objects.filter(date_of_purchase=sales.date,ntc_recharge_card=True,amount_of_card=50).count()
        ntc_100 = Customer.objects.filter(date_of_purchase=sales.date,ntc_recharge_card=True,amount_of_card=100).count()
        ntc_200 = Customer.objects.filter(date_of_purchase=sales.date,ntc_recharge_card=True,amount_of_card=200).count()
        ntc_500 = Customer.objects.filter(date_of_purchase=sales.date,ntc_recharge_card=True,amount_of_card=500).count()
        waterbottle = Customer.objects.filter(date_of_purchase=sales.date,gift__name="Water Bottle").count()
        speaker =  Customer.objects.filter(date_of_purchase=sales.date,gift__name="Speaker").count()
        side_bag = Customer.objects.filter(date_of_purchase=sales.date,gift__name="Side Bag").count()
        
        ncell = Customer.objects.filter(date_of_purchase=sales.date,recharge_card__isnull=False)
        ncell_50 = ncell.filter(recharge_card__provider="Ncell",recharge_card__amount=50).count()
        ncell_100 = ncell.filter(recharge_card__provider="Ncell",recharge_card__amount=100).count()
        ncell_200 = ncell.filter(recharge_card__provider="Ncell",recharge_card__amount=200).count()
        ncell_500 = ncell.filter(recharge_card__provider="Ncell",recharge_card__amount=500).count()

        writer.writerow([sales.date,"Ntc",50,ntc_50])
        writer.writerow([sales.date,"Ntc",100,ntc_100])
        writer.writerow([sales.date,"Ntc",200,ntc_200])
        writer.writerow([sales.date,"Ntc",500,ntc_500])
        writer.writerow([sales.date,"Ncell",50,ncell_50])
        writer.writerow([sales.date,"Ncell",100,ncell_100])
        writer.writerow([sales.date,"Ncell",200,ncell_200])
        writer.writerow([sales.date,"Ncell",500,ncell_500])
        writer.writerow([sales.date,"Water Bottle",50,waterbottle])
        writer.writerow([sales.date,"Speaker",100,speaker])
        writer.writerow([sales.date,"Side Bag",200,side_bag])
    return response


def downloadDataToday(request):
    # Get all data from UserDetail Databse Table
    today_date = date.today()
    users = Customer.objects.filter(date_of_purchase=today_date)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="today.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign', 'ntc_recharge_card', 'amount_of_ntc','profession','ncell_recharge_card'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
    return response


def downloadDataYesterday(request):
    # Get all data from UserDetail Databse Table
    today_date = date.today() - timedelta(days=1)
    users = Customer.objects.filter(date_of_purchase=today_date)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="today.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign', 'ntc_recharge_card', 'amount_of_ntc','profession','ncell_recharge_card'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign, user.ntc_recharge_card, user.amount_of_card,user.profession,user.recharge_card])
    return response

def getNcell500(request):
    getrec = RechargeCard.objects.filter(provider="Ncell",amount=500,is_assigned=False).order_by('?').first()
    getrec.is_assigned = True
    getrec.save()
    return HttpResponse("Ncell 500 Recharge Card Assigned"+getrec.cardno)

def getNcell500Used(request):
    getrec = RechargeCard.objects.filter(provider="Ncell",amount=500,is_assigned=True)
    return JsonResponse(list(getrec.values()),safe=False)

def getNcellUsed(request):
    getrec = RechargeCard.objects.filter(provider="Ncell",is_assigned=True)
    #csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ncellused.csv"'

    writer = csv.writer(response)
    writer.writerow(['cardno','provider','amount','is_assigned'])

    for rec in getrec:
        writer.writerow([rec.cardno,rec.provider,rec.amount,rec.is_assigned])
        
    return response



def registerCustomer(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        contact_number = request.POST["phone_number"]
        shop_name = request.POST["shop_name"]
        profession = request.POST.get("profession","None")
        sold_area = request.POST["sold_area"]
        phone_model = request.POST["phone_model"]
        imei_number = request.POST["imei_number"]
        how_know_about_campaign = request.POST["how_know_about_campaign"]
        provider = request.POST["provider"]

        if Customer.objects.filter(imei=imei_number).exists():
            cust = Customer.objects.get(imei=imei_number)
            request.session['error_message'] = "The IMEI number is already registered by another customer with phone no : "+cust.phone_number
            message = ""
            if cust.gift:
                message += "You have won Gift: " + cust.gift.name
            elif cust.ntc_recharge_card:
                message += "You have won Rs : " + str(cust.amount_of_card) + " NTC Recharge Card. You Mobile would be recharged within 24hrs." 
            elif cust.recharge_card:
                message += "You have won Rs : " + str(cust.recharge_card.amount) + " Ncell Recharge card. Here's your PIN : "+ cust.recharge_card.cardno
            else:
                message += "No Gift Allocated"
            request.session['gift_message'] = message
            return redirect('index')
        
        if Customer.objects.filter(phone_number=contact_number).exists():
            request.session['error_message'] = "A customer with the same phone number already exists."
            return redirect('index')

        # Check if the IMEI number is valid and available in IMEINO table
        imei_check=False
        get_all_imeis = IMEINO.objects.filter(used=False)
        for imeei in get_all_imeis:
            if imei_number==str(imeei.imei_no):
                imei_check=True

        if(imei_check==False):
            request.session['error_message'] = "Invalid IMEI"
            return redirect('index')

        # Create a new customer
        customer = Customer.objects.create(
            customer_name=customer_name,
            phone_number=contact_number,
            shop_name=shop_name,
            sold_area=sold_area,
            phone_model=phone_model,
            sale_status="SOLD",
            imei=imei_number,
            profession=profession,
            how_know_about_campaign=how_know_about_campaign
        )

        # Mark the IMEI as used
        imeii = IMEINO.objects.get(imei_no=imei_number)
        imeii.used = True
        imeii.save()

        gift_assigned = False
        recharge_cardd = None
        recharge_card_assigned = False
        ntc_recharge_card_assigned = False

        # Select Gift or Recharge Card
        today_date = date.today()
        sales_all = Sales.objects.all()

        # Check if a sale record exists for today, if not, create one
        if not sales_all.filter(date=today_date).exists():
            saless = Sales.objects.create(sales_count=0, date=today_date)
            saless.save()

        sale_today = Sales.objects.get(date=today_date)
        get_sale_count = sale_today.sales_count
        sale_today.sales_count = get_sale_count + 1
        sale_today.save()

        fixed_offers = FixOffer.objects.all()

        for off in fixed_offers:
            if (imei_number in off.imei_no):
                if (off.quantity > 0):
                    customer.gift = off.gift
                    customer.save()
                    gift_assigned = True
                    off.quantity = 0
                    off.save()
                    break

        if not gift_assigned:
            # Retrieve the weekly offer based on the current date
            weekly_offer = Offers.objects.filter(
                start_date__lte=today_date, end_date__gte=today_date, type_of_offer="Weekly Offer")

            for offer in weekly_offer:
                if ((get_sale_count + 1) in offer.sale_numbers) and (offer.quantity > 0):
                    qty = offer.quantity
                    customer.gift = offer.gift
                    customer.save()
                    offer.quantity = qty - 1
                    offer.save()
                    gift_assigned = True
                    break

        if not gift_assigned:
            for offer in Offers.objects.filter(end_date__gte=today_date):
                if offer.type_of_offer == "After every certain sale":
                    if (((get_sale_count + 1) % int(offer.offer_condition_value) == 0)) and (offer.quantity > 0):
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty - 1
                        offer.save()
                        gift_assigned = True
                        break
                if offer.type_of_offer == "At certain sale position":
                    if ((get_sale_count + 1) == int(offer.offer_condition_value)) and (offer.quantity > 0):
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty - 1
                        offer.save()
                        gift_assigned = True
                        break

        if not gift_assigned:
            # Check for Recharge Card offers
            recharge_card_offers = RechargeCardOffer.objects.filter(
                start_date__lte=today_date, end_date__gte=today_date,provider=provider).order_by('-amount')

            for recharge_card_offer in recharge_card_offers:
                if recharge_card_offer.type_of_offer == "After every certain sale":
                    if (((get_sale_count + 1) % int(recharge_card_offer.offer_condition_value) == 0)) and (recharge_card_offer.quantity > 0):
                        qty = recharge_card_offer.quantity
                        recharge_card_offer.quantity = qty - 1
                        recharge_card_offer.save()
                        if provider == "Ncell":
                            recharge_card_assigned = True
                            amt = recharge_card_offer.amount
                            recharge = RechargeCard.objects.filter(
                                provider=provider, is_assigned=False,amount=amt).order_by('?').first()
                            recharge.is_assigned = True
                            recharge.save()
                            recharge_cardd = recharge
                            customer.recharge_card = recharge
                            customer.save()
                        else:
                            ntc_recharge_card_assigned = True
                            customer.amount_of_card = recharge_card_offer.amount
                            customer.ntc_recharge_card = True
                            customer.save()
                        break
                else:
                    if ((get_sale_count + 1) in recharge_card_offer.sale_numbers) and (recharge_card_offer.quantity > 0):
                        qty = recharge_card_offer.quantity
                        recharge_card_offer.quantity = qty - 1
                        recharge_card_offer.save()
                        if provider == "Ncell":
                            recharge_card_assigned = True
                            recharge = RechargeCard.objects.filter(
                                provider=provider, is_assigned=False).order_by('?').first()
                            recharge.is_assigned = True
                            recharge.save()
                            recharge_cardd = recharge
                            customer.recharge_card = recharge
                            customer.save()
                        else:
                            ntc_recharge_card_assigned = True
                            customer.amount_of_card = recharge_card_offer.amount
                            customer.ntc_recharge_card = True
                            customer.save()
                        break
                            
        return render(request, "output.html", {"customer": customer, "gift_assigned": gift_assigned,"recharge_card": recharge_cardd, "recharge_card_assigned": recharge_card_assigned,"ntc_recharge_card_assigned": ntc_recharge_card_assigned })
    else:
        return redirect('indexWithError')
    

def convallrec(request):
    custt = Customer.objects.filter(recharge_card__isnull=False)
    for cus in custt:
        recc = cus.recharge_card
        recc.is_assigned = True
        recc.save()