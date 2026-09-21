import odoo
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied
from odoo.service.common import exp_authenticate
from odoo.service.security import check


def _rpc_allowed(user):
    return user.has_group(
        'restricted_rpc.group_xmlrpc_api_access'
    )

def _check_user_rpc_allowed(db, login):
    res_users = odoo.registry(db)["res.users"]
    with res_users.pool.cursor() as cr:
        self = odoo.api.Environment(cr, SUPERUSER_ID, {})[res_users._name]
        with self._assert_can_auth(user=login):
            user = self.search(self._get_login_domain(login), order=self._get_login_order(), limit=1)
            if not user:
                raise AccessDenied()
            user = user.with_user(user)
            if not _rpc_allowed(user):
                raise AccessDenied()

def restricted__exp_authenticate(db, login, password, user_agent_env):
    try:
        _check_user_rpc_allowed(db, login)
    except AccessDenied:
        return False
    else:
        return exp_authenticate(db, login, password, user_agent_env)

def restricted__check(db, uid, passwd):
    res_users = odoo.registry(db)["res.users"]
    with res_users.pool.cursor() as cr:
        self = odoo.api.Environment(cr, uid, {})[res_users._name]
        user = self.browse(uid)
        if not _rpc_allowed(user):
            raise AccessDenied()
    return check(db, uid, passwd)

