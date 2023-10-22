from django.urls import path
from. import views
from django.contrib.auth import views as auth_views
from .views import export_data_to_excel,export_data_to_excel_from_product
urlpatterns =[
    path('', views.index, name='dashboard-index'),
    path('export/', export_data_to_excel, name='export_data_to_excel'),
    path('export_data_to_excel_from_product/', export_data_to_excel_from_product, name='export_data_to_excel_from_product'),
    path('staff/',views.staff, name = 'dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff-detail'),
    path('order/update/<int:pk>/', views.order_update, name='dashboard-order-update'),
    path('order/delete/<int:pk>/', views.order_delete, name='dashboard-order-delete'),
    path('order/cancel/<int:pk>/',views.order_cancel, name = 'dashboard-order-cancel'),
    path('staff/delete/<int:pk>/',views.staff_delete, name = 'dashboard-staff-delete'),
    path('product/',views.products, name = 'dashboard-products'),
    path('product/delete/<int:pk>/',views.product_delete, name = 'dashboard-product-delete'),
    path('product/update/<int:pk>/',views.product_update, name = 'dashboard-product-update'),
    path('order/',views.order, name = 'dashboard-order'), 
    path('password-reset/',auth_views.PasswordResetView.as_view(), name = 'password_reset'),
    path('password-reset_done/',auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password_reset_xomplete/',auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
]