from django.contrib import admin

from security_team.models import SecurityGuard, SecurityGuardID, SecurityGuardIDImage, SecurityGuardContact, \
    SecurityGuardDeviceInfo, SecurityGuardActivity, SecurityGuardFile, SecurityGuardNote, SecurityGuardSkill, \
    SecurityGuardAccess, SecurityGuardSetting, SecurityGuardSettingGeneral, SecurityGuardSettingTimeClock, \
    SecurityGuardSettingScheduler, SecurityGuardTask, SecurityGuardSettingNotification, GuardAvailability, TimeSlot

admin.site.register(SecurityGuard)
admin.site.register(SecurityGuardID)
admin.site.register(SecurityGuardIDImage)
admin.site.register(SecurityGuardContact)
admin.site.register(SecurityGuardDeviceInfo)
admin.site.register(SecurityGuardActivity)
admin.site.register(SecurityGuardFile)
admin.site.register(SecurityGuardNote)
admin.site.register(SecurityGuardSkill)
admin.site.register(SecurityGuardAccess)
admin.site.register(SecurityGuardSetting)
admin.site.register(SecurityGuardSettingGeneral)
admin.site.register(SecurityGuardSettingTimeClock)
admin.site.register(SecurityGuardSettingScheduler)
admin.site.register(SecurityGuardSettingNotification)
admin.site.register(SecurityGuardTask)
admin.site.register(GuardAvailability)
admin.site.register(TimeSlot)
