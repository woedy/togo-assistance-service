from django.contrib.auth import get_user_model
from rest_framework import serializers

from human_resources.models import DepartmentComplaint, HumanResource, StaffPayrollEntry, StaffPayPeriod, Recruitment, RecruitmentAttachment

User = get_user_model()


class HumanResourceUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class HumanResourceDetailsSerializer(serializers.ModelSerializer):
    user = HumanResourceUserDetailSerializer(many=False)
    class Meta:
        model = HumanResource
        fields = "__all__"








class StaffPayPeriodDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffPayPeriod
        fields = "__all__"


class AllStaffPayPeriodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayPeriod
        fields = "__all__"





class StaffPayrollEntryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffPayrollEntry
        fields = "__all__"


class AllStaffPayrollEntrysSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayrollEntry
        fields = "__all__"


class RecruitmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment
        fields = "__all__"

class AllRecruitmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment
        fields = "__all__"




class RecruitmentAttachmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentAttachment
        fields = "__all__"

class AllRecruitmentAttachmentsSerializer(serializers.ModelSerializer):
    recruitment = AllRecruitmentsSerializer(many=False)
    class Meta:
        model = RecruitmentAttachment
        fields = "__all__"






class DepartmentComplaintDetailSerializer(serializers.ModelSerializer):
    department_complaint_forwarding_list = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentComplaint
        fields = "__all__"


    
    def get_department_complaint_forwarding_list(self, obj):
        return [dcl.department for dcl in obj.department_forwarding_list.all()]






class AllDepartmentComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentComplaint
        fields = "__all__"
