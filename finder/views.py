from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from finder.forms import ResourcesForm, CreateUserForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Resources,UserResources, UserQuality
from finder.models import ResourcesProper

# Create your views here.


class UserView(generic.DetailView):
    model = User
    template_name = 'finder/user.html'


class UserListView(generic.ListView):
    template_name = "finder/users_list.html"
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class AddResourcesView(generic.FormView):
    template_name = 'finder/new_resources.html'
    form_class = ResourcesForm
    success_url = 'finder/list-resources/'

    def form_valid(self, form):
        resources = form.saveData()
        return super().form_valid(form)


class CreateUserView(generic.FormView):
    template_name = 'finder/create_user.html'
    form_class = CreateUserForm
    success_url = '/finder/list-users/'

    def form_valid(self, form):
        user = form.saveData()
        return super().form_valid(form)


class ResourcesDetails(generic.DetailView):
    model = Resources
    template_name = 'finder/resources.html'

    def get_context_data(self, **kwargs):
        context = super(ResourcesDetails, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

class ResourcesList(generic.ListView):
    template_name = "finder/resources_list.html"
    context_object_name = 'resources'

    def get_queryset(self):
        return Resources.objects.all()


def add_user_resources(request, resources_id):
    user = get_object_or_404(User, pk=request.POST['user_id'])
    resources = get_object_or_404(Resources, pk=resources_id)
    user_resources = UserResources()
    user_resources.user = user
    user_resources.value = resources
    user_resources.save()

    return HttpResponseRedirect(reverse('finder:resources_details', args=(resources_id,)))


def add_resources_proper(request, resources_id):
    resources = get_object_or_404(Resources, pk=resources_id)
    r_proper = ResourcesProper()
    r_proper.resources = resources
    key = request.POST['key']
    value = request.POST['value']
    if(key.replace(" ", "") != "" or value.replace(" ", "") != ""):
        r_proper.key = request.POST['key']
        r_proper.value = request.POST['value']
        r_proper.save()

    return HttpResponseRedirect(reverse('finder:resources_details', args=(resources_id,)))

def add_user_quality(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    u_quality = UserQuality()
    u_quality.user = user
    value = request.POST['value']
    if(value.replace(" ", "") != ""):
        u_quality.value = request.POST['value']
        u_quality.save()

    return HttpResponseRedirect(reverse('finder:user_details', args=(user_id,)))


def delete_user_quality(request, user_quality_id):
    user_quality = get_object_or_404(UserQuality, pk=user_quality_id)
    user_id = user_quality.user.pk
    user_quality.delete()
    return HttpResponseRedirect(reverse('finder:user_details', args=(user_id,)))


def delete_resources_proper(request, proper_id):
    r_proper = get_object_or_404(ResourcesProper, pk=proper_id)
    resources_id = r_proper.resources.pk
    r_proper.delete()

    return HttpResponseRedirect(reverse('finder:resources_details', args=(resources_id,)))


def delete_resources(request, resources_id):
    resources = get_object_or_404(Resources, pk= resources_id)
    resources.delete()
    return HttpResponseRedirect(reverse('finder:resources_list'))


def delete_user_resources(request, uR_id):
    user_resources = get_object_or_404(UserResources, pk = uR_id)
    resources_id = user_resources.value.pk
    user_resources.delete()
    return HttpResponseRedirect(reverse('finder:resources_details', args=(resources_id,)))


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if(user.is_superuser == 0):
        user.delete()
    return HttpResponseRedirect(reverse('finder:users_list'))


def index(request):
    return render(request,'finder/index.html',)

def search(request):
    resourcesPropers = ResourcesProper.objects.filter(value__contains=request.POST['text'])

    userQualities = UserQuality.objects.filter(value__contains=request.POST['text'])

    userNames = User.objects.filter(username__contains=request.POST['text'])
    userEmails = User.objects.filter(email__contains=request.POST['text'])

    data = {}
    resourcesP = {}
    users = {}

    for rP in resourcesPropers:
        resourcesP[rP.pk] = {
            'name': rP.resources.name,
            'id': rP.resources.pk,
            'key': rP.key,
            'value': rP.value
        }

    data['resources'] = resourcesP

    for uQ in userQualities:
        if uQ.user.first_name != "" and uQ.user.last_name != "":
            name = uQ.user.first_name + " " + uQ.user.last_name
        else:
            name = uQ.user.username
        users[uQ.pk] = {
            'name': name,
            'id': uQ.user.pk,
            'key': 'quality',
            'value': uQ.value
        }

    for uQ in userNames:
        if uQ.first_name != "" and uQ.last_name != "":
            name = uQ.first_name + " " + uQ.last_name
        else:
            name = uQ.username
        users[uQ.pk] = {
            'name': name,
            'id': uQ.pk,
            'key': 'username',
            'value': uQ.username
        }

    for uQ in userEmails:
        if uQ.first_name != "" and uQ.last_name != "":
            name = uQ.first_name + " " + uQ.last_name
        else:
            name = uQ.username
        users[uQ.pk] = {
            'name': name,
            'id': uQ.pk,
            'key': 'email',
            'value': uQ.email
        }

    data['users'] = users;

    return JsonResponse(data)


