from django.http import *
from django.shortcuts import render_to_response,redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from models import Usr, Consultation, Payment, Room, Appointment, Prescription, Notification, Medicine
from django.contrib.auth.models import User
from datetime import date, timedelta
from random import randint
import uuid

@login_required
def index(request):
    u = Usr.objects.get(user_id=request.user)
    if u.user_type=='patient':
        ur = Usr.objects.get(user_id=request.user)
        c = Consultation.objects.filter(active=True, patient=request.user)
        a = Appointment.objects.filter(time__gte=date.today(), user_id=request.user)
        p = Prescription.objects.filter(user_id=request.user, active=True)
        return render_to_response('main.html', {'user':ur, 'consult':c, 'med':p, 'appt':a})
    elif u.user_type=='doctor':
        ur = Usr.objects.get(user_id=request.user)
        c = Consultation.objects.filter(active=True, doctor=request.user)
        return render_to_response('doctor.html', {'user':ur, 'consult':c})
    elif u.user_type=='front_desk':
        ur = Usr.objects.get(user_id=request.user)
        return render_to_response('frontdesk.html', {'user':ur})

@login_required
def apptlistfd(request):
    a = Appointment.objects.filter(active=True, time__gte=date.today())
    return render_to_response('fdappointmentlist.html', {'appt':a})

@login_required
def cancel_appt(request):
    if request.POST:
        aid = request.POST['id']
        a = Appointment.objects.filter(a_id=aid)
        usr = a[0].user_id
        time = a[0].time
        dname = a[0].doc_name
        a1 = Appointment.objects.get(a_id=aid)
        a1.active = False
        a1.save()
        n = Notification(n_id=uuid.uuid4(), patient=usr, doc_name=dname, date=time)
        n.save()
        return render_to_response('apptcancelsuccess.html')

@login_required
def show_notification(request):
    user = request.user
    n = Notification.objects.filter(patient=user)
    return render_to_response('usernotification.html', {'notification':n})

@login_required
def doc_appt(request):
    usr = request.user
    t = date.today()+timedelta(days=2)
    a = Appointment.objects.filter(doctor=usr, time__gte=date.today(), time__lte=t, active=True)
    return render_to_response('doctorappt.html', {'appt':a})

@login_required
def updatecomments(request):
    if request.POST:
        cid = request.POST['id']
        com = request.POST['comments']
        c = Consultation.objects.get(c_id=cid)
        c.comments = c.comments+"<br>"+com
        c.save()
        return render_to_response('commentsuccess.html')

@login_required
def create_consult(request):
    if request.POST:
        aid = request.POST['id']
        a = Appointment.objects.filter(a_id=aid)
        a1 = Appointment.objects.get(a_id=aid)
        patient = a[0].user_id
        pname = a[0].patient_name
        doctor = a[0].doctor
        dept = a[0].dept
        dnm = a[0].doc_name
        a1.active = False
        a1.save()
        c = Consultation(c_id=uuid.uuid4(), patient=patient, patient_name=pname, doctor=doctor, dept=dept, doc_name=dnm, comments="Consultation started", active=True)
        c.save()
        p = Payment(payment_id=uuid.uuid4(), item_id="Consultation Fees", user=patient, payment_type="Debit Card", status=0, active=True, date=date.today(), amount=200)
        p.save()
        return render_to_response('consultsuccess.html')

@login_required
def close_consult(request):
    if request.POST:
        cid = request.POST['id']
        c = Consultation.objects.get(c_id=cid)
        c.active = False
        c.save()
        return render_to_response('closeconsultsuccess.html')

@login_required
def consult_page(request):
    if request.POST:
        cid = request.POST['id']
        c = Consultation.objects.filter(c_id=cid)
        return render_to_response('consultationpage.html', {'consult': c[0]})

@login_required
def doc_consult_page(request):
    if request.POST:
        cid = request.POST['id']
        c = Consultation.objects.filter(c_id=cid)
        return render_to_response('docconsultationpage.html', {'details': c[0]})

@login_required
def add_med(request):
    if request.POST:
        uid = request.POST['id']
        return render_to_response('createprescription.html', {'user':uid})

@login_required
def med_success(request):
    usr = request.user
    if request.POST:
        uid = request.POST['id']
        med_name = request.POST['medname']
        details = request.POST['details']
        m = Prescription(p_id=uuid.uuid4(), user_id=uid, doctor=usr, medicine_name=med_name, details=details, active=True)
        m.save()
        return render_to_response('prescriptionsuccess.html')




@login_required
def payments(request):
    usr = request.user
    p = Payment.objects.filter(user=usr)
    return render_to_response('userpayments.html', {'pay':p})

@login_required
def appointment(request):
    u = request.user
    d = Usr.objects.filter(user_type="doctor")
    return render_to_response('userappt.html', {'doctors':d})

@login_required
def history(request):
    u = request.user
    h = Consultation.objects.filter(patient=u, active=False)
    return render_to_response('userhistory.html', {'history':h})

@login_required
def dochistory(request):
    u = request.user
    h = Consultation.objects.filter(doctor=u, active=False)
    return render_to_response('dochistory.html', {'history':h})

@login_required
def consultdetails(request):
    if request.POST:
        cid = request.POST['id']
        c = Consultation.objects.filter(c_id=cid)
        return render_to_response('consultdetails.html', {'details':c[0]})

@login_required
def paydetails(request):
    if request.POST:
        pid = request.POST['id']
        p = Payment.objects.filter(payment_id=pid)
        return render_to_response('paydetails.html', {'details':p[0]})
		

@login_required
def buymeds(request):
    if request.POST:
        mid = request.POST['id']
        m = Prescription.objects.filter(p_id=mid)
        y = m[0].medicine_name
        name = m[0].medicine_name + "(Medicine)"
        x = Medicine.objects.filter(name=y)
        if len(x)>0:
            am = x[0].cost
            z = Medicine.objects.get(m_id=x[0].m_id)
            z.stock -=1
            z.save()
            p = Payment(payment_id=uuid.uuid4(), item_id=name, user=request.user, payment_type="Debit Card", status=0, active=True, date=date.today(), amount=am)
            p.save()
            return render_to_response('medpaysuccess.html')
        else:
            return render_to_response('medpayfailure.html')

		
@login_required
def makepayment(request):
    user = request.user
    if request.POST:
        id = request.POST['id']
        p = Payment.objects.filter(payment_id=id)
        u = Usr.objects.filter(user_id=user)
        bal = u[0].balance
        am = p[0].amount
        return render_to_response('makepayment.html', {'id':id, 'amount':am, 'balance':bal})

@login_required
def paymentstatus(request):
    user = request.user
    if request.POST:
        id = request.POST['id']
        u = Usr.objects.filter(user_id=user)
        b = u[0].balance
        pm = Payment.objects.filter(payment_id=id)
        am = pm[0].amount
        if b>am:
            p = Payment.objects.get(payment_id=id)
            p.status = 2
            p.save()
            ur = Usr.objects.get(user_id=user)
            ur.balance = b-am
            ur.save()
            nb = b-am
            return render_to_response('paymentsuccess.html', {'balance':nb})
        else:
            return render_to_response('paymentfailure.html')

@login_required
def logging_out(request):
    logout(request)
    return render_to_response('logoutsuccess.html')
        

@login_required
def create_appt(request):
    u = request.user
    if request.POST:
        d = request.POST['id']
        t = date.today()+ timedelta(days=1)
        doc = Usr.objects.filter(user_id=d, user_type='doctor')
        ptnt = Usr.objects.filter(user_id=u, user_type='patient')
        #Only 10 appointments can be made for a doctor in a day
        tx = date.today()+timedelta(days=3)
        x = Appointment.objects.filter(doctor=d, user_id=u, time__gte=date.today(), time__lte=tx, active=True)
        y = Appointment.objects.filter(time=t, doctor=d)
        t2 = date.today()+timedelta(days=2)
        y2 = Appointment.objects.filter(time=t2, doctor=d)
        t3 = date.today()+timedelta(days=3)
        y3 = Appointment.objects.filter(time=t3, doctor=d)
        if len(x)>0:
            return render_to_response('appt_user_failure.html')
        else:
            if len(y)<10:
                a = Appointment(a_id=uuid.uuid4(), user_id=u, patient_name=ptnt[0].name, doctor=d, doc_name=doc[0].name, dept=doc[0].extra, time=t, active=True, token=len(y)+1)
                a.save()
                return render_to_response('appt_success.html', {'date':t, 'token':len(y)+1})
            elif len(y2)<10:
                a = Appointment(a_id=uuid.uuid4(), user_id=u, patient_name=ptnt[0].name, doctor=d, doc_name=doc[0].name, dept=doc[0].extra, time=t2, active=True, token=len(y2)+1)
                a.save()
                return render_to_response('appt_success.html', {'date':t2, 'token':len(y2)+1})
            elif len(y3)<10:
                a = Appointment(a_id=uuid.uuid4(), user_id=u, patient_name=ptnt[0].name, doctor=d, doc_name=doc[0].name, dept=doc[0].extra, time=t3, active=True, token=len(y3)+1)
                a.save()
                return render_to_response('appt_success.html', {'date':t3, 'token':len(y3)+1})
            else:
                return render_to_response('appt_failure.html')

       

def login_user(request):
        logout(request)
        username = password = ''
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
        return render_to_response('login.html')
    
@login_required
def add_user(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password =  request.POST['password']
        user_type = request.POST['type']
        extra = request.POST['extra']
        print user_type
        u = User.objects.create_user(email, email, password)
        u.save()
        ur = Usr(user_id=email, name=name, user_type=user_type, extra=extra)
        ur.save()
        return render_to_response('usercreatesuccess.html')

@login_required
def assign_room(request):
    if request.POST:
        user = request.POST['user']
        rn = request.POST['rno']
        sd = request.POST['sd']
        ed = request.POST['ed']
        r = Room(user_id=user, r_id=uuid.uuid4(), room_no=rn, start_date=sd, end_date=ed, available=False)
        r.save()
        return render_to_response('roomcreatesuccess.html')
        
   
def migrations(request):
    print "Step 1"
    #m1 = Medicine(m_id=uuid.uuid4(), name="Crocin", cost=20, stock=90)
    #m1.save()
    #m2 = Medicine(m_id=uuid.uuid4(), name="Lactocalamine", cost=90, stock=300)
    #m2.save()
    #m3 = Medicine(m_id=uuid.uuid4(), name="Asprin", cost=200, stock=40)
    #m3.save()
    #m4 = Medicine(m_id=uuid.uuid4(), name="Benadryl", cost=80, stock=300)
    #m4.save()
    #m5 = Medicine(m_id=uuid.uuid4(), name="Dolo", cost=35, stock=1000)
    #m5.save()
    #u = User.objects.create_user('frontdesk@hmsystem.io', 'frontdesk@hmsystem.io', 'qwerty@123')
    #u.save()
    #ur = Usr(user_id='frontdesk@hmsystem.io', name='Front Desk', user_type='front_desk', extra='Front Desk')
    #ur.save()
    #a = Appointment(a_id=uuid.uuid4(), user_id="johnku@gmail.com", patient_name="John Kurian", doctor="mtarakan@gmail.com", doc_name="Mathew Tarkan", dept="Nephrology", time=date.today(), active=True)
    #a.save()
    #c = Consultation(c_id=uuid.uuid4(), patient='johnku@gmail.com', doctor='mnandan@gmail.com', doc_name='Meera Nandan', dept='Cardiology', active=False)
    #c.save()
    #u = User.objects.create_user('mnandan@gmail.com', 'mnandan@gmail.com', 'qwerty@123')
    #u.save()
    #ur = Usr(user_id='mnandan@gmail.com', name='Meera Nandan', user_type='doctor', extra='Cardiology')
    #ur.save()
    #m = Prescription(user_id='johnku@gmail.com', p_id=uuid.uuid4(), doctor='mtarakan@gmail.com', medicine_name='Crocin', details='Twice everyday - morning and evening after food.', active=True)
    #m.save()
    #p = Payment(user='johnku@gmail.com', payment_type='Debit Card', item_id='Consultation Fee', payment_id=uuid.uuid4(), status=2, amount=300, active=True, date=date.today())
    #p.save()
    print "Done"
    #u = User.objects.create_user('johnku@gmail.com', 'johnku@gmail.com', 'qwerty@123')
    #u.save()
    #print "I am here"
    #ur = Usr(user_id='johnku@gmail.com', name='John Kurian', user_type='patient', extra='no dept')
    #ur.save()
    #c = Consultation(c_id=uuid.uuid4(), patient='johnku@gmail.com', doctor='mtarakan@gmail.com', doc_name='Mathew Tarakan', dept='Nephrology', active=True)
    #c.save()
    #d = User.objects.create_user('mtarakan@gmail.com', 'mtarakan@gmail.com', 'qwerty@123')
    #d.save()
    #dr = Usr(user_id='mtarakan@gmail.com', name='Mathew Tarakan', user_type='doctor', extra="Nephrology")
    #dr.save()