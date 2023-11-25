from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from users.models import CustomUser
import re
from django.contrib import messages
from .utils import send_sms,whatsapp
from codes.forms import CodeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from users.forms import *
from users.models import *
import openpyxl
import pandas as pd
# model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View

from django.contrib.auth import logout

from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
import csv
def logout_view(request):
    logout(request)
    return redirect('authenticate-view')

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None



def ViewPDF(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        data={
            'class':'PYTHON CLASS',
            'students':Python.objects.all(),
    
        }
        pdf=render_to_pdf('pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')
    elif user.unit=='sql':
        data={
            'class':'SQL CLASS',
            'students':Sql.objects.all(),
    
        }
        pdf=render_to_pdf('pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')
    elif user.unit=='javascript':
        data={
            'class':'JS CLASS',
            'students':Javascript.objects.all(),
    
        }
        pdf=render_to_pdf('pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')
    elif user.unit=='php':
        data={
            'class':'PHP CLASS',
            'students':Php.objects.all(),
    
        }
        pdf=render_to_pdf('pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')



def downloadPDF(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        data={
            'class':'PYTHON CLASS',
            'students':Python.objects.all(),
    
        }
        pdf = render_to_pdf('pdf.html',data)

        response=HttpResponse(pdf,content_type='application/pdf')
        filename="Python_%s.pdf"%("12341231")
        content="attachment; filename='%s'"%(filename)
        response['Content-Disposition']=content
        return response
    elif user.unit=='javascript':
        data={
            'class':'JS CLASS',
            'students':Javascript.objects.all(),
    
        }
        pdf = render_to_pdf('pdf.html',data)

        response=HttpResponse(pdf,content_type='application/pdf')
        filename="JS_%s.pdf"%("12341231")
        content="attachment; filename='%s'"%(filename)
        response['Content-Disposition']=content
        return response
    elif user.unit=='sql':
        data={
            'class':'SQL CLASS',
            'students':Sql.objects.all(),
    
        }
        pdf = render_to_pdf('pdf.html',data)

        response=HttpResponse(pdf,content_type='application/pdf')
        filename="Sql_%s.pdf"%("12341231")
        content="attachment; filename='%s'"%(filename)
        response['Content-Disposition']=content
        return response
    elif user.unit=='php':
        data={
            'class':'PHP CLASS',
            'students':Php.objects.all(),
    
        }
        pdf = render_to_pdf('pdf.html',data)

        response=HttpResponse(pdf,content_type='application/pdf')
        filename="Php_%s.pdf"%("12341231")
        content="attachment; filename='%s'"%(filename)
        response['Content-Disposition']=content
        return response

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        un = request.POST['unit']
        unit=un.lower()
        phone=request.POST['phonenumber']
        email=request.POST['email']
        pl = len(password)
        reg=re.compile('[@_!#$%^&*()~:/\|]')

        if password == password2:
           
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return render(request, 'register.html')
            elif(pl < 8):
                messages.info(request, 'password must be 8 or more characters')
                return render(request, 'register.html')
            elif reg.search(password)==None:
                messages.info(request, 'password must contain special characters eg. @ # $')
                return render(request, 'register.html')
            elif len(phone)>10 or len(phone)<10:
                messages.info(request, 'Phone number must be atleast 10 and atmost 10 numbers')
                return render(request, 'register.html')
            elif unit !='python' or unit!='javascript' or unit!='sql' or unit!='php' or unit!='':
                messages.info(request, 'For units, choose Python, Javascript, PHP,Sql or leave a blank space')
                return render(request, 'register.html')

            else:
                replacement='+254'
                phone=phone.replace(phone[0], replacement, 1)
                user = CustomUser.objects.create_user(
                    username=username, password=password,phone_number=phone,unit=unit,email=email)
                user.save()
                return redirect('home-view')

        else:
            messages.info(request, 'Password not the same')
            return render(request, 'register.html')


    else:
        return render(request, 'register.html')

def authenticate_view(request):
    form=AuthenticationForm()
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk']=user.pk
            return redirect('verify-view')
        messages.info(request, 'Invalid credentials')
    return render(request, 'auth.html',{'form':form})
def verify_view(request):
    form=CodeForm(request.POST or None)
    pk=request.session.get('pk')
    if pk:
        user=CustomUser.objects.get(pk=pk)
        code=user.code
        code_user=f"{user.username}: {user.code}"
        if not request.POST:
            print(code_user)
            # send_sms(code_user, user.phone_number)
        if form.is_valid():
            num=form.cleaned_data.get('number')
            if str(code)==num:
                code.save()
                # login(request, user)
                # un=request.user.username
                # print(un)
                # if un=='tom':
                
                request.session['pk']=user.pk
                return redirect('home-view')
            else:
                messages.info(request, 'Invalid code. Login again.')
                return redirect('authenticate-view')
    return render(request,'verify.html',{'form':form})

def home_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    print(user)
    if user.username=='admin':
        context={
            'user':user,
            'pythonfail':Python.objects.filter(prediction='FAIL').count(),
            'jsfail':Javascript.objects.filter(prediction='FAIL').count(),
            'sqlfail':Sql.objects.filter(prediction='FAIL').count(),
            'phpfail':Php.objects.filter(prediction='FAIL').count(),
            'students':Students.objects.all().count(),
            'users':CustomUser.objects.all().count(),
            'staff':CustomUser.objects.filter(username__startswith='lecturer'),
            'staffcount':CustomUser.objects.filter(username__startswith='lecturer').count()
        }
        return render(request,'admin.html',context)
    elif user.username=='System admin':
        context={
            'user':user,
            'pythonfail':Python.objects.filter(prediction='FAIL').count(),
            'jsfail':Javascript.objects.filter(prediction='FAIL').count(),
            'sqlfail':Sql.objects.filter(prediction='FAIL').count(),
            'phpfail':Php.objects.filter(prediction='FAIL').count(),
            'students':Students.objects.all().count(),
            'users':CustomUser.objects.all().count(),
        }
        return render(request,'system.html',context)
    elif user.username.endswith('student'):
        print(str(pk)+'here########')
        us=str(user)
        name2=us[:-8]
        student=Students.objects.get(name=name2)
        context={
            'python':'NULL',
            'js':'NULL',
            'sql':'NULL',
            'php':'NULL',
            'student':student
        }
        for unit in student.units.all():
            if unit.pk==1:
                context['python']=Python.objects.get(reg=student.pk)
                # units.append(Python.objects.get(reg=student.pk))
            elif unit.pk==2:
                context['php']=Php.objects.get(reg=student.pk)
                # units.append(Php.objects.get(reg=student.pk))
            elif unit.pk==3:
                context['js']=Javascript.objects.get(reg=student.pk)
                # units.append(Javascript.objects.get(reg=student.pk))
            elif unit.pk==4:
                context['sql']=Sql.objects.get(reg=student.pk)
                # units.append(Sql.objects.get(reg=student.pk))
               
                
                
        # print(units)
        # print(context)
      
        
        
       
        return render(request,'student.html',context)
    elif user.unit=='python':
        if request.method=='POST':
            data=request.FILES['excel_file']
            
            dataframe1 = pd.read_excel(data)
            # print(dataframe1)
            d=dataframe1.iloc[0,0]
            print(d)
            tt=Python.objects.all()
            for ob in tt:
                print(ob.pk)
            

            
            for x in range(0,len(dataframe1)):
                reg=dataframe1.iloc[x,0]
                cat1=dataframe1.iloc[x,1]
                cat2=dataframe1.iloc[x,2]
                cat3=dataframe1.iloc[x,3]
                days=dataframe1.iloc[x,4]
                a=Python.objects.get(pk=reg)
                a.cat1=cat1
                a.cat2=cat2
                a.cat3=cat3
                a.days=days
                a.save()
                
            
            
            pythonstudents=Python.objects.all()
            
            context={
                'class':'Python class',
                'students':pythonstudents
                
                

            }
            return render(request,'attendance.html',context)
                # return redirect('attendance-view')

        # if request.user.username=="tom":
        #     context={'class':'Python class'}
        #     return render(request,'attendance.html',context)
        else:
            context={
                'class':'Python class',
                
            }
            
            return render(request,'attendance.html',context)
    elif user.unit=='php':
        if request.method=='POST':
            data=request.FILES['excel_file']
          
            dataframe1 = pd.read_excel(data)
            
            # print(dataframe1)
            d=dataframe1.iloc[0,0]
            print(d)
            tt=Php.objects.all()
            for ob in tt:
                print(ob.pk)
            

            
            for x in range(0,len(dataframe1)):
                reg=dataframe1.iloc[x,0]
                cat1=dataframe1.iloc[x,1]
                cat2=dataframe1.iloc[x,2]
                cat3=dataframe1.iloc[x,3]
                days=dataframe1.iloc[x,4]
                a=Php.objects.get(pk=reg)
                a.cat1=cat1
                a.cat2=cat2
                a.cat3=cat3
                a.days=days
                a.save()
                
            
            
            phpstudents=Php.objects.all()
            
            context={
                'class':'PHP class',
                'students':phpstudents
                
                

            }
            return render(request,'attendance.html',context)
                # return redirect('attendance-view')

        # if request.user.username=="tom":
        #     context={'class':'Python class'}
        #     return render(request,'attendance.html',context)
        else:
            context={
                'class':'PHP class',
                
            }
            
            return render(request,'attendance.html',context)
    elif user.unit=='javascript':
        if request.method=='POST':
            data=request.FILES['excel_file']
           
            dataframe1 = pd.read_excel(data)
            # print(dataframe1)
            d=dataframe1.iloc[0,0]
            print(d)
            tt=Javascript.objects.all()
            for ob in tt:
                print(ob.pk)
            

            
            for x in range(0,len(dataframe1)):
                reg=dataframe1.iloc[x,0]
                cat1=dataframe1.iloc[x,1]
                cat2=dataframe1.iloc[x,2]
                cat3=dataframe1.iloc[x,3]
                days=dataframe1.iloc[x,4]
                a=Javascript.objects.get(pk=reg)
                a.cat1=cat1
                a.cat2=cat2
                a.cat3=cat3
                a.days=days
                a.save()
                
            
            
            jsstudents=Javascript.objects.all()
            
            context={
                'class':'JavaScript class',
                'students':jsstudents
                
                

            }
            return render(request,'attendance.html',context)
                # return redirect('attendance-view')

        # if request.user.username=="tom":
        #     context={'class':'Python class'}
        #     return render(request,'attendance.html',context)
        else:
            context={
                'class':'Javascript class',
                
            }
            
            return render(request,'attendance.html',context)
    elif user.unit=='sql':
        if request.method=='POST':
            data=request.FILES['excel_file']
            
            dataframe1 = pd.read_excel(data)
            # print(dataframe1)
            d=dataframe1.iloc[0,0]
            print(d)
            tt=Sql.objects.all()
            for ob in tt:
                print(ob.pk)
            

            
            for x in range(0,len(dataframe1)):
                reg=dataframe1.iloc[x,0]
                cat1=dataframe1.iloc[x,1]
                cat2=dataframe1.iloc[x,2]
                cat3=dataframe1.iloc[x,3]
                days=dataframe1.iloc[x,4]
                a=Sql.objects.get(pk=reg)
                a.cat1=cat1
                a.cat2=cat2
                a.cat3=cat3
                a.days=days
                a.save()
                
            
            
            sqlstudents=Sql.objects.all()
            
            context={
                'class':'SQL class',
                'students':sqlstudents
                
                

            }
            return render(request,'attendance.html',context)
            # return redirect('attendance-view')

        # if request.user.username=="tom":
        #     context={'class':'Python class'}
        #     return render(request,'attendance.html',context)
        else:
            context={
                'class':'SQL class',
                
            }
            
            return render(request,'attendance.html',context)
    

    python=Students.objects.filter(units__name__startswith="Python").count()
    # java=Students.objects.filter(units__name__startswith="java").count()
    javascript=Students.objects.filter(units__name__startswith="JavaScript").count()
    php=Students.objects.filter(units__name__startswith="PHP").count()
    sql=Students.objects.filter(units__name__startswith="SQL").count()
    l=[python,javascript,php,sql]
    

    students=Students.objects.all()
    for s in students:
        print(s.units.all())
        
    
    
    if request.method=="POST":
        form=studentsForm(request.POST)
        if form.is_valid():
            global name
            
            name=form['name'].value()
            phone=form['phone_no'].value()
            ss=Students.objects.filter(name=name).count()
            if ss==1:
                messages.info(request, 'Name Exists. Provide a different one.')
                return redirect('home-view')

            form.save()
            ss=Students.objects.get(name=name)
            studentPassword=str(Students.objects.get(name=name).pk)
            studentEmail=ss.email
            print(name)
            replacement='+254'
            phone=phone.replace(phone[0], replacement, 1)
            user = CustomUser.objects.create_user(
                    username=name+'-student', password=studentPassword,email=studentEmail,phone_number=phone)
            user.save()
            for unit in ss.units.all():
                if unit.id==1:
                    p=Python(name=Students.objects.get(name=name))
                    p.reg=Students.objects.get(name=name).pk
                    p.save()
                  
                    
                
                elif unit.id==2:
                    ph=Php(name=Students.objects.get(name=name))
                    ph.reg=Students.objects.get(name=name).pk
                    ph.save()
                    
                elif unit.id==3:
                    js=Javascript(name=Students.objects.get(name=name))
                    js.reg=Students.objects.get(name=name).pk
                    js.save()
                    
                elif unit.id==4:
                    s=Sql(name=Students.objects.get(name=name))
                    s.reg=Students.objects.get(name=name).pk
                    s.save()
                    
            reg=str(Students.objects.get(name=name).pk)
            print(reg)
            messages.info(request, "Registration number: "+reg)
            return redirect('home-view')
    else:
        form=studentsForm
    # print(Students.objects.get(name='Thomas').pk)
    total=Students.objects.all().count()
    context={
        'units':l,
        'form':form,
        'all':total
      
    }
       
    # id_profile = Attendance.objects.get(name =1)
    # print(id_profile.name)
    return render(request,'home.html',context)
    
def allstudents_view(request):
    students=Students.objects.all()
    context={'students':students}
    return render(request,'allstudents.html',context)
def deletestudent(request, pk):
    return render(request,'allstudents.html')
# def attendance_view(request):
#     pk=request.session.get('pk')
#     print(pk)
#     user=CustomUser.objects.get(pk=pk)
#     print(user)
#     if user.unit=='python':
#         if request.method=='POST':
#             data=request.FILES['excel_file']
            
#             dataframe1 = pd.read_excel(data)
#             # print(dataframe1)
#             d=dataframe1.iloc[0,0]
#             print(d)
#             tt=Python.objects.all()
#             for ob in tt:
#                 print(ob.pk)
            

            
#             for x in range(0,len(dataframe1)):
#                 reg=dataframe1.iloc[x,0]
#                 cat1=dataframe1.iloc[x,1]
#                 cat2=dataframe1.iloc[x,2]
#                 cat3=dataframe1.iloc[x,3]
#                 days=dataframe1.iloc[x,4]
#                 a=Python.objects.get(pk=reg)
#                 a.cat1=cat1
#                 a.cat2=cat2
#                 a.cat3=cat3
#                 a.days=days
#                 a.save()
                
            
            
#             pythonstudents=Python.objects.all()
            
#             context={
#                 'class':'Python class',
#                 'students':pythonstudents
                
                

#             }
#             return render(request,'attendance.html',context)
#                 # return redirect('attendance-view')

#         # if request.user.username=="tom":
#         #     context={'class':'Python class'}
#         #     return render(request,'attendance.html',context)
#         else:
#             context={
#                 'class':'Python class',
                
#             }
            
#             return render(request,'attendance.html',context)
#     elif user.unit=='php':
#         if request.method=='POST':
#             data=request.FILES['excel_file']
          
#             dataframe1 = pd.read_excel(data)
            
#             # print(dataframe1)
#             d=dataframe1.iloc[0,0]
#             print(d)
#             tt=Php.objects.all()
#             for ob in tt:
#                 print(ob.pk)
            

            
#             for x in range(0,len(dataframe1)):
#                 reg=dataframe1.iloc[x,0]
#                 cat1=dataframe1.iloc[x,1]
#                 cat2=dataframe1.iloc[x,2]
#                 cat3=dataframe1.iloc[x,3]
#                 days=dataframe1.iloc[x,4]
#                 a=Php.objects.get(pk=reg)
#                 a.cat1=cat1
#                 a.cat2=cat2
#                 a.cat3=cat3
#                 a.days=days
#                 a.save()
                
            
            
#             phpstudents=Php.objects.all()
            
#             context={
#                 'class':'PHP class',
#                 'students':phpstudents
                
                

#             }
#             return render(request,'attendance.html',context)
#                 # return redirect('attendance-view')

#         # if request.user.username=="tom":
#         #     context={'class':'Python class'}
#         #     return render(request,'attendance.html',context)
#         else:
#             context={
#                 'class':'PHP class',
                
#             }
            
#             return render(request,'attendance.html',context)
#     elif user.unit=='javascript':
#         if request.method=='POST':
#             data=request.FILES['excel_file']
           
#             dataframe1 = pd.read_excel(data)
#             # print(dataframe1)
#             d=dataframe1.iloc[0,0]
#             print(d)
#             tt=Javascript.objects.all()
#             for ob in tt:
#                 print(ob.pk)
            

            
#             for x in range(0,len(dataframe1)):
#                 reg=dataframe1.iloc[x,0]
#                 cat1=dataframe1.iloc[x,1]
#                 cat2=dataframe1.iloc[x,2]
#                 cat3=dataframe1.iloc[x,3]
#                 days=dataframe1.iloc[x,4]
#                 a=Javascript.objects.get(pk=reg)
#                 a.cat1=cat1
#                 a.cat2=cat2
#                 a.cat3=cat3
#                 a.days=days
#                 a.save()
                
            
            
#             jsstudents=Javascript.objects.all()
            
#             context={
#                 'class':'JavaScript class',
#                 'students':jsstudents
                
                

#             }
#             return render(request,'attendance.html',context)
#                 # return redirect('attendance-view')

#         # if request.user.username=="tom":
#         #     context={'class':'Python class'}
#         #     return render(request,'attendance.html',context)
#         else:
#             context={
#                 'class':'Javascript class',
                
#             }
            
#             return render(request,'attendance.html',context)
#     elif user.unit=='sql':
#         if request.method=='POST':
#             data=request.FILES['excel_file']
            
#             dataframe1 = pd.read_excel(data)
#             # print(dataframe1)
#             d=dataframe1.iloc[0,0]
#             print(d)
#             tt=Sql.objects.all()
#             for ob in tt:
#                 print(ob.pk)
            

            
#             for x in range(0,len(dataframe1)):
#                 reg=dataframe1.iloc[x,0]
#                 cat1=dataframe1.iloc[x,1]
#                 cat2=dataframe1.iloc[x,2]
#                 cat3=dataframe1.iloc[x,3]
#                 days=dataframe1.iloc[x,4]
#                 a=Sql.objects.get(pk=reg)
#                 a.cat1=cat1
#                 a.cat2=cat2
#                 a.cat3=cat3
#                 a.days=days
#                 a.save()
                
            
            
#             sqlstudents=Sql.objects.all()
            
#             context={
#                 'class':'SQL class',
#                 'students':sqlstudents
                
                

#             }
#             return render(request,'attendance.html',context)
#             # return redirect('attendance-view')

#         # if request.user.username=="tom":
#         #     context={'class':'Python class'}
#         #     return render(request,'attendance.html',context)
#         else:
#             context={
#                 'class':'SQL class',
                
#             }
            
#             return render(request,'attendance.html',context)
#     else:
#         return render(request,'null.html')

def admin_view(request):
    return render(request,'admin.html')
def grades_view(request):
    # students=Results.objects.filter(python_marks__gt=0)
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='php':
        students=Php.objects.all()
    
        context={
            'students':students,
            'class':'PHP'
        }
        return render(request,'grades.html',context)
    elif user.unit=='python':
        students=Python.objects.all()
    
        context={
            'students':students,
            'class':'Python'
        }
        return render(request,'grades.html',context)
    elif user.unit=='javascript':
        students=Javascript.objects.all()
    
        context={
            'students':students,
            'class':'JavaScript'
        }
        return render(request,'grades.html',context)
    elif user.unit=='sql':
        students=Sql.objects.all()
    
        context={
            'students':students,
            'class':'Sql'
        }
        return render(request,'grades.html',context)
def model_view(request):
    data=pd.read_excel('datasets/dataset2.xlsx')
    target=[]
    for i in range(len(data)):
        target.append(data.iloc[i,4])
    print(target)
    data2=[]
    for i in range(len(data)):
        cat1=data.iloc[i,0]
        cat2=data.iloc[i,1] 
        cat3=data.iloc[i,2] 
        total=data.iloc[i,3] 
        data2.append([cat1,cat2,cat3,total])
    print(data2)
    X=data2
    Y=target
    clf=RandomForestClassifier()
    clf.fit(X,Y)
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)
    clf.fit(X_train,Y_train)
    print(clf.predict([[15,15,1,31]]))

    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        pstudents=Python.objects.all()
        for s in pstudents:
            data=[[s.cat1,s.cat2,s.cat3,s.total]]
            prediction=clf.predict(data)
            if prediction==1:
                s.prediction='FAIL'
                s.save()
            else:
                s.prediction='PASS'
                s.save()
        predicted=Python.objects.filter(prediction='FAIL')
        context={
            'predicted':predicted,
            'class':'Python fail list.'
        }
        


        return render(request,'model.html',context)
    elif user.unit=='php':
        phpstudents=Php.objects.all()
        for s in phpstudents:
            data=[[s.cat1,s.cat2,s.cat3,s.total]]
            prediction=clf.predict(data)
            if prediction==1:
                s.prediction='FAIL'
                s.save()
            else:
                s.prediction='PASS'
                s.save()
        predicted=Php.objects.filter(prediction='FAIL')
        context={
            'predicted':predicted,
            'class':'PHP fail list.'
        }
        


        return render(request,'model.html',context)
    elif user.unit=='javascript':
        jsstudents=Javascript.objects.all()
        for s in jsstudents:
            data=[[s.cat1,s.cat2,s.cat3,s.total]]
            prediction=clf.predict(data)
            if prediction==1:
                s.prediction='FAIL'
                s.save()
            else:
                s.prediction='PASS'
                s.save()
        predicted=Javascript.objects.filter(prediction='FAIL')
        context={
            'predicted':predicted,
            'class':'JavaScript fail list.'
        }
        


        return render(request,'model.html',context)
    elif user.unit=='sql':
        sqlstudents=Sql.objects.all()
        for s in sqlstudents:
            data=[[s.cat1,s.cat2,s.cat3,s.total]]
            prediction=clf.predict(data)
            if prediction==1:
                s.prediction='FAIL'
                s.save()
            else:
                s.prediction='PASS'
                s.save()
        predicted=Sql.objects.filter(prediction='FAIL')
        context={
            'predicted':predicted,
            'class':'SQL fail list.'
        }
        


        return render(request,'model.html',context)

def update_view(request,pk):
    queryset=Python.objects.get(pk=pk)
    form=studentsUpdateForm(instance=queryset)
    if request.method=='POST':
        form=studentsUpdateForm(request.POST,instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/grades/')
    context={'form':form}
    return render(request,'entry.html',context)
def admin_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    print(user)
    if user.username=='Ian':
        return render(request,'admin.html')
    else:
        return render(request,'access.html')

def staff(request):
    context={
        'staff':CustomUser.objects.all()
    }
    return render(request,'staff.html',context)
    
def deleteStaff(request, pk):
    pk2=request.session.get('pk')
    user=CustomUser.objects.get(pk=pk2)
    if user.username=='admin':
        if request.method=="POST":
            CustomUser.objects.get(pk=pk).delete()
            return redirect("/staffpage/")
        return render(request,'deletestaff2.html')
    else:
        if request.method=="POST":
            CustomUser.objects.get(pk=pk).delete()
            return redirect("/staff/")
        return render(request,'deletestaff.html')

def deleteStudent(request,pk):
    if request.method=="POST":
        Students.objects.get(pk=pk).delete()
        return redirect('/allstudents/')
    return render(request, "delete.html")
def failView(request, pk):
    pk2=request.session.get('pk')
    print(pk2)
    user=CustomUser.objects.get(pk=pk2)
    if user.unit=='python':
        student=Students.objects.get(pk=pk)
        clubs=student.clubs.count()
        studentpy=Python.objects.get(pk=pk)
        days=studentpy.days
        print(days)
        if days<30 and clubs>1:
            context={
                'class':'Python class Fail report.',
                'student':student,
                'message':'You need to attend more classes and drop some clubs for you to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
        else:
            context={
                'class':'Python class Fail report.',
                'student':student,
                'message':'You need to revise more to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
    elif user.unit=='javascript':
        student=Students.objects.get(pk=pk)
        clubs=student.clubs.count()
        studentjs=Javascript.objects.get(pk=pk)
        days=studentjs.days
        print(days)
        if days<30 and clubs>1:
            context={
                'class':'JavaScript class Fail report.',
                'student':student,
                'message':'You need to attend more classes and drop some clubs for you to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
        else:
            context={
                'class':'Javascript class Fail report.',
                'student':student,
                'message':'You need to revise more to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
    elif user.unit=='php':
        student=Students.objects.get(pk=pk)
        clubs=student.clubs.count()
        studentphp=Php.objects.get(pk=pk)
        days=studentphp.days
        print(days)
        if days<30 and clubs>1:
            context={
                'class':'Php class Fail report.',
                'student':student,
                'message':'You need to attend more classes and drop some clubs for you to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
        else:
            context={
                'class':'Php class Fail report.',
                'student':student,
                'message':'You need to revise more to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
    elif user.unit=='sql':
        student=Students.objects.get(pk=pk)
        clubs=student.clubs.count()
        studentsql=Sql.objects.get(pk=pk)
        days=studentsql.days
        print(days)
        if days<30 and clubs>1:
            message='Hello '+student.name+'. You need to attend more classes and drop some clubs to avoid failing your SQL final exam.'
            whatsapp(+254111330150,message)
            context={
                'class':'SQL class Fail report.',
                'student':student,
                'message':'You need to revise more to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
        else:
            
            context={
                'class':'SQL class Fail report.',
                'student':student,
                'message':'You need to revise more to avoid failing in the final exam'
            }
            return render(request,'fail.html',context)
def notifications_view(request):
    pk2=request.session.get('pk')
    user=CustomUser.objects.get(pk=pk2)
    if user.unit=='python':
        students=Python.objects.filter(prediction='FAIL')
        for student in students:
            st=Students.objects.get(pk=student.pk)
            clubs=st.clubs.count()
            if student.days<30 and clubs>1:
                subject = 'Python class fail report'
                message = 'Hello '+str(student.name)+'. You need to attend more classes and drop some clubs to avoid failing your python final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            elif student.days>30 and clubs>1:
                subject = 'Python class fail report'
                message = 'Hello '+str(student.name)+'. You need to  drop some clubs and revise more to avoid failing your python final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            else:
                subject = 'Python class fail report'
                message = 'Hello '+str(student.name)+'. You need to revise more to avoid failing your python final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
        return redirect('home-view')
    elif user.unit=='javascript':
        students=Javascript.objects.filter(prediction='FAIL')
        for student in students:
            st=Students.objects.get(pk=student.pk)
            clubs=st.clubs.count()
            if student.days<30 and clubs>1:
                subject = 'JavaScript class fail report'
                message = 'Hello '+str(student.name)+'. You need to attend more classes and drop some clubs to avoid failing your JS final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            elif student.days>30 and clubs>1:
                subject = 'JavaScript class fail report'
                message = 'Hello '+str(student.name)+'. You need to  drop some clubs and revise more to avoid failing your JS final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            else:
                subject = 'JavaScript class fail report'
                message = 'Hello '+str(student.name)+'. You need to revise more to avoid failing your JS final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
        return redirect('home-view')
    elif user.unit=='php':
        students=Php.objects.filter(prediction='FAIL')
        for student in students:
            st=Students.objects.get(pk=student.pk)
            clubs=st.clubs.count()
            if student.days<30 and clubs>1:
                subject = 'Php class fail report'
                message = 'Hello '+str(student.name)+'. You need to attend more classes and drop some clubs to avoid failing your Php final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            elif student.days>30 and clubs>1:
                subject = 'Php class fail report'
                message = 'Hello '+str(student.name)+'. You need to  drop some clubs and revise more to avoid failing your Php final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            else:
                subject = 'Php class fail report'
                message = 'Hello '+str(student.name)+'. You need to revise more to avoid failing your Php final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
        return redirect('home-view')
    elif user.unit=='sql':
        students=Sql.objects.filter(prediction='FAIL')
        for student in students:
            st=Students.objects.get(pk=student.pk)
            clubs=st.clubs.count()
            if student.days<30 and clubs>1:
                subject = 'SQL class fail report'
                message = 'Hello '+str(student.name)+'. You need to attend more classes and drop some clubs to avoid failing your SQL final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            elif student.days>30 and clubs>1:
                subject = 'SQL class fail report'
                message = 'Hello '+str(student.name)+'. You need to  drop some clubs and revise more to avoid failing your SQL final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
            else:
                subject = 'SQL class fail report'
                message = 'Hello '+str(student.name)+'. You need to revise more to avoid failing your SQL final exam.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [st.email]
                send_mail(subject, message, from_email,
                recipient_list, fail_silently=False)
        messages.info(request, "Notifications send successfully!: ")
        return redirect('home-view')
    
   
def uploadAttendance_view(request):

    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    form=pyattendaceForm
    form2=jsattendaceForm
    form3=sqlattendaceForm
    form4=phpattendaceForm
    if user.unit=='python':
        if request.method=="POST":
            form=pyattendaceForm(request.POST)
            if form.is_valid():
                name=form['name'].value()
                reg=form['reg'].value()
                
                if Python.objects.filter(pk=reg).count()==1 and str(Python.objects.get(pk=reg).name)==name:
                    form.save()
                    dic=pythonAttendance.objects.filter(name=name).aggregate(Sum('sumhrs'))
                    print(str(dic['sumhrs__sum'])+"$$$$$")
                    student=Python.objects.get(pk=reg)
                    student.hours=dic['sumhrs__sum']
                    student.save()
                    
                    return redirect('/updateattendance/')
                else:
                    messages.info(request, "Make sure the student belongs to this class.")
                    return redirect('/updateattendance/')
        context={
        'form':form,
        'students':Python.objects.all()
        }
        return render(request,'uattendance.html',context)
    if user.unit=='sql':
        if request.method=="POST":
            form=sqlattendaceForm(request.POST)
            if form.is_valid():
                name=form['name'].value()
                reg=form['reg'].value()
                
                if Sql.objects.filter(pk=reg).count()==1 and str(Sql.objects.get(pk=reg).name)==name:
                    form.save()
                    dic=sqlAttendance.objects.filter(name=name).aggregate(Sum('sumhrs'))
                    print(str(dic['sumhrs__sum'])+"$$$$$")
                    student=Sql.objects.get(pk=reg)
                    student.hours=dic['sumhrs__sum']
                    student.save()
                    
                    return redirect('/updateattendance/')
                else:
                    messages.info(request, "Make sure the student belongs to this class.")
                    return redirect('/updateattendance/')
        context={
        'form':form3,
        'students':Sql.objects.all()
        }
        return render(request,'uattendance.html',context)
    if user.unit=='javascript':
        if request.method=="POST":
            form=jsattendaceForm(request.POST)
            if form.is_valid():
                name=form['name'].value()
                reg=form['reg'].value()
                
                if Javascript.objects.filter(pk=reg).count()==1 and str(Javascript.objects.get(pk=reg).name)==name:
                    form.save()
                    dic=jsAttendance.objects.filter(name=name).aggregate(Sum('sumhrs'))
                    print(str(dic['sumhrs__sum'])+"$$$$$")
                    student=Javascript.objects.get(pk=reg)
                    student.hours=dic['sumhrs__sum']
                    student.save()
                    
                    return redirect('/updateattendance/')
                else:
                    messages.info(request, "Make sure the student belongs to this class.")
                    return redirect('/updateattendance/')
        context={
        'form':form2,
        'students':Javascript.objects.all()
        }
        return render(request,'uattendance.html',context)
    if user.unit=='php':
        if request.method=="POST":
            form=phpattendaceForm(request.POST)
            if form.is_valid():
                name=form['name'].value()
                reg=form['reg'].value()
                
                if Php.objects.filter(pk=reg).count()==1 and str(Php.objects.get(pk=reg).name)==name:
                    form.save()
                    dic=phpAttendance.objects.filter(name=name).aggregate(Sum('sumhrs'))
                    print(str(dic['sumhrs__sum'])+"$$$$$")
                    student=Php.objects.get(pk=reg)
                    student.hours=dic['sumhrs__sum']
                    student.save()
                    
                    return redirect('/updateattendance/')
                else:
                    messages.info(request, "Make sure the student belongs to this class.")
                    return redirect('/updateattendance/')
        context={
        'form':form4,
        'students':Php.objects.all()
        }
        return render(request,'uattendance.html',context)

    context={
        'form':form
    }
    return render(request,'uattendance.html',context)
def attendance_csv(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=pythonattendancesheet.csv'
        writer=csv.writer(response)
        students=Python.objects.all()
        writer.writerow(['Reg','Name','From','To','Signature'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='javascript':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=jsattendancesheet.csv'
        writer=csv.writer(response)
        students=Javascript.objects.all()
        writer.writerow(['Reg','Name','From','To','Signature'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='php':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=phpattendancesheet.csv'
        writer=csv.writer(response)
        students=Php.objects.all()
        writer.writerow(['Reg','Name','From','To','Signature'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='sql':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=sqlattendancesheet.csv'
        writer=csv.writer(response)
        students=Sql.objects.all()
        writer.writerow(['Reg','Name','From','To','Signature'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
def download_attendance(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=pythonattendance.csv'
        writer=csv.writer(response)
        students=Python.objects.all()
        writer.writerow(['Reg','Name','Days/Sem'])
        for student in students:
            writer.writerow([student.reg,student.name,student.hours])
        return response
    elif user.unit=='javascript':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=jsattendance.csv'
        writer=csv.writer(response)
        students=Javascript.objects.all()
        writer.writerow(['Reg','Name','Days/Sem'])
        for student in students:
            writer.writerow([student.reg,student.name,student.hours])
        return response
    elif user.unit=='sql':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=sqlattendance.csv'
        writer=csv.writer(response)
        students=Sql.objects.all()
        writer.writerow(['Reg','Name','Days/Sem'])
        for student in students:
            writer.writerow([student.reg,student.name,student.hours])
        return response
    elif user.unit=='php':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=phpattendance.csv'
        writer=csv.writer(response)
        students=Php.objects.all()
        writer.writerow(['Reg','Name','Days/Sem'])
        for student in students:
            writer.writerow([student.reg,student.name,student.hours])
        return response
def pyatt_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    name2=str(user)[:-8]
    print(name2)
    units=Students.objects.get(name=name2).units.all()
    # for u in units:
    #     if str(u)=='Python':
    #         print('@@@@@@@')
    if 'Python' in str(units):
        data=pythonAttendance.objects.filter(name=name2)
        context={
            'data':data,
            'lec':'Lecturer1',
            'classes':pythonAttendance.objects.filter(name=name2).count(),
            'absent':pythonAttendance.objects.filter(present='NO').count(),
            'subject':'Python'
        }
        return render(request,'pyatt.html',context)
    else:
         messages.info(request, "You are not part of the python class")
         return redirect('/home/')


    return render(request,'pyatt.html',context)
def jsatt_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    name2=str(user)[:-8]
    print(name2)
    units=Students.objects.get(name=name2).units.all()
    # for u in units:
    #     if str(u)=='Python':
    #         print('@@@@@@@')
    if 'JavaScript' in str(units):
        data=jsAttendance.objects.filter(name=name2)
        context={
            'data':data,
            'lec':'Lecturer2',
            'classes':jsAttendance.objects.filter(name=name2).count(),
            'absent':jsAttendance.objects.filter(present='NO').count(),
            'subject':'Javascript'
        }
        return render(request,'pyatt.html',context)
    else:
         messages.info(request, "You are not part of the JS class")
         return redirect('/home/')
def phpatt_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    name2=str(user)[:-8]
    print(name2)
    units=Students.objects.get(name=name2).units.all()
    # for u in units:
    #     if str(u)=='Python':
    #         print('@@@@@@@')
    if 'PHP' in str(units):
        data=phpAttendance.objects.filter(name=name2)
        context={
            'data':data,
            'lec':'Lecturer3',
            'classes':phpAttendance.objects.filter(name=name2).count(),
            'absent':phpAttendance.objects.filter(present='NO').count(),
            'subject':'PHP'
        }
        return render(request,'pyatt.html',context)
    else:
         messages.info(request, "You are not part of the PHP class")
         return redirect('/home/')

def sqlatt_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    name2=str(user)[:-8]
    print(name2)
    units=Students.objects.get(name=name2).units.all()
    # for u in units:
    #     if str(u)=='Python':
    #         print('@@@@@@@')
    if 'SQL' in str(units):
        data=sqlAttendance.objects.filter(name=name2)
        context={
            'data':data,
            'lec':'Lecturer4',
            'classes':sqlAttendance.objects.filter(name=name2).count(),
            'absent':sqlAttendance.objects.filter(present='NO').count(),
            'subject':'SQL'
        }
        return render(request,'pyatt.html',context)
    else:
         messages.info(request, "You are not part of the SQL class")
         return redirect('/home/')  
def downloadfail_view(request):
    pk=request.session.get('pk')
    print(pk)
    user=CustomUser.objects.get(pk=pk)
    if user.unit=='python':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=pythonFailList.csv'
        writer=csv.writer(response)
        students=Python.objects.filter(prediction='FAIL')
        writer.writerow(['Reg','Name'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='javascript':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=JSFailList.csv'
        writer=csv.writer(response)
        students=Javascript.objects.filter(prediction='FAIL')
        writer.writerow(['Reg','Name'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='sql':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=SQLFailList.csv'
        writer=csv.writer(response)
        students=Sql.objects.filter(prediction='FAIL')
        writer.writerow(['Reg','Name'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
    elif user.unit=='php':
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=PHPFailList.csv'
        writer=csv.writer(response)
        students=Php.objects.filter(prediction='FAIL')
        writer.writerow(['Reg','Name'])
        for student in students:
            writer.writerow([student.reg,student.name])
        return response
def staffpage_view(request):
    context={
        'staff':CustomUser.objects.filter(username__startswith='lecturer')
    }
    return render(request,'staffpage.html',context)