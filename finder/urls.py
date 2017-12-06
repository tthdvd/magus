from django.conf.urls import url

from . import views

app_name = "finder"

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # RESOURCES
    url(r'^new-resources/$', views.AddResourcesView.as_view(), name='add_resources'),
    url(r'^resources/(?P<pk>[0-9]+)/$', views.ResourcesDetails.as_view(), name='resources_details'),
    url(r'list-resources/$', views.ResourcesList.as_view(), name="resources_list"),
    url(r'^delete-resources/(?P<resources_id>[0-9]+)/$', views.delete_resources, name="delete_resources"),

    # RESOURCES PROPER
    url(r'^(?P<resources_id>[0-9]+)/add_proper/$', views.add_resources_proper, name='add_resources_proper'),
    url(r'^delete-resources-proper/(?P<proper_id>[0-9]+)/$', views.delete_resources_proper, name="delete_resources_proper"),

    #SEARCH
    url(r'^search/$', views.search, name='search'),

    #USER RESOURCES
    url(r'^add-user-resources/(?P<resources_id>[0-9]+)/$', views.add_user_resources, name="add_user_resources"),
    url(r'^delete-user-resources/(?P<uR_id>[0-9]+)/$', views.delete_user_resources, name="delete_user_resources"),

    # USER
    url(r'^create-user', views.CreateUserView.as_view(), name="create_user"),
    url(r'^list-users/$', views.UserListView.as_view(), name='users_list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name="user_details"),
    url(r'^delete-user/(?P<user_id>[0-9]+)/$', views.delete_user, name='delete_user'),

    # USER QUALITY
    url(r'^(?P<user_id>[0-9]+)/add-quality/$', views.add_user_quality, name='add_user_quality'),
    url(r'^delete-quality/(?P<user_quality_id>[0-9]+)/$', views.delete_user_quality, name='delete_user_quality'),

]
