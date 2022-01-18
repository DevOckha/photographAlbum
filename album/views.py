from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from .models import Profile, Photograph
from .forms import PhotoForm, ProfileForm, CustomUserCreationForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

def photos(request):
    photos = Photograph.objects.all()
    context = {'photos':photos}
    return render(request, 'album/photo_list.html', context)


def photoDetail(request, pk):
    photo = Photograph.objects.get(id=pk)
    context = {'photo':photo}
    return render(request, 'album/photo_detail.html', context)



# class PhotoCreateView(CreateView):
#     model = Photograph
#     form_class = PhotoForm
#     template_name = 'album/create_photo.html'
#     success_url = reverse_lazy('list_photos')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.profile = self.request.user
#         self.object.save()
#         return super().form_valid(form)

@login_required(login_url='login')
def photoCreate(request):

    form = PhotoForm()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('list_photos')
                
    context = {'form':form}
    return render(request, 'album/create_photo.html', context)

@login_required(login_url='list_photos')
def photoEdit(request, pk):
    photo = Photograph.objects.get(id=pk)
    form = PhotoForm(instance=photo)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        print(request.POST)

        if form.is_valid():
            form.save()
        return redirect('list_photos')
    context = {'form':form}

    return render(request, 'album/photo_edit.html', context)

@login_required(login_url='list_photos')
def photoDelete(request, pk):
    photo = Photograph.objects.get(id=pk)

    if request.method == 'POST':
        photo.delete()
        return redirect('list_photos')
    context = {'photo':photo}
    return render(request, 'album/delete_photo.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('list_photos')
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this username does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('list_photos')
        else:
            messages.error(request, 'Username OR password is incorrect')
    
    context = {}
    return render(request, 'album/login.html', context)



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('list_photos')
    
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user, username=user.username, first_name = user.first_name, last_name = user.last_name)
            messages.success(request, 'Account successfuly created!')
            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
            
            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'list_photos'
            return redirect(next_url)
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form':form}
    return render(request, 'album/register.html', context)



def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='list_photos')
def userAccount(request):
    profile = request.user.profile
    context = {'profile':profile}
    return render(request, 'album/account.html', context)


@login_required(login_url='list_photos')
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'album/profile_form.html', context)