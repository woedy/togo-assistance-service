from django.contrib import admin

from human_resources.models import DepartmentComplaint, DetartmentForwardingList, HumanResource, StaffPayrollEntry, StaffPayPeriod, NonSystemUser, \
    RecruitmentAttachment, Recruitment

admin.site.register(HumanResource)
admin.site.register(StaffPayPeriod)
admin.site.register(StaffPayrollEntry)
admin.site.register(Recruitment)
admin.site.register(RecruitmentAttachment)
admin.site.register(NonSystemUser)
admin.site.register(DepartmentComplaint)
admin.site.register(DetartmentForwardingList)
