
from email.mime import base
from django.contrib import admin
from django.db import router
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static, url, serve


from matrixapp import views

from .import views , HOD_Views,SuperAgent_Views

# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns



def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    
    path('admin/', admin.site.urls),
     path('admin/', admin.site.urls),
    path('', include("Home.urls")),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    
    path('base1', views.BASE1, name='base1') ,

    path('pagelogin', views.pagelogin, name='login') ,
    path('pagelogin1', views.pagelogin1, name='login1') ,
    path('', views.prelogin, name='prelogin') ,

    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogin1', views.doLogin1, name='doLogin1'),
    path('Logout', views.doLogout,name="logout"),

    #profile update 

    
    path('registeruserr/', views.registeruserr,name="registeruserr"),
    path('do_superAgent_signup',views.dosuperAgent,name="do_superAgent_signup"),
    path('do_Agent_signup',views.doAgent,name="do_Agent_signup"),

    # Car Path 

    path('addcar/', HOD_Views.addcar,name="addcar"),
    path('car/view_Car', HOD_Views.view_Car,name="view_Car"),
    path('car/availablecar', HOD_Views.availablecar,name="availablecar"),
    path('view_Car/Edit<str:id>', HOD_Views.EDIT_Car,name="EDIT_Car"),
    path('view_car/UPDATE', HOD_Views.UpdateCar,name="UpdateCar"),
    path('view_car/deletecar<str:id>', HOD_Views.deletecar,name="deletecar"),
   
     
    
   
    path('HOD/approvedplote/', HOD_Views.approvedplote,name="approvedplote"),
    path('HOD/bookplot/Delete/<str:id>',HOD_Views.DELETE_PLOT,name="delete_plot"),
    path('HOD/searchbar/',HOD_Views.SEARCH_BAR,name="searchbar"),

    # Hod Panel 
    path('signup_admin/',views.signup_admin,name="signup_admin"),
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('HOD/Home', HOD_Views.HOME, name='admin_home'),


     ########################## define for user url ############################

    path('Agent/Home', SuperAgent_Views.Home, name='Agent_Home') ,
    path('car/view_Car1', SuperAgent_Views.view_Car1,name="view_Car1"),
    path('car/bookcar<str:id>', SuperAgent_Views.bookcar,name="bookcar"),
    path('car/carbook', SuperAgent_Views.bookcar1,name="bookcar1"),
    path('car/bookedcars', SuperAgent_Views.bookedcars,name="bookedcars"),


    



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
         path('__debug__/', include('debug_toolbar.urls')),

    ]+urlpatterns

# urlpatterns += staticfiles_urlpatterns()
   