from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.contrib import messages
from django.views.generic import ListView,DetailView
# Create your views here.
def index(request):
    job=Job.objects.all().order_by('-start_date')
    d={'job':job[:2]}
    return render(request, "index.html",d)

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
   
    d={'job':job,'len1':len1,'len2':len2,'len3':len3,'len4':len4,'len5':len5,'len6':len6,'len7':len7,'len8':len8,'recruiter':recruiter}
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
        l=request.FILES["logo"]
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
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,salary=s,image=l,description=description,experience=e,location=location,skills=skills,creationdate=date.today(),nature=nature,vacancy=vacancy,category=category)
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
    li=[]
    for  i in data:
        li.append(i.job.id)
    d={'job':job,'li':li,'len1':len1,'len2':len2,'len3':len3,'len4':len4,'len5':len5,'len6':len6,'len7':len7,'len8':len8,'recruiter':recruiter}
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
    else:
      if request.method=="POST":
        cl=request.FILES["resume"]
        p=request.POST['portifolio']
        cover=request.POST['coverletter']
        
        Apply.objects.create(job=job,student=student,resume=cl,applydate=date1,portifolio_website=p,coverletter=cover)
        job.vacancy-=1
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
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Customer Service")
    d={'job':job,'li':li}
    return render(request, "Customer_Service.html",d)

def Human_Resource(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Human Resource")
    d={'job':job,'li':li}
    return render(request, "Human_Resource.html",d)

def Project_Management(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Project Management")
    d={'job':job,'li':li}
    return render(request, "Project_Management.html",d)

def Bussiness_Development(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Bussiness Development")
    d={'job':job,'li':li}

    return render(request, "Bussiness_Development.html",d)

def Human_Resource(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Sales & Communication")
    d={'job':job,'li':li}
    return render(request, "Sales_and_Communication.html",d)


def Teaching_and_Education(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Teaching & Education")
    d={'job':job,'li':li}
    return render(request, "Teaching_and_Education.html",d)

def Design_and_Creative(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Design & Creative")
    d={'job':job,'li':li}
    return render(request, "Design_and_Creative.html",d)

def Sales_and_Communication(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for  i in data:
        li.append(i.job.id)
    job=Job.objects.filter(category="Sales & Communication")
    d={'job':job,'li':li}
    return render(request, "Sales_and_Communication.html",d)
# Category end

#def error_404_view(request,exception):
  # return render(request,"404.html")

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