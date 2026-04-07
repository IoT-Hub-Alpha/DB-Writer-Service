from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class GetHealth(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"detail": "ok"})