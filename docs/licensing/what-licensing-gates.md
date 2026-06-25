# What Licensing Gates

## Checking your license status

The **Licensing** page (Options window) shows a **license card** with:

- The **licensee** (company, or "First Last") and an **Active / Inactive** pill.
- **Valid through** date with an expiry progress bar and **days left**.
- The **Issued** date and the machine identifier (with a **Copy** button).
- A **Refresh** button that re-queries the Service.

When there is no valid license, the card shows the reason (for example
*Not licensed* or *Service not connected*).

Programmatically, the `get_license_status` tool returns the same data: `valid`,
`status`, `user_display`, company/email/name, `issued`, `expires`, `days_left`,
and a `message`.

## What is gated

With **no valid license**, only three operations are allowed — so you can always
get yourself licensed:

- `get_license_status`
- `generate_license_request`
- `install_license`

**Every other tool is blocked** until the license is valid; calls return a
`LICENSE_*` error (see below). Starting the **UserMode Runtime (UMR)** is also
gated: if the license isn't valid, the toolbar action shows a warning and opens
the **Licensing** page instead of starting UMR.

### License error codes

| Error code | Status | Meaning |
|------------|--------|---------|
| `LICENSE_REQUIRED` | `MISSING` | No license installed. |
| `LICENSE_EXPIRED` | `EXPIRED` | Past the expiry date. |
| `LICENSE_INVALID` | `INVALID` | Malformed or altered token. |
| `LICENSE_FINGERPRINT_MISMATCH` | `FINGERPRINT_MISMATCH` | Token was issued for a different machine. |
| `LICENSE_TAMPERED` | `TAMPERED` | License integrity check failed — typically the system clock was moved backwards. |

## Troubleshooting

| Symptom | Status | Cause & fix |
|---------|--------|-------------|
| "Service not connected" | — | The Service isn't running or is unreachable. Make sure the TwinCat-MCP Service is up, then click **Refresh**. |
| "Not licensed" | `MISSING` | No token installed. [Generate a request and install a token](requesting-and-installing.md). |
| Rejected on install | `INVALID` | Token truncated or altered. Re-copy the full `TCMCP1.…` string and install again. |
| Rejected / inactive | `FINGERPRINT_MISMATCH` | Token was issued for a different machine. Re-generate the request **on this machine** and request a new token. |
| Inactive after a date | `EXPIRED` | The license expired. Request a renewed token. |
| Inactive, "tampered" | `TAMPERED` | The system clock was moved backwards. Set the clock to the correct time and restart the Service. |

Still stuck? Contact [info@qubernetic.com](mailto:info@qubernetic.com).
