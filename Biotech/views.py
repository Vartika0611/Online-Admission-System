from django.shortcuts import render,HttpResponse, redirect
from django.utils import timezone
from .models import Enquiry,Login,session,tbl_student,Course
from django.contrib import messages
from .import smssender
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
def layout(request):
    return render(request,'layout.html')

def home(req):
    return render(req,'home.html')

def about(req):
    return render(req,'about.html')

def Contact(req):
    if req.method=="POST":
        Name=req.POST['name']
        email=req.POST['email']
        contactno=req.POST['contactno']
        enqtext=req.POST['enqtext']
        regdate=timezone.now()
        Enquiry.objects.create(
    name=Name,
    email=email,
    contactno=contactno,
    enqtext=enqtext,
    regdate=regdate
)
        smssender.sendsms(contactno)
        messages.success(req,"Enquiry Saved")
        return redirect('Contact')
    return render(req,'contact.html')

def login(req):
    return render(req,'login.html')

def logcode(request):
    if request.method=="POST":
        usertype=request.POST['usertype']
        username=request.POST['userid']
        password=request.POST['password']
        user=Login.objects.filter(userid=username,password=password).first()
        if user:
            if user.usertype=="admin" and usertype=="admin":
                request.session['adminid']=username
                return redirect('adminhome')
            elif usertype=="student" and usertype=="student":
                request.session['studentid']=username
                return redirect('studentzone')
            else:
                return redirect('login')
        else:
            return redirect('login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminzone(request):
    if 'adminid' in request.session:
        return render(request,'adminzone.html')
    else:
        return redirect('login')
def logout(request):
    request.session.flush()
    return redirect('login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addsession(request):
    if request.method == "POST":
    
        SessionName = request.POST['session']
        sessiondate = timezone.now()
        if session.objects.filter(session=SessionName).exists():
            messages.error(request, "This session already exists.")
            return redirect('addsession')

        session.objects.create(session=SessionName, sessiondate=sessiondate)
        messages.success(request, "Session is successfully stored.")
        return redirect('addsession')

    return render(request, 'addsession.html')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def showsession(request):
    sh=session.objects.all()
    return render(request,'showsession.html',{'sh':sh})
def sessiondelete(request,id):
        dl=session.objects.get(pk=id)
        dl.delete()
        return redirect('showsession')

def addcourse(request):
    # सभी सेशन प्राप्त करें
    sh = session.objects.all()

    if request.method == "POST":
        # यूज़र से डेटा प्राप्त करें
        course_session = request.POST['course_session']
        course_name = request.POST['course_name']
        course_duration = request.POST['course_duration']
        course_fees = request.POST['course_fees']
        course_date = timezone.now()
        # वेलिडेशन: चेक करें कि कोर्स का नाम पहले से मौजूद है या नहीं
        if Course.objects.filter(course_name=course_name).exists():
            messages.error(request, 'This course name already exists. Please choose a different name.')
            return redirect('addcourse')

        # डेटा सेव करें
        Course.objects.create(
            course_session=course_session,
            course_name=course_name,
            course_duration=course_duration,
            course_fees=course_fees,
            course_date=course_date
        )
        messages.success(request, 'Course Successfully Added')
        return redirect('addcourse')

    return render(request, 'addcourse.html', {'sh': sh})

def showcourse(request):
    sh=Course.objects.all()
    return render(request,'showcourse.html',{'sh':sh})
def deletecourse(request,id):
    dl=Course.objects.get(id=id)
    dl.delete()
    return redirect('showcourse')

def editsession(request,id):
    ab=session.objects.get(id=id)
    if request.method=="POST":
        Session=request.POST['session']
        sessiondate=timezone.now()
        session.objects.filter(id=id).update(session=Session,sessiondate=sessiondate)
        return redirect('showsession')
    return render(request,'editsession.html',{'ab':ab})

def editcourse(request,id):
    ab=Course.objects.get(id=id)
    if request.method=="POST":
        course_session=request.POST['course_session']
        course_name=request.POST['course_name']
        course_duration=request.POST['course_duration']
        course_fees=request.POST['course_fees']
        course_date=timezone.now()
        Course.objects.filter(id=id).update(course_session=course_session,course_name=course_name,course_duration=course_duration,course_fees=course_fees,course_date=course_date)
        return redirect('showcourse')
    return render(request,'editcourse.html',{'ab':ab})

def addstudent(request):
    if request.method=="POST":
        name=request.POST['name']
        gender=request.POST['gender']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        usertype="student"
        ab=tbl_student(name=name,gender=gender,email=email,mobile=mobile,password=password)
        ca=Login(usertype=usertype,userid=email,password=password)
        ab.save()
        ca.save()
        subject = 'Welcome to Biotech Park Lucknow – Your Online Admission Details'
        html_content = render_to_string('welcome_email.html', {'name': name, 'emailaddress': email, 'password': password})

        # Send email
        email = EmailMultiAlternatives(subject, "This is the plain text version.", settings.DEFAULT_FROM_EMAIL, [email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request,'Student Add Successfully')
        return redirect('addstudent')

    return render(request,'addstudent.html')

def showstudent(request):
    sh=tbl_student.objects.all()
    return render(request,'showstudent.html',{'sh':sh})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def studentzone(request):
    if 'studentid' in request.session:
            return render(request,'studentzone.html')
    else:
        return redirect('login')    

def studentlogout(request):
    request.session.flush()
    return redirect('login')

def updateprofile(request):
    user_email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=user_email).first()
    dir={
        'sh':user
    }
    return render(request,'updateprofile.html',dir)
def updateprosave(request):
    email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=email).first()
    if user:
        user.name=request.POST['name']
        user.gender=request.POST['gender']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.fname=request.POST['fname']
        user.mname=request.POST['mname']
        user.address=request.POST['address']
        user.save()
        return redirect('document')
def document(request):
    ab=session.objects.all()
    ba=Course.objects.all()
    if request.method=="POST":
        email=request.session.get('studentid')
        user=tbl_student.objects.filter(email=email).first()
        if user:
            user.addharno=request.POST['addharno']
            if 'addharpic' in request.FILES:
                user.addharpic=request.FILES['addharpic']
            user.session=request.POST['session']
            user.course=request.POST['course']
            user.course_duration=request.POST['course_duration']
            user.hs_percent=request.POST['hs_percent']
            if 'hs_marksheet' in request.FILES:
                user.hs_marksheet=request.FILES['hs_marksheet']
            user.inter_percent=request.POST['inter_percent']
            if 'inter_marksheet' in request.FILES:
                user.inter_marksheet=request.FILES['inter_marksheet']
            if 'profile_pic' in request.FILES:
                user.profile_pic=request.FILES['profile_pic']
            if 'sing' in request.FILES:
                user.sing=request.FILES['sing']
            user.form_status="Panding"
            c=Course.objects.get(course_name=user.course)
            fees=c.course_fees
            user.course_fees=fees
            user.save()
            return redirect('feespayment')

    return render(request,'document.html',{'ab':ab,'ba':ba})

def feespayment(request):
    email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=email).first()
    if user.form_status=="Panding":
        # return redirect('verficationpanding')
        return HttpResponse("Your documents have not been verified by the admin yet.")
    elif user.form_status=="Approve":
        user_email=request.session.get('studentid')
        user=tbl_student.objects.filter(email=user_email).first()
        dir={
        'sh':user
         }
        return render(request,'fees.html',dir)
    
def Approvedoc(request):
    email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=email).first()
    if user:
        user.form_status="Approve"
        user.save()
        return redirect('document_Verification')
    
def verficationpanding(request):
    return render(request,'verfipanding.html')

def feessave(req):
    if req.method=="POST":
        email=req.session.get('studentid')
        user=tbl_student.objects.filter(email=email).first()
        if user:
            user.fees_sc=req.FILES['fees_sc']
            user.fees_status="Not_check"
            user.save()
        return redirect('course_Alloted')
    
def course_Alloted(request):
    email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=email).first()
    if user:
        if user.fees_status=="Not_check":
            # return redirect('paymentpanding')
            return HttpResponse("Your payment is under review. Please wait for the admin to verify your payment before proceeding further.")
        elif user.fees_status=="check":
            user_email=request.session.get('studentid')
            user=tbl_student.objects.filter(email=user_email).first()
            dir={
            'sh':user
             }
            return render(request,'course_Alloted.html',dir)
    
        else:
             return redirect('paymentpanding')

        
def paymentpanding(request):
     user_email=request.session.get('studentid')
     user=tbl_student.objects.filter(email=user_email).first()
     dir={
     'sh':user
         }
     return render(request,'paymentpanding.html',dir)

def fees_approve(request):
     user_email=request.session.get('studentid')
     user=tbl_student.objects.filter(email=user_email).first()
     if user:
         user.fees_status="check"
         user.save()
         subject = '🎉 Admission Successfully Completed'
         html_content = render_to_string('welcome_email1.html', {'name': user.name, 'course_name':user.course,'duration': user.course_duration})

        # Send email
         email = EmailMultiAlternatives(subject, "This is the plain text version.", settings.DEFAULT_FROM_EMAIL, [user.email])
         email.attach_alternative(html_content, "text/html")
         email.send()
         return redirect('pendingfees')

def studenthome(req):
    user_email=req.session.get('studentid')
    user=tbl_student.objects.filter(email=user_email).first()
    dir={
    'sh':user
        }
    return render(req,'studenthome.html',dir)

def verfiyfeesstu(req):
     user_email=req.session.get('studentid')
     user=tbl_student.objects.filter(email=user_email)
     return render(req,'verfiyfeesdtu.html',{'sh':user})

def about(request):
       return render(request,'about.html')
def courses(request):
       return render(request,'courses.html')

def adminhome(req):
    ab=tbl_student.objects.count()
    ba=Course.objects.count()
    ca=Enquiry.objects.count()
    da=session.objects.all()
    # user_email=req.session.get('studentid')
    # user=tbl_student.objects.filter(email=user_email).first()
    # if user:
    #    fscount= user.form_status=="Pending".count()
    # else:
    #     fscount=0

    return render(req,'adminhome.html',{'ab':ab,'ba':ba,'ca':ca,'da':da,})

def pendingfees(request):
    user_email=request.session.get('studentid')
    user=tbl_student.objects.filter(email=user_email).first()
    if user.fees_status=="Not_check":
        user_email=request.session.get('studentid')
        user=tbl_student.objects.filter(email=user_email)
        dir={
             'sh':user
         }
        return render(request,'pendingfees.html',dir)
    else:
        return render(request,'pendingfees.html')


def document_Verification(request):
     user_email=request.session.get('studentid')
     user=tbl_student.objects.filter(email=user_email).first()
     if user.form_status=="Panding":
         sh=tbl_student.objects.all()
         return render(request,'docverify.html',{'sh':sh}) 
     else:
        messages.success(request,'Not Data Fatch')
        return render(request,'docverify.html') 
     
def document_Verified(request):
     user_email=request.session.get('studentid')
     user=tbl_student.objects.filter(email=user_email).first()
     if user.form_status=="Approve":
         sh=tbl_student.objects.all()
         return render(request,'docverified.html',{'sh':sh}) 
     else:
        messages.success(request,'Not Data Fatch')
        return render(request,'docverified.html') 
        
        
         
     
        
   
    

