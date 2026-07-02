# Authentication Reference

## `rayfin.yml` Auth Config

```yaml
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
      enabled: true      # local dev email/password; disable in production
    fabric:
      enabled: true      # Entra ID SSO for deployed apps
```

When both `staticHosting` and `fabric.auth` are enabled, `npx rayfin up`
auto-registers the deployed app's callback URI in `allowedRedirectUris`.

## Local Dev Authentication

```typescript
await client.auth.signIn({ email, password });
await client.auth.signOut();
client.auth.onSessionChange((session) => { /* react to auth state */ });
const session = client.auth.getSession();
```

Client automatically attaches session to all subsequent data API calls.

## Fabric SSO (`@microsoft/rayfin-auth-provider-fabric`)

Install only if not already scaffolded by template:
```bash
npm install @microsoft/rayfin-auth-provider-fabric
```

### How the Handoff Flow Works

`ensureSignedInWithFabric()` runs a four-step waterfall:
1. Return existing session (cached) — safe on page load.
2. Silent refresh via refresh token — safe on page load.
3. Embedded mode (app in Fabric iframe) — safe on page load; acquires session
   via `postMessage` to parent frame without popup.
4. Popup flow — opens Fabric portal → Entra ID → PKCE handoff →
   session tokens. **Must run inside synchronous user-gesture handler**
   (onClick, not page load, not async chain before interaction).

Steps 1–3 run automatically before step 4. Call `ensureSignedInWithFabric()`
unconditionally from a button handler — it won't open a popup if already
authenticated.

### Core API

```typescript
import { ensureSignedInWithFabric, initEmbeddedAuth } from '@microsoft/rayfin-auth-provider-fabric';

const fabricOptions = {
  workspaceId:     import.meta.env.VITE_FABRIC_WORKSPACE_ID,
  projectId:       import.meta.env.VITE_FABRIC_ITEM_ID,
  fabricPortalUrl: import.meta.env.VITE_FABRIC_PORTAL_URL,
  returnOrigin:    window.location.origin,   // bare origin; NO trailing path
};

// Popup sign-in — call ONLY from onClick or equivalent synchronous handler
const session = await ensureSignedInWithFabric(client.auth, fabricOptions);
if (session.isAuthenticated && session.user) {
  console.log('Signed in:', session.user.email);
}

// Embedded mode — safe to call on page load
// Returns null when not in Fabric iframe (safe to call unconditionally)
const session = await initEmbeddedAuth(client.auth, fabricOptions);
```

`returnOrigin` must be a bare origin: `https://app.contoso.com` ✓
Not: `https://app.contoso.com/` ✗ or `https://app.contoso.com/auth` ✗

### `useFabricAuth` React Hook

```typescript
import { useState, useEffect, useCallback } from 'react';
import { ensureSignedInWithFabric } from '@microsoft/rayfin-auth-provider-fabric';
import { client } from './lib/rayfin';

const fabricOptions = {
  workspaceId:     import.meta.env.VITE_FABRIC_WORKSPACE_ID,
  projectId:       import.meta.env.VITE_FABRIC_ITEM_ID,
  fabricPortalUrl: import.meta.env.VITE_FABRIC_PORTAL_URL,
  returnOrigin:    window.location.origin,
};

export function useFabricAuth() {
  const [session, setSession] = useState(client.auth.getSession());

  useEffect(() => client.auth.onSessionChange(setSession), []);

  const signIn = useCallback(async () => {
    const result = await ensureSignedInWithFabric(client.auth, fabricOptions);
    setSession(result);
    return result;
  }, []);

  const signOut = useCallback(async () => {
    await client.auth.signOut();
  }, []);

  return {
    session,
    signIn,
    signOut,
    isAuthenticated: session?.isAuthenticated ?? false,
  };
}
```

### Usage in Components

```typescript
function App() {
  const { isAuthenticated, signIn, signOut } = useFabricAuth();

  if (!isAuthenticated) {
    return <button onClick={signIn}>Sign in with Fabric</button>;
  }
  return (
    <>
      <Dashboard />
      <button onClick={signOut}>Sign out</button>
    </>
  );
}
```

### Embedded Mode on Startup

Call `initEmbeddedAuth()` early in app entry point to silently acquire session
when app opens inside Fabric portal (no click required):

```typescript
// main.tsx or app entry
import { initEmbeddedAuth } from '@microsoft/rayfin-auth-provider-fabric';
import { client } from './lib/rayfin';

const session = await initEmbeddedAuth(client.auth, {
  workspaceId:     import.meta.env.VITE_FABRIC_WORKSPACE_ID,
  projectId:       import.meta.env.VITE_FABRIC_ITEM_ID,
  fabricPortalUrl: import.meta.env.VITE_FABRIC_PORTAL_URL,
  returnOrigin:    window.location.origin,
});
// session is null when not in embedded mode — no-op, safe to ignore
```

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Popup blocked | Move `ensureSignedInWithFabric()` directly into `onClick` handler |
| `returnOrigin` mismatch | Must match an entry in `allowedRedirectUris` exactly |
| Session lost on refresh | Refresh token handles this; verify `refreshToken.lifetimeInDays` set |
| Embedded mode never fires | Verify `VITE_FABRIC_ITEM_ID` and `VITE_FABRIC_WORKSPACE_ID` are set |
