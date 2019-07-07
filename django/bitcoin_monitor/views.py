import logging
import os

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View


react_index_path = os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')


class FrontendAppView(View):
    """
    Serves the compiled frontend entry point
    (only works if you have run `npm run build`).
    """

    def get(self, request):
        try:
            with open(react_index_path) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            logging.exception('Production build of app not found')
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `npm run build` to test the production version.
                """,
                status=501,
            )
