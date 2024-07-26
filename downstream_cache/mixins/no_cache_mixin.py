from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

class NoCacheMixin:
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    