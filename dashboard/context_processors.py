from .models import PermissionToViewBranch

def permissions_to_view(request):
    permissions = []
    try:
        permissions = PermissionToViewBranch.objects.filter(user__pk=request.user.profile.pk)
    except:
        print("Anonymous user has not profile")
    permissions_length = len(permissions)
    return {"permissions_to_view_branch_length": permissions_length}