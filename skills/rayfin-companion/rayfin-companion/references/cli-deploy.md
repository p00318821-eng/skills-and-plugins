# CLI & Deployment Reference

## Full `rayfin/rayfin.yml` Specification

All string values support `${VAR}` and `${VAR:-default}` interpolation from
`rayfin/.env` and shell environment.

```yaml
id: my-app           # project slug; Docker Compose name; Fabric item ID
name: my-app         # human-readable display name
version: 1.0.0       # semver

services:
  auth:
    enabled: true
    expiryInMinutes: 60
    refreshToken:
      lifetimeInDays: 30
    customClaims:
      tenant: "default"
    scopes:
      - read:data
      - write:data
    allowedRedirectUris:
      - http://localhost:5173
      - http://localhost:5173/auth/callback
    password:
      enabled: true          # local dev only; disable for production
    fabric:
      enabled: false         # set true for Entra ID SSO in production
    passwordless:
      magicLink:
        enabled: false
        expiryMinutes: 15
      smsOtp:
        enabled: false
    email:
      enabled: false
      provider: smtp
      senderName: Rayfin Platform
      verificationTokenExpirationHours: 24
      passwordResetTokenExpirationMinutes: 30
      smtp:
        host: maildev
        port: 1025
        senderEmail: noreply@rayfin.local
        username: ""
        password: ""
        useSsl: false
        useStartTls: false
        webPort: 1080

  data:
    enabled: true
    dialect: mssql             # only supported dialect

  storage:
    enabled: false

  staticHosting:
    enabled: true
    root: .                    # frontend root dir (relative to project root)
    folder: dist               # build output dir (relative to root)
    buildCommand: npm run build
    indexDocument: index.html
```

**`services.auth` key fields:**

| Field | Default | Description |
|---|---|---|
| `enabled` | false | Enable auth service |
| `expiryInMinutes` | — | JWT token TTL |
| `refreshToken.lifetimeInDays` | — | Refresh token TTL |
| `customClaims` | — | Additional JWT claims map |
| `scopes` | — | OAuth scopes |
| `allowedRedirectUris` | `["http://localhost:5173"]` | Auth callback URIs |
| `password.enabled` | true | Email/password for local dev |
| `fabric.enabled` | false | Entra ID SSO for production |

**`services.staticHosting` key fields:**

| Field | Required | Default | Description |
|---|---|---|---|
| `enabled` | Yes | — | Enable static hosting |
| `folder` | Yes | — | Build output dir relative to `root` |
| `root` | No | project root | Frontend root dir |
| `buildCommand` | No | — | Shell command run before packaging |
| `indexDocument` | No | — | Default doc for directory requests |

**Static hosting limits**: Compressed ZIP must not exceed **100 MB**.

## CLI Command Reference

### Scaffold

```bash
npm create @microsoft/rayfin@latest my-app --workspace <workspace-name>
npx rayfin init [directory]          # add Rayfin to existing project
npx rayfin init --list-templates     # list available templates
npx rayfin init . --template-name react-vite --dialect mssql
```

### Deploy

```bash
npx rayfin up                                         # full deploy (schema + static)
npx rayfin up --dry-run --verbose                     # preview without applying
npx rayfin up --workspace-id <uuid> --yes             # non-interactive deploy
npx rayfin up db apply                                # schema only
npx rayfin up db apply --force                        # destructive schema changes
npx rayfin up staticapp deploy                        # frontend only (fast iteration)
npx rayfin up staticapp deploy --skip-build           # deploy prebuilt dist/
npx rayfin up staticapp deploy --verbose
```

### Status & Management

```bash
npx rayfin up status                 # current deployment status
npx rayfin up status --json          # machine-readable
npx rayfin up list                   # all recorded Fabric deployments
npx rayfin up switch [workspace]     # switch active deployment; rewrites rayfin/.env
npx rayfin up switch --list          # list available deployments
```

### Environment

```bash
npx rayfin env --framework vite      # emit .env.local from rayfin/.env
npx rayfin env --framework vite --show   # preview without writing
npx rayfin env --framework nextjs
```

### Auth

```bash
npx rayfin login                     # interactive sign-in
npx rayfin login --tenant <uuid>     # specific tenant
npx rayfin logout
```

## Vite Environment Variables

| Variable | Source | Purpose |
|---|---|---|
| `VITE_RAYFIN_API_URL` | manual / `.env.local` | Backend base URL |
| `VITE_RAYFIN_PUBLISHABLE_KEY` | manual / `.env.local` | Client auth key |
| `VITE_FABRIC_ITEM_ID` | written by `rayfin up` | Fabric item ID for SSO |
| `VITE_FABRIC_WORKSPACE_ID` | written by `rayfin up` | Fabric workspace ID for SSO |
| `VITE_FABRIC_PORTAL_URL` | written by `rayfin up` | Fabric portal URL for SSO handoff |
| `VITE_RAYFIN_HOSTING_URL` | written by `rayfin up` | Public hosting URL |

Written to `.env.fabric-<workspacename>` and `.env.fabric` during `rayfin up`.

## `.gitignore` Requirements

```
rayfin/.env
rayfin/.temp/
.env.fabric*
```

## Typical Iteration Cycles

**Schema change only** (no frontend change):
```bash
npx rayfin up db apply
# add --force if dropping/renaming columns
```

**Frontend change only** (no schema change):
```bash
npx rayfin up staticapp deploy
# add --skip-build if dist/ already built
```

**Full redeploy**:
```bash
npx rayfin up
```

**Switch workspace** (e.g. dev → staging):
```bash
npx rayfin up switch staging-workspace
# rewrites rayfin/.env with new workspace context
npx rayfin up
```
