from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Child
from .serializers import ChildSerializer, ChildCreateSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def child_list_create_view(request):
    if request.method == "GET":
        queryset = Child.objects.filter(parent=request.user)
        serializer = ChildSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ChildCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def child_detail_view(request, pk):
    try:
        child = Child.objects.get(pk=pk, parent=request.user)
    except Child.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ChildSerializer(child)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = ChildSerializer(
            child,
            data=request.data,
            partial=request.method == "PATCH",
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        child.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

