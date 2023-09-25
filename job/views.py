from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
import pdfkit
from django.utils.crypto import get_random_string





# Create your views here.
def index(request):
    job=Job.objects.all().order_by('-start_date')
    d={'job':job[:2]}
    return render(request, "index.html",d)

def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        try:
            user = User.objects.get(username=username)
             # Generate a new password
            new_password = get_random_string(length=12)
            user.set_password(new_password)
            user.save()
            # Send email notification
            send_mail('Password Reset Request',f'Your new password is: {new_password}',settings.EMAIL_HOST_USER,[username,],fail_silently=False,)
            return redirect('password_reset_done')
        except:
            messages.error(request, 'No user found with that email address.')
            return redirect('forget_password')
    return render(request, 'forget_password.html')

def password_reset_done(request):
    return render(request,"password_reset_done.html")

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
             u.set_password(n)
             u.save()   
             error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,"change_passwordadmin.html",d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
             u.set_password(n)
             u.save()   
             error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,"change_passworduser.html",d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
             u.set_password(n)
             u.save()   
             error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,"change_passwordrecruiter.html",d)

def admin_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        
        try:

            if user.is_staff:
                 login(request,user)
                 error="no"
            else:
                    error="yes"
        except:
                error="yes"
        
    d={'error':error}
    return render(request,"admin_login.html",d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount=Recruiter.objects.all().count
    scount=StudentUser.objects.all().count
    d={'rcount':rcount,'scount':scount}
    return render(request,"admin_home.html",d)

def Logout(request):
    logout(request)
    return redirect('index')

def contact(request):
    return render(request,"contact.html")

def services(request):
    return render(request,"services.html")

def latest_jobs(request):
    job=Job.objects.all().order_by('-start_date')
    category1=Job.objects.filter(category="Marketing")
    category2=Job.objects.filter(category="Customer Service")
    category3=Job.objects.filter(category="Human Resource")
    category4=Job.objects.filter(category="Project Management")
    category5=Job.objects.filter(category="Business Development")
    category6=Job.objects.filter(category="Sales & Communication")
    category7=Job.objects.filter(category="Teaching & Education")
    category8=Job.objects.filter(category="Design & Creative")
    len1=0
    len2=0
    len3=0
    len4=0
    len5=0
    len6=0
    len7=0
    len8=0
    for i in category1:
         len1+=i.vacancy
    for i in category2:
         len2+=i.vacancy
    for i in category3:
         len3+=i.vacancy
    for i in category4:
         len4+=i.vacancy
    for i in category5:
         len5+=i.vacancy
    for i in category6:
         len6+=i.vacancy
    for i in category7:
         len7+=i.vacancy
    for i in category8:
         len8+=i.vacancy
    
    recruiter=Recruiter.objects.all()
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1 and i.vacancy>0):
            valid.append(i)
    d={'valid':valid,'len1':len1,'len2':len2,'len3':len3,'len4':len4,'len5':len5,'len6':len6,'len7':len7,'len8':len8,'recruiter':recruiter}
    return render(request,"latest_jobs.html",d)

def user_signup(request):
    error=""
    if request.method=='POST':
     try:
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        company=request.POST['company']
        company_detail=request.POST['detail']
        user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
        Recruiter.objects.create(user=user,mobile=con,image=i,gender=gen,company=company,company_detail=company_detail,type="recruiter",status="pending")
        subject = 'welcome to GurageJobs'
        message = f'Hi {user.username}, thank you for registering in GurageJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.username, ]
        send_mail( subject, message, email_from, recipient_list)
        error="no"
        d={'error':error}
        return render(request,"user_signup.html",d)
     except:
            error="yes"
     try:
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
        StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student")
        subject = 'welcome to GurageJobs'
        message = f'Hi {user.username}, thank you for registering in GurageJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.username, ]
        send_mail( subject, message, email_from, recipient_list)
        error="no"
     except:
            error="yes"
    d={'error':error}
    return render(request,"user_signup.html",d)

def recruiter_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        company=request.POST['company']
        company_detail=request.POST['detail']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            Recruiter.objects.create(user=user,mobile=con,image=i,gender=gen,company=company,company_detail=company_detail,type="recruiter",status="pending")
            error="no"
        except:
            error="yes"
            
    d={'error':error}
    return render(request,"recruiter_signup.html",d)


def user_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                login(request,user)
                error="sno"
                d={'error':error}
                return render(request,"user_login.html",d)
            except:
                error="yes"
            
            try:
                user1=Recruiter.objects.get(user=user)
                if  user1.status=="Accept" :
                 login(request,user)
                 error="rno"

                elif  user1.status=="Reject":
                    error="not"
                else:
                    error="pending"
                d={'error':error}
                return render(request,"user_login.html",d)
            except:
                error="yes"
            
            try:

             if user.is_staff:
                 login(request,user)
                 error="ano"
             else:
                    error="yes"
            except:
                error="yes"

        else:
            error="yes"
    d={'error':error}
    return render(request,"user_login.html",d)

def recruiter_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=Recruiter.objects.get(user=user)
                if user1.type=="recruiter" and  user1.status=="Accept" :
                 login(request,user)
                 error="no"
                elif user1.type=="recruiter" and  user1.status=="Reject":
                    error="not"
                else:
                    error="pending"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,"recruiter_login.html",d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
        try:
            image=request.FILES['image']
            student.image=image
            student.save()
        except:
            pass
    d={'student':student,'error':error}
    return render(request,"user_home.html",d)

def about(request):
    return render(request,"about.html")

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con
        recruiter.gender=gen
        
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
        try:
            image=request.FILES['image']
            recruiter.image=image
            recruiter.save()
        except:
            pass

    d={'recruiter':recruiter,'error':error}
    return render(request,"recruiter_home.html",d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        jt=request.POST["jobtitle"]
        sd=request.POST["startdate"]
        ed=request.POST["enddate"]
        s=request.POST["salary"]
        e=request.POST["experience"]
        location=request.POST["location"]
        skills=request.POST["skills"]
        description=request.POST["description"]
        nature=request.POST["nature"]
        vacancy=request.POST["vacancy"]
        category=request.POST["category"]
        user=request.user
        recruiter=Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,salary=s,description=description,experience=e,location=location,skills=skills,creationdate=date.today(),nature=nature,vacancy=vacancy,category=category)
            subject = 'Exciting new role available within the'+recruiter.company
            message = f'An exciting opportunity is now open within the {recruiter.company} for a {jt}.We are asking you to apply directly to the HR department before the role is advertised on external job boards.The role of {jt} will require the following skills {skills} and would be suitable for team members holding the following {description}.We are hoping to start interviews on {ed} and would encourage interested applicants to have expressed their interest by {StudentUser}. To do so, please complete an internal application form and send it to the HR department.We encourage all suitably qualified and interested team members to apply for this exciting position. For further information or details please contact us on {recruiter.user.username}.'
            email_from = settings.EMAIL_HOST_USER
            data=StudentUser.objects.all()
            recipient_list = []
            for i in data:
                recipient_list.append(i.user.username)
            send_mail( subject, message, email_from, recipient_list)
            error="no"
        except:
            error="yes"
    d={'error':error}
    
    return render(request,"add_job.html",d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,"job_list.html",d)

def user_latestjobs(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    date1=date.today()
    category1=Job.objects.filter(category="Marketing")
    category2=Job.objects.filter(category="Customer Service")
    category3=Job.objects.filter(category="Human Resource")
    category4=Job.objects.filter(category="Project Management")
    category5=Job.objects.filter(category="Business Development")
    category6=Job.objects.filter(category="Sales & Communication")
    category7=Job.objects.filter(category="Teaching & Education")
    category8=Job.objects.filter(category="Design & Creative")
    len1=0
    len2=0
    len3=0
    len4=0
    len5=0
    len6=0
    len7=0
    len8=0
    for i in category1:
         len1+=i.vacancy
    for i in category2:
         len2+=i.vacancy
    for i in category3:
         len3+=i.vacancy
    for i in category4:
         len4+=i.vacancy
    for i in category5:
         len5+=i.vacancy
    for i in category6:
         len6+=i.vacancy
    for i in category7:
         len7+=i.vacancy
    for i in category8:
         len8+=i.vacancy
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    recruiter=Recruiter.objects.all()
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1 and i.vacancy>0):
            valid.append(i)
    li=[]
    for  i in data:
        li.append(i.job.id)
    d={'valid':valid,'li':li,'len1':len1,'len2':len2,'len3':len3,'len4':len4,'len5':len5,'len6':len6,'len7':len7,'len8':len8,'recruiter':recruiter,'date1':date1}
    return render(request,"user_latestjobs.html",d)

def job_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date<date1:
        error="close"
    elif job.start_date>date1:
        error="notopen"
    elif job.vacancy==0:
        error="novacancy"
    else:
      if request.method=="POST":
        cl=request.FILES["resume"]
        p=request.POST['portifolio']
        cover=request.POST['coverletter']
        
        Apply.objects.create(job=job,student=student,resume=cl,applydate=date1,portifolio_website=p,coverletter=cover)
        job.vacancy=max(0,job.vacancy-1)
        job.save()
        error="done"
    d={'error':error,'student':student,'job':job}
    return render(request,"job_detail.html",d)

def application_success(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request, "application_success.html",d)


def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=Recruiter.objects.get(id=pid)
    error=""
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,"change_status.html",d)


#category start
def marketing(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Marketing")
    d={'job':job,'li':li}
    return render(request, "marketing.html",d)


def Customer_Service(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Customer Service")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Customer_Service.html",d)

def Human_Resource(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Human Resource")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Human_Resource.html",d)

def Project_Management(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Project Management")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Project_Management.html",d)

def Bussiness_Development(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Bussiness Development")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Bussiness_Development.html",d)


def Teaching_and_Education(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Teaching & Education")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Teaching_and_Education.html",d)

def Design_and_Creative(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Design & Creative")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Design_and_Creative.html",d)

def Sales_and_Communication(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Sales & Communication")
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date<=date1 and i.end_date>=date1):
            valid.append(i)
    d={'valid':valid,'li':li}
    return render(request, "Sales_and_Communication.html",d)
# Category end

# def error_404_view(request,exception):
#   return render(request,"404.html")

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,"recruiter_all.html",d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=Recruiter.objects.get(id=pid)
    error=""
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,"change_status.html",d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('recruiter_all')


def joblist_companies(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    recruiter=Recruiter.objects.get(id=pid)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job ,'recruiter':recruiter}
    return render(request, "joblist_companies.html",d)

class BlogSearchView(ListView):
    model=Job
    template_name="user_latestjobs.html"
    context_object_name='posts'


    def  get_queryset(self):
        query=self.request.GET.get('q')
        return Job.objects.filter(title__icontains=query).order_by('-start_date')

def delete_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    job=Job.objects.get(id=pid)
    job.delete()
    return redirect('job_list')

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,"view_users.html",d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=Apply.objects.all()
    d={'data':data}
    return render(request,"applied_candidatelist.html",d)

def build_cv(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    profile_id=None
    user=request.user
    if request.method=="POST":
        degree=request.POST["degree"]
        university=request.POST["university"]
        about_you=request.POST["about_you"]
        languages=request.POST["languages"]
        e=request.POST["experience"]
        skills=request.POST["skills"]
        
        
        try:
            profile=Profile.objects.create(degree=degree,university=university,skills=skills,experience=e,languages=languages,about_you=about_you)
            profile_id=profile.id
            error="no"
        except:
            error="yes"
    d={"error":error,"profile_id":profile_id,"user":user}
    return render(request,"build_cv.html",d)


def resume(request,pid):
    user_profile=Profile.objects.get(id=pid)
    return render(request,"resume.html",{'user_profile':user_profile})

def privacy_policy(request):
   return render(request,'privacy_policy.html')



def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)

    if request.method=="POST":
        jt=request.POST["jobtitle"]
        sd=request.POST["startdate"]
        ed=request.POST["enddate"]
        s=request.POST["salary"]
        e=request.POST["experience"]
        location=request.POST["location"]
        skills=request.POST["skills"]
        description=request.POST["description"]
        vacancy=request.POST['vacancy']
        nature=request.POST['nature']
        category=request.POST['category']
        job.title=jt
        job.salary=s
        job.experience=e
        job.location=location
        job.skills=skills
        job.description=description
        job.vacancy=vacancy
        job.nature=nature
        job.category=category
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        else:
            pass

        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass
        else:
            pass
    d={'error':error,'job':job}
    
    return render(request,"edit_jobdetail.html",d)


def upcoming_jobs(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    job=Job.objects.all().order_by('-start_date')
    date1=date.today()
    recruiter=Recruiter.objects.all()
    valid=[]
    date1=date.today()
    for i in job:
        if (i.start_date>date1):
            valid.append(i)
    d={'valid':valid,'recruiter':recruiter}
    return render(request,"upcoming_jobs.html",d)


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
        try:
            image=request.FILES['image']
            student.image=image
            student.save()
        except:
            pass
    d={'student':student,'error':error}
    return render(request,"edit_profile.html",d)


def edit_profilerecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        detail=request.POST['detail']
        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con
        recruiter.gender=gen
        recruiter.company_detail=detail
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
        try:
            image=request.FILES['image']
            recruiter.image=image
            recruiter.save()
        except:
            pass

    d={'recruiter':recruiter,'error':error}
    return render(request,"edit_profilerecruiter.html",d)


def email_setting(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
       user=request.user
       try:
        category=request.POST["category"]
        Email.objects.create(email=user.username,category=category)
        error="no"
       except:
        error="yes"
    d={'error':error}
    return render(request,"email_setting.html",d)
    