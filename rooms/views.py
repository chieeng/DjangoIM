from django.http import HttpResponse


def index(request):
    return HttpResponse("Rooms module placeholder.", content_type="text/plain")


def room_list(request):
    return HttpResponse("Room list placeholder.", content_type="text/plain")


def room_detail(request, pk: int):
    return HttpResponse(f"Room detail placeholder: {pk}", content_type="text/plain")

