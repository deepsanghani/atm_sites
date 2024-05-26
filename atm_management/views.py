from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import ATMSite

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()

            group_name = 'app_viewer'
            group = Group.objects.filter(name=group_name).first()
            if not group:
                group = Group.objects.create(name=group_name)
                content_type = ContentType.objects.get_for_model(ATMSite)
                permission_view = Permission.objects.get(content_type=content_type, codename='view_atmsite')
                group.permissions.add(permission_view)

            user.groups.add(group)

            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('admin:index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
