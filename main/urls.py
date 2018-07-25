"""hm_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logging_out, name='logout'),
    url(r'^migrations/$', views.migrations, name='migrations'),
    url(r'^appointment/$', views.appointment, name='appointment'),
    url(r'^payments/$', views.payments, name='payments'),
    url(r'^history/$', views.history, name='history'),
    url(r'^apptstatus/$', views.create_appt, name='appt_status'),
    url(r'^paydetails/$', views.paydetails, name='pay_details'),
    url(r'^consultdetails/$', views.consultdetails, name='consult_details'),
	url(r'^buymeds/$', views.buymeds, name='buymeds'),
	url(r'^makepayment/$', views.makepayment, name='makepayment'),
	url(r'^paymentstatus/$', views.paymentstatus, name='paymentstatus'),
	url(r'^createappt/$', views.create_appt, name='createappt'),
    url(r'^docappt/$', views.doc_appt, name='docappt'),
    url(r'^updatecomments/$', views.updatecomments, name='updatecomments'),
    url(r'^createconsult/$', views.create_consult, name='createconsult'),
    url(r'^consultpage/$', views.consult_page, name='consultpage'),
    url(r'^closeconsult/$', views.close_consult, name='closeconsult'),
    url(r'^addmed/$', views.add_med, name='addmed'),
    url(r'^addmedsuccess/$', views.med_success, name='addmedsuccess'),
    url(r'^adduser/$', views.add_user, name='adduser'),
    url(r'^assignroom/$', views.assign_room, name='assignroom'),
    url(r'^showappt/$', views.apptlistfd, name='apptlistfd'),
    url(r'^cancelappt/$', views.cancel_appt, name='cancel_appt'),
    url(r'^notifications/$', views.show_notification, name='notification'),
    url(r'^consultdetailsdoc/$', views.doc_consult_page, name='consultdetailsdoc'),
    url(r'^dochistory/$', views.dochistory, name='dochistory'),
]

