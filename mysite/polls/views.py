from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render

@login_required
def index(request):
    # return HttpResponse("Hello, world.")
    return render(request, "index.html")
    
class logout(LogoutView):
    template_name = "logout.html"
    
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                next = request.GET["next"] if "next" in request.GET else "/"
                return redirect(next)
            else:
                return render(request, "login.html", {"warning": "Your account is disabled"})
        else:
            return render(request, "login.html", {"warning": "Invalid username and or password"})