# Requesting & Installing a License

TwinCat-MCP is licensed per machine. Activating it is a two-step flow: you
generate a **license request** on the machine that will run the Service, send it
to Qubernetic, and install the **token** you receive back.

## 1. Generate a license request

The request binds your future token to this specific machine.

### From the UI (recommended)

1. Open the **Options** window from the **gear "Options"** button on the TwinCat-MCP toolbar.
2. Select the **Licensing** page.
3. Under **"1 · Generate a license request"**, optionally fill in **Company / Email / First name / Last name** — these are embedded into the token for display only.
4. Click **Generate request**. The request JSON appears in the box and is also saved to:

   ```
   C:\ProgramData\TwinCat-MCP\license-request.json
   ```

5. **Send that JSON (or file) to Qubernetic** at [info@qubernetic.com](mailto:info@qubernetic.com) to receive your token.

### Via the MCP tool

An AI agent (or any MCP client) can do the same with the always-available
`generate_license_request` tool (optional params: `company`, `email`, `first`,
`last`). It returns the request JSON and the saved path.

!!! note
    The request is **not** secret — it only carries your machine identifier and
    the contact details you entered. You can share it freely.

## 2. Install your license token

Once you receive a token (a long string starting with `TCMCP1.`):

### From the UI

1. Options → **Licensing** page → **"2 · Install a license token"**.
2. Paste the full `TCMCP1.…` token.
3. Click **Install license**. The result line shows either:
    - **Installed** — the status card refreshes to **Active**.
    - **Rejected (`<STATUS>`)** — nothing changes; see [What Licensing Gates → Troubleshooting](what-licensing-gates.md#troubleshooting).

### Via the MCP tool

Use the always-available `install_license` tool (param: `token`). It returns
`valid`, `status`, and a human-readable `message`.

!!! tip
    Your token is validated for this machine **before** anything is replaced, so
    a rejected token never overwrites a working license.

## Next

See [What Licensing Gates](what-licensing-gates.md) for how to check your status
and what each tool needs.
