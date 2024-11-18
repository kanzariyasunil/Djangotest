from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name= 'ShopName'),
    path("about/",views.about,name= 'AboutUs'),
    path("contact/",views.contact,name= 'ContactUs'),
    path("tracker/",views.tracker,name= 'TrackingUs'),
    path("search/",views.search,name= 'search'),
    path("products/<int:myid>",views.prodView,name= 'Productview'),
    path("checkout",views.checkout,name= 'checkout'),
    path("handlerequest/",views.handlerequest,name= 'HandleRequest'),
    
]
