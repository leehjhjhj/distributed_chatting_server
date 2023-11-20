from django.shortcuts import get_object_or_404
from members.domains import Member

class MemberRepository:
    def find_member_by_email(self, email: str):
        return get_object_or_404(Member, email=email)