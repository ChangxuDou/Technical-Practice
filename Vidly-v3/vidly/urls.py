from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path
from django.views.generic import TemplateView
from rentals import views as v
from rentals import workflow_views as w
urlpatterns=[
    path("qa/", TemplateView.as_view(template_name="qa.html"), name="qa"),
    path("wishes/",w.wishlist,name="wishlist"),
    path("wallet/",w.my_wallet,name="my_wallet"),
    path("wallet/pay/<uuid:order_id>/",w.mock_payment,name="mock_payment"),
    path("desk/wishes/",w.wish_summary,name="wish_summary"),
    path("desk/wishes/<int:pk>/",w.wish_review,name="wish_review"),
    path("desk/settings/rewards/",w.reward_settings,name="reward_settings"),
    path("desk/purchases/",w.purchases,name="purchases"),
    path("desk/purchases/new/",w.purchase_new,name="purchase_new"),
    path("desk/purchases/<int:pk>/",w.purchase_detail,name="purchase_detail"),
    path('',v.home,name='home'),path('movies/',v.catalog,name='catalog'),path('movies/<int:pk>/',v.detail,name='detail'),
    path('bag/',v.bag,name='bag'),path('bag/add/<int:pk>/',v.bag_add,name='bag_add'),path('bag/update/<int:pk>/',v.bag_update,name='bag_update'),path('checkout/',v.place_order,name='checkout'),
    path('accounts/signup/',v.signup,name='signup'),path('accounts/login/',auth.LoginView.as_view(template_name='login.html'),name='login'),path('accounts/logout/',auth.LogoutView.as_view(),name='logout'),
    path('rentals/',v.my_rentals,name='my_rentals'),path('rentals/<int:pk>/',v.rental_detail,name='rental_detail'),path('coupons/claim/',v.claim_coupon,name='claim_coupon'),
    path('desk/',v.desk,name='desk'),path('desk/customers/',v.customers,name='customers'),path('desk/customers/new/',v.customer_edit,name='customer_new'),path('desk/customers/<int:pk>/edit/',v.customer_edit,name='customer_edit'),path('desk/customers/<int:pk>/wallet/',v.wallet,name='wallet'),path('desk/checkout/',v.counter,name='counter'),
    path('desk/inventory/',v.inventory,name='inventory'),path('desk/inventory/new/',v.movie_edit,name='movie_new'),path('desk/inventory/<int:pk>/',v.movie_edit,name='movie_edit'),path('desk/inventory/<int:pk>/delete/',v.movie_delete,name='movie_delete'),path('desk/reports/',v.reports,name='reports'),
    path('api/movies/',v.movie_api,name='movie_api'),path('admin/',admin.site.urls),
]
