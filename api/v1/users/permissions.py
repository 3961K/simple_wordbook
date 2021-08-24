from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSelfOrReadOnly(BasePermission):
    """
    GET, HEAD, OPTIONSメソッドの場合は全てのユーザにアクセスを許可し,それ以外のメソッドの
    場合は認証されており,かつアクセスしているユーザとURLに含まれるユーザが同じである必要がある
    """

    def __init__(self, username=''):
        super().__init__()
        self.username = username

    def has_permission(self, request, view):
        # viewからlookup_fieldを介して取得したユーザ名(obj)とrequest.userを比較する
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.username == self.username
        )
