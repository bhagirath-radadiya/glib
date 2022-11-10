from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from complaintApp.models import UserMaster, ComplaintMaster
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime
import csv
from django.template.loader import get_template
import pdfkit


def check_con(func):
    def wrapper(request, *args, **kwargs):
        ls1 = request.session.keys()
        print(ls1)
        ls2 = ['user_id', 'user_email', 'role', 'is_superuser']
        check =  all(item in ls1 for item in ls2)
        if check:
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper


def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if not user:
            return render(request, "login.html", context={"message":"invalid credential."})
        
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['role'] = user.role
        request.session['is_superuser'] = user.is_superuser

        if user.role == "user":
            return redirect('/complaint-list/')
        else:
            return redirect('/complaint-list/')

    if request.method == "GET":
        request.session.clear()
        print(request.session.keys())
        return render(request, "login.html")


def logout(request):

    if request.method == "GET":
        request.session.clear()
        return redirect('/')


def registration(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        UserMaster.objects.create(email=email, custom_password=password)
        return redirect('/')
    
    if request.method == "GET":
        return render(request, "registration.html")


@check_con
def complaint(request):
    try:
        if request.method == "POST":
            complaint = request.POST['complaint']
            ComplaintMaster.objects.create(complaint=complaint, created_by_id=request.session['user_id'])
            return redirect('/complaint-list/')
        
        if request.method == "GET":
            return render(request, "post_complaint.html")
    except:
        return redirect('/')


@check_con
def complaintList(request):
    try:
        if request.method == "GET":
            if request.session['role'] == "user":
                queryset = ComplaintMaster.objects.filter(created_by_id=request.session['user_id']).order_by('-id')
                return render(request, "user_complaint_list.html", context={"queryset":queryset})
            else:
                queryset = ComplaintMaster.objects.all().order_by('-id')
                if "status" in request.GET:
                    status = request.GET['status']
                    queryset = queryset.filter(status=status)
                    return render(request, "user_complaint_list.html", context={"queryset":queryset,"redirect":"/complaint-list/?status={}".format(status)})
                return render(request, "user_complaint_list.html", context={"queryset":queryset, "redirect":"/complaint-list/"})
    except Exception as e:
        print(e.args)
        return redirect('/')


@check_con
def statusUpdate(request):
    try:
        if request.method == "GET":
            if request.session['role'] == "worker":
                status = request.GET['status']
                id = request.GET['id']
                obj = ComplaintMaster.objects.get(id=id)
                obj.status = status
                obj.updated_by_id = request.session['user_id']
                obj.save()
                return redirect(request.GET['redirect'])
            else:
                return HttpResponse("<html><body>Only worker allow for this action</body></html>")
    except:
        return redirect("/")


@check_con
def analysis(request):
    try:
        if request.method == "GET":
            if request.session['role'] == "worker":
                data = {}

                user_qs = list(ComplaintMaster.objects.filter(created_by__role='user').values('created_by__id').annotate(count=Count('id')))

                data["chart_1_id"] = [d['created_by__id'] for d in user_qs]
                data["chart_1_count"] = [d['count'] for d in user_qs]

                complaint_qs = ComplaintMaster.objects.all()
                data['chart_2'] = [
                    complaint_qs.filter(status="pending").count(),
                    complaint_qs.filter(status="in_progress").count(),
                    complaint_qs.filter(status="completed").count()
                ]

                daily_complaint_qs = list(ComplaintMaster.objects.values('created__date').annotate(count=Count('id')))
                data["chart_3_date"] = [d['created__date'].strftime("%m/%d/%Y") for d in daily_complaint_qs]
                data["chart_3_count"] = [d['count'] for d in daily_complaint_qs]
                # print(daily_complaint_qs)

                print(data)

                return render(request, "analysis.html", context=data)
    except:
        return redirect("/")


def export(request):
    try:
        if request.method == "GET":
            doc_type = "csv"
            for_what = "complaint"
            if 'doc_type' in request.GET:
                doc_type = request.GET['doc_type']
            if "for_what" in request.GET:
                for_what = request.GET["for_what"]
            
            if for_what == "user":
                headline = ['email','created']
                queryset = UserMaster.objects.filter(role="user").exclude(is_superuser=True)
                queryset_list = queryset.values_list('email','created')
            else:
                headline = ['complaint','status','user']
                queryset = ComplaintMaster.objects.all()
                queryset_list = queryset.values_list('complaint','status','created_by__email')
            
            if doc_type == "csv":
                response = HttpResponse(content_type='text/csv')
                filename = "{}.csv".format(for_what)
                response['Content-Disposition'] = 'attachment; filename=' + filename
                writer = csv.writer(response)

                writer.writerow(headline)
                for data in queryset_list:
                    writer.writerow(data)
                return response

            else:
                template = get_template("export_pdf.html")
                print({"headline":headline,"queryset":queryset, "for_what":for_what})
                html = template.render({"headline":headline,"queryset":queryset, "for_what":for_what})
                pdf = pdfkit.from_string(html, False)
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(for_what)
                return response
            

    except Exception as e:
        print(e.args)
        return redirect("/")
        