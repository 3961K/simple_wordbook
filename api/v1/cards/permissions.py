from rest_framework.permissions import BasePermission


class IsNotAuthorReadPublicOnly(BasePermission):
    def __init__(self, card=None):
        super().__init__()
        self.card = card

    def has_permission(self, request, view):
        if not self.card.is_hidden:
            # 公開カードに対して作者の場合は全ての操作を許可
            if request.user.id == self.card.author.id:
                return bool(
                    True
                )

            # 公開カードに対して作者でない場合はGETのみ許可
            return bool(
                request.method == 'GET'
            )

        # 非公開カードに対してはGET, PATCH, DELETE全ての処理が作者のみに許可される
        return bool(
            request.user.id == self.card.author.id
        )
