from xmlrpc.client import Fault

from odoo.tests import tagged
from odoo.tests.common import get_db_name, new_test_user, HttpCase

@tagged("-at_install", "post_install")
class TestRestrictRPC(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.not_allowed_user = new_test_user(cls.env, login="23456789D")
        cls.allowed_user = new_test_user(
			cls.env, login="98765432M",
            groups='base.group_user,restricted_rpc.group_xmlrpc_api_access',
		)
        cls.dbname = get_db_name()

    def test_restricted__exp_authenticate__ok(self):
        # given an allowed user
        # self.allowed_user 
        # if we want to login use the xml-rpc protocol
        uid = self.xmlrpc_common.login(self.dbname, self.allowed_user.login, self.allowed_user.login)

        # then user can be authenticated
        self.assertIsNot(uid, False)

    def test_restricted__exp_authenticate__not_allowed_ok(self):
        # given a not allowed user
        # self.not_allowed_user 
        # if we want to login use the xml-rpc protocol
        uid = self.xmlrpc_common.login(self.dbname, self.not_allowed_user.login, self.not_allowed_user.login)

        # then user can not be authenticated
        self.assertFalse(uid)

    def test_restricted__check__ok(self):
        # given an allowed user
        uid = self.xmlrpc_common.login(self.dbname, self.allowed_user.login, self.allowed_user.login)
        # if we want to execute some function in a model in the database using the xml-rpc protocol
        res = self.xmlrpc_object.execute_kw(self.dbname, uid, self.allowed_user.login, 'res.users', 'search', [[]])

        # then user can doit
        self.assertIsNot(res, False)

    def test_restricted__check__not_allowed_ok(self):
        # given a not allowed user
        uid = self.not_allowed_user.id
        # if we want to execute some function in a model in the database using the xml-rpc protocol
        with self.assertRaises(Fault) as excp:
            self.xmlrpc_object.execute_kw(self.dbname, uid, self.not_allowed_user.login, 'res.users', 'search', [[]])

        # then user cannot do it
        self.assertEqual(excp.exception.faultString, 'Access Denied')