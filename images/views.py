from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from .models import Image
from django.views.generic import View,DetailView
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from actions.utils import create_action

# Create your views here.
class ImageCreateView(View):
    def get(self,*args,**kwargs):
        return render(self.request,'images/image/create.html',context={'form':ImageCreateForm(data=self.request.GET)})
    
    def post(self,*args,**kwargs):
        form =  ImageCreateForm(data=self.request.POST)
        
        if form.is_valid():
            image = form.save(commit=False)
            image.user = self.request.user
            image.save()
            create_action(self.request.user,'bookmarked image',image)
            return redirect(image.get_absolute_url())
        else:
            print("form is invalid")

        return render(self.request,'images/image/create.html',context={'form':ImageCreateForm(data=self.request.GET)})

class ImageDetailView(DetailView):
    model = Image
    template_name = 'images/image/detail.html'
    context_object_name = 'image'

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user,'likes',image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    else:
        return JsonResponse({'status':'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    p = Paginator(images,6)
    page = request.GET.get('page')

    try:
        images = p.page(page)
    except PageNotAnInteger:
        images = p.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = p.page(p.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',{'images':images,'imgs':'active'})
    return render(request,'images/image/list.html',{'images':images,'imgs':'active'})


