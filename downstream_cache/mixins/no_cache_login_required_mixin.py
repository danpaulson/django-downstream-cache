from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin


class NoCacheLoginRequiredMixin(LoginRequiredMixin):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
