from django.shortcuts import redirect


class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.path == LOGIN_REDIRECT_URL:
            if request.user.is_resident:
                return redirect('resident_dashboard')
            elif request.user.is_specialist:
                return redirect('specialist_dashboard')
            elif request.user.is_tszh_member:
                return redirect('tszh_dashboard')

        return response