from django.urls import path
from .views import BusinessNameView, BusinessDetailsView, IntegrationsView, UserIntegrationsView,UserIntegrationStatsView

urlpatterns = [
    path('dashboard/business-name/', BusinessNameView.as_view(), name='business-name-completion'),
    path('dashboard/business_details/', BusinessDetailsView.as_view(), name='business-details-completion'),
    path('dashboard/integrations/', IntegrationsView.as_view()),  # Built-in integrations
    path('dashboard/user_integrations/', UserIntegrationsView.as_view()),
    path('dashboard/update_integrations/<int:pk>/', UserIntegrationsView.as_view(), name='user-integration-status'),
    path('dashboard', UserIntegrationStatsView.as_view(), name='user-services-counts')
    
]
