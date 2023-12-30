from typing import Union, List, Optional

from django.conf import settings
from django.http.response import HttpResponseBase
from django.utils.cache import cc_delim_re, patch_vary_headers

from rest_framework.response import Response


class DownstreamCacheMixin:
    cache_tags = None
    max_age = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.cache_tags is None:
            self.cache_tags = []
        self.max_age = None

    def add_cache_tags(self, tags: Optional[Union[str, List[str]]] = None):
        """
        Args:
            keys ([array]): [Array of header key strings]
        """
        if tags is None:
            return

        if isinstance(tags, str):
            tags = [tags]

        self.cache_tags += tags

    def dispatch(self, request, *args, **kwargs):
        if not self.cache_tags:
            self.cache_tags = []
        return super(DownstreamCacheMixin, self).dispatch(request, *args, **kwargs)

    def add_headers(self, response):
        if self.cache_tags:
            # Unique out the list before adding headers to prevent duplicates
            self.cache_tags = list(set(self.cache_tags))
            response[settings.DOWNSTREAM_CACHE_HEADER_NAME] = ','.join(self.cache_tags)

        if self.max_age is not None:
            response['Cache-Control'] = 's-maxage=%s' % self.max_age

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.
        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)

        response = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

        self.add_headers(response)

        return response

    # This is used for Django REST requests
    def finalize_response(self, request, response, *args, **response_kwargs):
        """
        Returns the final response object.
        """
        # Make the error obvious if a proper response is not returned
        assert isinstance(response, HttpResponseBase), (
            'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
            'to be returned from the view, but received a `%s`'
            % type(response)
        )

        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        # Add new vary headers to the response instead of overwriting.
        vary_headers = self.headers.pop('Vary', None)
        if vary_headers is not None:
            patch_vary_headers(response, cc_delim_re.split(vary_headers))

        for key, value in self.headers.items():
            response[key] = value

        self.add_headers(response)

        return response
