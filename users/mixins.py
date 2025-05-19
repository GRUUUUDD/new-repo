from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

#чуть под обновила для форума
class ResidentRequiredMixin:
    """Только для жильцов (статус 3)"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 3:
            raise PermissionDenied("Доступ только для жильцов")
        return super().dispatch(request, *args, **kwargs)


class TSZHMemberRequiredMixin:
    """Только для членов ТСЖ (статус 1 или 2)"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.role in [1, 2]:
            raise PermissionDenied("Доступ только для членов ТСЖ")

        return super().dispatch(request, *args, **kwargs)


class SpecialistRequiredMixin:
    """Только для специалистов (статус 4)"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 4:
            raise PermissionDenied("Доступ только для специалистов")
        return super().dispatch(request, *args, **kwargs)


# Декораторная версия для функций
def tszh_member_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.role in [1, 2]:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper
