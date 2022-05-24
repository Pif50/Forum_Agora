from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

class StaffMixin(UserPassesTestMixin):
    """ Lo scopo di questo mixin è fare in modo che solo lo staff possa creare nuove sezioni """

    def test_func(self): #Qual'ora test_func restituisca TRUE, allora il test è stato superato.
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())