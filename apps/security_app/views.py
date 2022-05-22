import code
from django.shortcuts import render, get_object_or_404, redirect
from security_app.models import Sharer 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def create_sharer(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = get_object_or_404(User, username=username)
        code = generate_code()
        limit_visits = request.POST['limit_visits']
        limit_datetime = request.POST['limit_datetime']

        # Criar sharer
        sharer = Sharer.objects.create(user=user,code=code,limit_visits=limit_visits,limit_datetime=limit_datetime)
        sharer.save()

        # Atualizar senha de um usuário criado
        user.update(password=password).save()

        return redirect('?user='+username)
    elif 'user' in request.GET:
        sharer = get_object_or_404(Sharer, user=user)
        data = {
            'sharer':sharer
        }
        return render(request, 'create_sharer.html',data)
    else:
        User = get_user_model()
        users = User.objects.all()
        data = {
            'users':users
        }
        return render(request, 'create_sharer.html', data)

def sharer(request):
    if 'code' in request.GET:
        sharer = get_object_or_404(Sharer, code=request.GET['code'])
        if authorized_to_display(sharer):
            return render(request, 'sharer.html')
        else:
            return render(request, 'sharer.html')
    else:
        return render(request, 'sharer.html')

def generate_code():
    return "..."

def authorized_to_display(sharer):
    return True