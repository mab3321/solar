from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'errors' in data:  # If the response contains errors
            status_code = renderer_context['response'].status_code  # Extract status code
            response_data = {
                'errors': data,
                'status_code': status_code
            }
            response = json.dumps(response_data)  # Return the errors with status code
        else:
            response = json.dumps({'data': data})  # Otherwise, return the data with 'data' key
        return response