from django.urls import path
from . import views
# from django.conf.urls import url

urlpatterns = [

    path('',views.homepage,name = "homepage"),
    path('register/', views.register,name='register' ),
    path('registerShop/', views.registerShop,name='registerShop' ),
    path('registerHosp/', views.registerHosp,name='registerHosp' ),
    path('login1/', views.user_login1, name='login1'),
    path('checkLogin1/', views.checkLogin1, name = "checkLogin1"),
    path('checkSignup/', views.checkSignup,name = 'checkSignup'),
    path('checkSignupShopkeeper/', views.checkSignup,name = 'checkSignupShopkeeper'),

    path('logout/', views.user_logout,name = 'logout'),
    path('showLogin/', views.show_login,name = 'showLogin'),
    path('showRegister/', views.show_register,name = 'showRegister'),
      path('create/', views.create_blog, name='create_blog'),

    path('notifications/', views.notifications,name = 'notifications'),
    path('approve/', views.approve,name = 'approve'),
    path('reject/<int:pk>', views.reject,name = 'reject'),

    path('blogs/', views.blogs,name = 'blogs'),
    path('registerDoc/', views.registerDoc,name = 'registerDoc'),
    path('appointment/', views.appointment,name = 'appointment'),
    path('done/', views.done,name = 'done'),
    path('done1/', views.done1,name = 'done1'),
    path('prescription/', views.prescription,name = 'prescription'),
    path('yoga/', views.meditation,name = 'yoga'),
    path('reject/', views.rejectDoc,name = 'reject'),
    path('check/', views.check,name = 'check'),
    path('showMessages/', views.showMessages,name = 'showMessages'),
    path('sendMsg/',views.sendMsg,name = "sendMsg"),
    path('sendMsg1/',views.sendMsg1,name = "sendMsg1"),
    path('checkDate/', views.checkDate,name = 'checkDate'),
    path('appointmentsall/', views.appsall,name = 'appointmentsall'),
    path('therapists/', views.therapists,name = 'therapists'),
    path('enroll/', views.enroll,name = 'enroll'),
    path('myclasses/', views.myclasses,name = 'myclasses'),
    path('viewClass/<int:pk>', views.viewClass,name = 'viewClass'),
    path('approvedoc/<int:pk>', views.approvedoc,name = 'approvedoc'),
    path('rejectdoc/<int:pk>', views.rejectdoc,name = 'rejectdoc'),

    #For application mobile -----------------------------------------------

    path('register1/', views.register1,name='register1' ),
    path('registerDoctor/', views.registerDoctor,name='registerDoctor' ),

    path('login/', views.user_login, name='login'),
    path('blog/', views.blogs, name='blog'),
    path('logout/', views.user_logout, name='logout'),

    path('doctors/', views.doctors, name='doctors'),
    path('blog/', views.blogs, name='blog'),
    path('detect/', views.detect, name='detect'),


    path('addComment/', views.addComment, name='addComment'),
    path('comments/', views.comments, name='loadComments'),
    path('classes/', views.classes, name='classes'),

    path('chats/', views.getChats, name='chats'),
    path('messages/', views.messages, name='messages'),
    path('sendMsg/', views.sendMsg, name='sendMsg'),
    path('leave/', views.leave, name='leave'),
    path('editsymp/<int:pk>', views.editsymp, name='editsymp'),

    ]