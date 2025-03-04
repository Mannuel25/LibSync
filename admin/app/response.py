from rest_framework.response import Response
from rest_framework import status

class CustomResponse():
    """A custom view for every response sent by the server"""

    @staticmethod
    def success(data=None, message=None, status=status.HTTP_200_OK):
        response_data = {
            "success": True,
            "data": data or [],
            "message": message or "success"
        }
        return Response(response_data, 
            status=status)

    @staticmethod
    def failed(data=None, message=None, status=status.HTTP_400_BAD_REQUEST):
        response_data = {
            "success": False,
            "data": data or [],
            "message": message or "failed"
        }
        return Response(response_data, 
            status=status)


