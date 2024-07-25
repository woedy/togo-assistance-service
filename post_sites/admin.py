from django.contrib import admin

from post_sites.models import ClientZone, ClientZoneCoordinate, ClientPostSite, PostSiteActivity, PostOrder, \
    PostSiteNote, PostSiteFile, PostSiteAssignedGuard, PostSiteTask, SiteReport

admin.site.register(ClientZone)
admin.site.register(ClientZoneCoordinate)
admin.site.register(ClientPostSite)
admin.site.register(PostSiteActivity)
admin.site.register(PostOrder)
admin.site.register(SiteReport)
admin.site.register(PostSiteNote)
admin.site.register(PostSiteFile)
admin.site.register(PostSiteAssignedGuard)
admin.site.register(PostSiteTask)
