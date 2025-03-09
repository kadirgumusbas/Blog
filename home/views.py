from django.shortcuts import render, HttpResponse

def home_view(request):
    if request.user.is_authenticated:
        context = {
            'isim' : request.user.get_full_name(),
        }
    else:
        context = {
            'isim' : 'misafir',
        }
    return render(request, 'home.html', context)