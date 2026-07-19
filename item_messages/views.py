from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get messages for items owned by the user
        return Message.objects.filter(item__parent=self.request.user)


class MessageDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(item__parent=self.request.user)

    def update(self, request, *args, **kwargs):
        # Mark as read when updating
        instance = self.get_object()
        if 'is_read' in request.data:
            instance.is_read = request.data['is_read']
            instance.save()
        return Response(MessageSerializer(instance).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_message(request):
    """Public endpoint to create a message (for QR code scanning)"""
    serializer = MessageCreateSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

