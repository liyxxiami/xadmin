
from django.contrib.admin.templatetags.admin_static import static
from django.template import loader

from exadmin.sites import site
from exadmin.views import BaseAdminPlugin, ListAdminView

REFRESH_VAR = '_refresh'

class RefreshPlugin(BaseAdminPlugin):

    refresh_times = []

    # Media
    def get_media(self, media):
        if self.refresh_times and self.request.GET.get(REFRESH_VAR):
            media.add_js([static('exadmin/js/refresh.js')])
        return media

    # Block Views
    def block_top_toolbar(self, context, nodes):
        if self.refresh_times:
            current_refresh = self.request.GET.get(REFRESH_VAR)
            context.update({
                'has_refresh': bool(current_refresh),
                'clean_refresh_url': self.admin_view.get_query_string(remove=(REFRESH_VAR,)),
                'current_refresh': current_refresh,
                'refresh_times': [{
                    'time': r,
                    'url': self.admin_view.get_query_string({REFRESH_VAR: r}),
                    'selected': str(r) == current_refresh,
                } for r in self.refresh_times],
            })
            nodes.append(loader.render_to_string('admin/blocks/refresh.html', context_instance=context))


site.register_plugin(RefreshPlugin, ListAdminView)

