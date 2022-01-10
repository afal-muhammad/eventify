import datetime
import json
import stripe
import socket
from applications.events.models import Events
from decimal import Decimal
from django.conf import settings
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.
class LandingView(View):

    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        page_number = self.request.GET.get('page')
        events = Events.objects.filter(is_published=True, end_date__gte=datetime.datetime.now()).order_by('start_date')
        paginator = Paginator(events, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        return render(self.request, 'landing.html', {"events": events, 'now':now, 'page_obj': page_obj})


class PublishEventView(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        # using custom payment template
        # intent = stripe.PaymentIntent.create(
        #       amount = 5000,
        #       currency = "inr",
        #       automatic_payment_methods = {"enabled": True},
        #     )
        # amount = settings.STRIPE_PUBLISH_AMOUNT
        # event = Events.objects.get(slug=kwargs["slug"])
        # return render(self.request, 'payment.html', {'key': settings.STRIPE_PUBLISHABLE_KEY, "event":event,
        #                                                     'amount':Decimal(amount * 0.01).quantize(Decimal('1.00'))})
        # try:
        # event = Events.objects.get(slug=kwargs["slug"])

        # Using Stripe Checkout API
        current_site = get_current_site(self.request)
        if self.request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Publish '+ kwargs['slug'],
                    },
                    'unit_amount': 5000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=protocol + current_site.domain +
                        '/success?flag=True&session_id={CHECKOUT_SESSION_ID}&event=' + kwargs['slug'],
            cancel_url=protocol + current_site.domain +
                       '/success?flag=False&session_id={CHECKOUT_SESSION_ID}&event=' + kwargs['slug'],

        )
        return redirect(session.url)

    # Using Charges Api with custom payment page
    def post(self, *args, **kwargs):
        token = self.request.POST['stripeToken']
        name = self.request.POST.get('billingName')
        customer = stripe.Customer.create(email=self.request.user.email,
                                          name=name,
                                          source=token)
        charge = stripe.Charge.create(
            customer=customer,
            amount=settings.STRIPE_PUBLISH_AMOUNT,
            currency='inr',
            description='Publish Event',
        )
        reciept_link = charge.receipt_url
        event = Events.objects.get(id=self.request.POST["id"])
        if charge.status == "succeeded":
            event.is_published = True
            event.save()
            return render(self.request, 'payment-success.html', {"reciept_link":reciept_link})
        else:
            return render(self.request, 'payment-success.html')


class CreateEventView(View):

    def post(self, request):
        data = dict()
        if not request.POST["title"] or not request.POST["location"] or not request.POST["start_date"]:
            data["result"] = "You are missing any of title, location or start date"
            return HttpResponse(json.dumps(data),
                           content_type="application/json")
        formatted_date = datetime.datetime.fromisoformat(request.POST['start_date'])
        if datetime.datetime.now() >= formatted_date:
            data["result"] = "Start Date should be greater than today"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")

        # else:
        try:
            event_obj = Events.objects.get(id=request.POST['id'])
        except:
            event_obj = Events()
        event_obj.title = request.POST["title"]
        event_obj.location = request.POST["location"]
        event_obj.description = request.POST["description"]
        event_obj.user_obj = request.user
        event_obj.start_date = request.POST["start_date"]
        event_obj.end_date = request.POST["end_date"]
        if event_obj.end_date and event_obj.end_date <= event_obj.start_date:
            data["result"] = "End date should be greater than start date"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        if datetime.datetime.now() >= formatted_date:
            data["result"] = "Start Date should be greater from current time"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        if request.FILES:
            event_obj.banner = request.FILES["banner"]
        event_obj.save()
        if request.POST["publish"] == 'on':
            data["publish"] = "ON"
            data["result"] = "success"
            data["slug"] = event_obj.slug
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        else:
            data["publish"] = "OFF"
            data["result"] = "success"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")

class PaymentSuccessView(View):
    @method_decorator(login_required)
    def get(self, request):
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
        if request.GET.get('flag') == "True":
            event = Events.objects.get(slug=request.GET.get('event'))
            event.is_published = True
            event.save()
        return render(self.request, 'payment-success.html')

class EventDetailView(View):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        slug = kwargs["slug"]
        event = Events.objects.get(slug=slug)
        latest_events = Events.objects.filter(is_published=True, start_date__gt=datetime.datetime.now()).\
            order_by('start_date').exclude(slug=slug)[:4]
        print(latest_events)
        return render(self.request, 'event-detail.html', {"event":event, 'latest':latest_events})
