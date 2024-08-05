from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from django.utils import timezone
from .models import Business, Service, UserIntegration
from .serializers import BusinessNameSerializer, BusinessDetailsSerializer, UserIntegrationSerializer


class BusinessNameView(APIView):
    permission_classes = [IsAuthenticated]

    def create_notification(self, user, subject, body, notification_type, from_user):
        """
        Helper method to create a notification.
        """
        Notification.objects.create(
            user=user,
            subject=subject,
            body=body,
            time=timezone.now(),
            type=notification_type,
            from_user=from_user
        )

    def post(self, request):
        user = request.user
        serializer = BusinessNameSerializer(data=request.data)

        if serializer.is_valid():
            business_name = serializer.validated_data.get('business_name')

            # Check if a business with the same name already exists
            if Business.objects.filter(business_name=business_name).exists():
                return Response({
                    'status': 'failed',
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'A business with this name already exists.',
                    'data' : {}
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=user)

            # Create notification for saving business name
            notification_subject = "Business Registration"
            notification_body = f"{user.email} has registered their business with the name '{business_name}'"
            self.create_notification(user, notification_subject, notification_body, 'business_saved', 'system')

            return Response({
                'status': 'success',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Business name saved successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'failed',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
            'data' : {}
        }, status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_business_instance(self, user):
        """
        Helper method to get the business instance for the user.
        """
        try:
            return user.business_profile
        except Business.DoesNotExist:
            return None

    def post(self, request):
        user = request.user
        business = self.get_business_instance(user)

        if not business:
            return Response({
                'status': 'failed',
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Business profile not found. Please save business name first.',
                'data' : {}
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BusinessDetailsSerializer(business, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Business details saved successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'failed',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
            'data' : {}
        }, status=status.HTTP_400_BAD_REQUEST)

class IntegrationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        selected_integrations = request.data.get('selected_integrations', [])
        other_integrations = request.data.get('other_integrations',[])
        try:
                business_id = Business.objects.get(user=user.id)
        except Business.DoesNotExist:
                return Response({'status': 'failed', 'status_code': status.HTTP_404_NOT_FOUND, 'message': 'User has no business profile','data':{}}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Add selected integrations
            for integration_id in selected_integrations:
                try:
                    integration = Service.objects.get(pk=integration_id)
                    UserIntegration.objects.create(user=user, service=integration, status='todo', business_id=business_id.id)
                except Service.DoesNotExist:
                    return Response({'status': 'failed', 'status_code': status.HTTP_400_BAD_REQUEST, 'message': f'Integration with ID {integration_id} not found','data':{}}, status=status.HTTP_400_BAD_REQUEST)
            # Add other integrations
            for integration_name in other_integrations:
                integration, created = Service.objects.get_or_create(name=integration_name, type="False")
                UserIntegration.objects.create(user=user, service=integration, status='todo', business_id=business_id.id)

            return Response({'status': 'success', 'status_code': status.HTTP_200_OK, 'message': 'Integrations saved successfully', 'data': {}}, status=status.HTTP_200_OK)

        except Service.DoesNotExist as e:
             return Response({'status': 'failed', 'status_code': status.HTTP_400_BAD_REQUEST, 'message': str(e),'data':{}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'failed', 'status_code': status.HTTP_304_NOT_MODIFIED, 'message': f'the service is already exist id: {integration.id} service name:{integration}','data':{}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserIntegrationsView(APIView):
    permission_classes = [IsAuthenticated]
    def create_notification(self, user, subject, body, notification_type, from_user):
        """
        Helper method to create a notification.
        """
        Notification.objects.create(
            user=user,
            subject=subject,
            body=body,
            time=timezone.now(),
            type=notification_type,
            from_user=from_user
        )

    def get(self, request):
        user = request.user
        user_integrations = UserIntegration.objects.filter(user=user).select_related('service')
        serializer = UserIntegrationSerializer(user_integrations, many=True)
        return Response({'status': 'success', 'status_code': status.HTTP_200_OK,'message':'fetched user services sucessfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        try:
            user_integration = UserIntegration.objects.get(service=pk, user=user)
            new_status = request.data.get('status')

            if new_status in ['in_progress', 'completed']:
                old_status = user_integration.status
                user_integration.status = new_status
                user_integration.save()

                # Create notification for status update
                notification_subject = f"Status update for {user_integration.service.name}"
                notification_body = f"Status updated from {old_status} to {new_status}"
                self.create_notification(user, notification_subject, notification_body, 'status_update', 'system')

                return Response({'status': 'success', 'status_code': status.HTTP_200_OK,'message':'Integration status updated', 'data': new_status}, status=status.HTTP_200_OK)
               
            elif new_status == 'todo' and not user_integration.integration.is_built_in:
                # Handle marking custom integrations as read (no status change)
                pass
            else:
               return Response({'status': 'failed', 'status_code': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid status provided','data':{}}, status=status.HTTP_400_BAD_REQUEST)
        except UserIntegration.DoesNotExist:
            return Response({'status': 'failed', 'status_code': status.HTTP_404_NOT_FOUND, 'message': 'Integration not found','data':{}}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        user = request.user
        try:
            user_integration = UserIntegration.objects.get(service_id=pk, user=user)
            user_integration.delete()

             # Create notification for deletion
            notification_subject = f"Integration {user_integration.service.name} deleted"
            notification_body = "Integration has been deleted"
            self.create_notification(user, notification_subject, notification_body, 'integration_deleted', 'system')

            return Response({
                'status': 'success',
                'status_code': status.HTTP_200_OK,
                'message': 'User integration deleted successfully',
                'data': {}
            }, status=status.HTTP_200_OK)
        except UserIntegration.DoesNotExist:
            return Response({
                'status': 'error',
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'User integration not found',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'An unexpected error occurred: {str(e)}',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserIntegrationStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            todo_count = UserIntegration.objects.filter(user=user, status='todo').count()
            in_progress_count = UserIntegration.objects.filter(user=user, status='in_progress').count()
            completed_count = UserIntegration.objects.filter(user=user, status='completed').count()

            total_count = todo_count + in_progress_count + completed_count
            if total_count == 0:
                general_progress_percentage = 0
            else:
                general_progress_percentage = (completed_count / total_count) * 100

            return Response({
                'status': 'success',
                'status_code': status.HTTP_200_OK,
                'message': 'Fetched user integration counts and general progress successfully',
                'data': {
                    'todo': todo_count,
                    'in_progress': in_progress_count,
                    'completed': completed_count,
                    'total': total_count,
                    'general_percentage': round(general_progress_percentage, 2)  # Round to two decimal places
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'An unexpected error occurred: {str(e)}',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        