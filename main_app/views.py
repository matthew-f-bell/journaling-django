from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from .models import CustomUser
from django.http import HttpResponseRedirect, HttpResponseBadRequest
# Create your views here.

# Home Page View
class Home(TemplateView):
    template_name = 'home.html'

@login_required
def profile_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
#    if username:
#        profile = get_object_or_404(CustomUser, username=username).profile
#    else:
#        try:
#            profile = request.user.profile
#        except:
#            return HttpResponseBadRequest("you bad boy, profile is broken and can't get profile info")
#            return redirect('/')
    return render(request, 'profile.html', {'user': user})
