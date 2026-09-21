{
    "name": "Restricted RPC",
    "version": "16.0.0.0.0",
    "development_status": "Beta",
    "depends": [ ],
    "author": "Som Comunitats SCCL",
    "website": "https://github.com/somcomunitats-coop/odoo-ec-extra",
    "description": "This module restricts access to xml-rpc calls to a set of users that have a specifc group",
    "license": "AGPL-3",
    "demo": [ ],
    "data": [
        "security/security.xml",
    ],
    "post_load": "post_load_hook",
}
