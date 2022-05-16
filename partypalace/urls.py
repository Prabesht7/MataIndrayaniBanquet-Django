from django.urls import path
from partypalace.views.homepage import Homepage
from partypalace.views.contact import Contact

urlpatterns = [
    path('MataIndrayaniBanquet', Homepage.as_view(), name='homepage'),
    path('contact', Contact.as_view(), name='contact')
]
