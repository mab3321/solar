from django.urls import path,re_path
from . import views
from .views import manage_items, manage_invoices
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
class CustomRouter(DefaultRouter):
    def get_urls(self):
        urls = super().get_urls()
        urls.append(re_path(r'^api/(?P<model_name>[^/.]+)/$',
                             views.DynamicModelViewSet.as_view({'get': 'list', 'post': 'create'}),
                            name='dynamicmodel-list'))
        urls.append(re_path(r'^api/(?P<model_name>[^/.]+)/(?P<pk>[^/.]+)/$',
                            views.DynamicModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
                            name='dynamicmodel-detail'))
        return urls

router = CustomRouter()

urlpatterns = [
    path('', views.index, name='base'),
    path('manage_clients/', manage_items, name='manage_clients'),
    path('manage_invoices/', manage_invoices, name='manage_invoices'),
    path('invoice/',  views.InvoiceModelListView.as_view(), name='invoice'),
    path('invoice/<int:invoice_id>/', views.InvoiceModelListView.as_view(), name='invoice-detail'),
    path('invoice/<int:invoice_id>/download/',  views.modify_and_send_file, name='download-invoice'),
    path('<str:model_name>/', views.GenericModelListView.as_view(), name='generic_list'),
    path('<str:model_name>/new/', views.GenericModelCreateView.as_view(), name='generic_create'),
    path('<str:model_name>/edit/<int:pk>/', views.GenericModelUpdateView.as_view(), name='generic_update'),
    path('<str:model_name>/delete/<int:pk>/', views.GenericModelDeleteView.as_view(), name='generic_delete'),
    ]
urlpatterns = router.urls + urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)