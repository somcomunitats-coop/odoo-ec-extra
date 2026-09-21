# Restricted RPC

This addon restrict xml-rpc calls to a specific users group.

## Configuration
Append this addon in your `server_wide_modules` config

```
server_wide_modules = base,web,sentry,base_sparse_field,queue_job,restricted_rpc
```

## Changelog

### 2026-09-07 (v16.0.0.0.0)
- Restrict authentication login only to `group_xmlrpc_api_access` 
