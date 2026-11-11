# Licensing Tools

These three tools are **always available**, even without a valid license, so you can
always get licensed. All other tools require a valid license.

### get_license_status

Returns the license state: valid, status, licensee, expiry, days left.

### generate_license_request

Generates a machine-bound license request to send to Qubernetic.

| Parameter | Description |
|-----------|-------------|
| `company`, `email`, `first`, `last` | Optional contact details shown on the license. |

### install_license

Installs a license token (`TCMCP1.…`). The token is validated before anything is
replaced, so a rejected token never overwrites a working license.

| Parameter | Description |
|-----------|-------------|
| `token` | The full token string. |

See [Requesting & Installing a License](../licensing/requesting-and-installing.md) for
the full flow.
