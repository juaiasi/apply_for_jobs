from datetime import timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from security_app.models import Sharer 
from django.contrib.auth.models import User
from shortuuid import ShortUUID

def create_sharer(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = get_object_or_404(User, username=username)
        code = generate_code()
        limit_visits = request.POST['limit_visits']
        limit_datetime = request.POST['limit_datetime']

        # Criar sharer
        sharer = Sharer.objects.create(user=user,code=code,limit_visits=limit_visits,limit_datetime=limit_datetime,password=password)
        sharer.save()

        # Atualizar senha de um usuário criado
        # user.update(password=password).save()

        return redirect('display_link',user=user.id)
    else:
        users = User.objects.all()
        data = {
            'users':users,
            'date': str(date.today() + timedelta(days = 7))
        }
        return render(request, 'create_sharer.html', data)

def display_link(request,user):
    sharer = get_object_or_404(Sharer, user=user)
    data ={
        'sharer':sharer
    }
    return render(request,'display_link.html',data)

def sharer(request,code):
    sharer = get_object_or_404(Sharer, code=code)
    if authorized_to_display(sharer):
        limit_visits = sharer.limit_visits - 1
        Sharer.objects.filter(code=code).update(limit_visits=limit_visits)
        data ={
            'sharer':sharer
        }
        return render(request, 'sharer.html', data)
    return render(request, 'sharer.html')

def generate_code():
    while True:
        code = ShortUUID(alphabet="0123456789").random(length=5)
        try:
            Sharer.objects.get(code=code)
        except:
            break
    return code

def authorized_to_display(sharer):
    today = date.today()
    limit_datetime = sharer.limit_datetime
    limit_visits = sharer.limit_visits
    public = sharer.public
    code = sharer.code

    if (limit_visits>0) and (limit_datetime>=today) and public:
        return True
    else:
        Sharer.objects.filter(code=code).update(public=False,password="")
        return False