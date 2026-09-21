import logging

from odoo.service import common, security

from .patch import restricted__exp_authenticate, restricted__check

_logger = logging.getLogger(__name__)


def patch__restricted__exp_authenticate():
    """Patch exp_authenticate method"""
    restricted__exp_authenticate._orig__exp_authenticate = common.exp_authenticate
    common.exp_authenticate = restricted__exp_authenticate
    _logger.info("PATCHED odoo.service.common.exp_authenticate")

def patch__restricted__check():
    """Patch check method"""
    restricted__check._orig__check = security.check
    security.check = restricted__check
    _logger.info("PATCHED odoo.service.security.check")


def post_load_hook():
    patch__restricted__exp_authenticate()
    patch__restricted__check()
