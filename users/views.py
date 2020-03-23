from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,View,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.contrib.auth import get_user_model
from common.decorators import ajax_required
from django.http import JsonResponse
from .models import Contact
from actions.utils import create_action
from actions.models import Action

# Create your views here.
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self):
        actions = Action.objects.exclude(user=self.request.user)
        following_ids = self.request.user.following.values_list('id',flat=True)

        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.prefetch_related('target')[:10]
        return {'dsb':'active','actions':actions}

class EditProfileView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        return render(self.request,'account/edit.html',context={'form':EditProfileForm(instance=self.request.user)})
    
    def post(self,*args,**kwargs):
        form = EditProfileForm(instance=self.request.user,data=self.request.POST,files=self.request.FILES)
        if form.is_valid():
            form.save()
        return render(self.request,'account/edit.html',context={'form':EditProfileForm(instance=self.request.user)})

class UsersListView(LoginRequiredMixin,ListView):
    model = get_user_model()
    template_name = 'account/user/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ppl'] = 'active'
        return context

class UserDetailView(LoginRequiredMixin,DetailView):
    model = get_user_model()
    template_name = 'account/user/detail.html'

    def get_queryset(self):
        return get_object_or_404(get_user_model(),is_active=True,username=self.kwargs['username'])
    
    
@login_required
def user_detail_view(request,username):
    user = get_object_or_404(get_user_model(),username=username,is_active=True)
    return render(request,'account/user/detail.html',{'user':user})


class FollowUserView(LoginRequiredMixin,View):

    def post(self,*args,**kwargs):
        to = self.request.POST.get('id')
        action = self.request.POST.get('action')
        
        if to and action:
            try:
                user_to = get_user_model().objects.get(id=to)
                if action == 'follow':
                    Contact.objects.get_or_create(user_to=user_to,user_from=self.request.user)
                    create_action(self.request.user,'is following',user_to)
                    return JsonResponse({'status':'ok'})
                else:
                    Contact.objects.filter(user_to=user_to,user_from=self.request.user).delete()
                    return JsonResponse({'status':'ok'})
            except:
                return JsonResponse({'status':'ko'})
        
        return JsonResponse({'status':'ko'})

