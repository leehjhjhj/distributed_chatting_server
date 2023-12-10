from dependency_injector import containers, providers
from members.applications import MemberService, TokenService
from members.domains import MemberRepository

class MembersContainer(containers.DeclarativeContainer):
    member_repository = providers.Factory(MemberRepository)
    member_service = providers.Factory(
        MemberService,
        member_repository=member_repository
    )
    token_service = providers.Factory(
        TokenService,
        member_repository=member_repository
    )