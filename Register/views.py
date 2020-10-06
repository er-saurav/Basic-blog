from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView,View,ListView,DetailView,CreateView,TemplateView,UpdateView,DeleteView
from .forms import user_form,profile_form,post_form
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from .models import Post
from django.contrib.auth.models import User

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post/index.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        return context

@method_decorator(login_required,name='dispatch')
class UserPost(DetailView):
    model = User
    template_name = 'post/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['myPost'] = True
        return context

@method_decorator(login_required,name='dispatch')
class DeletePost(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('home')

@method_decorator(login_required,name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ['title','content','status','image']
    template_name = 'post/post_update.html'
    def get_success_url(self):
        return reverse('details',kwargs={'slug':self.object.slug})

@login_required
def createPost(request):
    if request.method == 'POST':
        userPost = post_form(request.POST)
        if userPost.is_valid():
            fs = userPost.save(commit=False)
            '''userPost.cleaned_data['author'] = request.user'''
            fs.author = request.user
            if 'image' in request.FILES:
                fs.image = request.FILES['image']
            fs.save()
            return HttpResponseRedirect(reverse('details',args=[slugify(userPost.cleaned_data['title'])]))
        else:
            model = post_form(initial={'author':request.user})
            return render(request,'post/createPost.html',{'msg':userPost.errors,'form':model})
    else:
        model = post_form(initial={'author': request.user,'status':1})
        model.author = request.user
        return render(request, 'post/createPost.html',{'form':model,'user':request.user})

def register(request):
    registered= False
    if request.method=='POST':
        user = user_form(request.POST)
        profile = profile_form(request.POST)
        if user.is_valid() and profile.is_valid():
            user = user.save()
            user.set_password(user.password)
            user.save()

            profile = profile.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(profile.errors,user.errors)
    else:
        user = user_form()
        profile = profile_form()
    return render(request,'register/register.html',{'user_form':user,'profile_form':profile,'registered':registered})

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('<h1>Failed</h1><br><p> Your account is currently unactive </p>')
        else:
            print('username:{}\npassword:{}'.format(username,password))
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'register/login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def help(request):
    return render(request,'register/help.html')