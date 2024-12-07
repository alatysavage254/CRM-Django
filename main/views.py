from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record





from django.contrib import messages


# - Homepage

def home(request):
    return render(request, 'index.html')


# - Register a user

def register(request):
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form': form}

    return render(request, 'register.html', context=context)


# - Login a user

def my_login(request):
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)



                return redirect("dashboard")

    context = {'form': form}

    return render(request, 'my-login.html', context=context)

#Dashboard
@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context   =  {'records': my_records}
    return render(request, 'dashboard.html', context=context)


# - User logout
def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")

#create a record
@login_required(login_url='my-login')
def create_record(request):

    form  = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Record created successfully!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'create-record.html', context=context)

#update a record

@login_required(login_url='my-login')
def update_record(request, pk):
    # Retrieve the record or return 404 if not found
    record = get_object_or_404(Record, id=pk)

    if request.method == "POST":
        # Handle form submission
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")
    else:
        # Render form for GET request
        form = UpdateRecordForm(instance=record)

    # Render the form regardless of request method
    context = {'form': form}
    return render(request, 'update-record.html', context)

    #Read or view a singular record
@login_required(login_url='my-login')
def singular_record(request, pk):
    all_records = Record.objects.get(id=pk)

    context = {'record': all_records}

    return render(request, 'view-record.html', context=context)

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")
