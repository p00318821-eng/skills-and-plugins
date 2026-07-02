# Data Models Reference

## Project Layout

```
your-project/
├── rayfin/
│   ├── data/
│   │   ├── schema.ts        ← entity registration map (update on every new entity)
│   │   └── *.ts             ← one file per entity
│   ├── .env                 ← secrets; never commit; use .env.example for docs
│   ├── rayfin.yml
│   └── tsconfig.json        ← CLI-managed; don't edit directly
├── src/                     ← React/Vite frontend
└── rayfin/.temp/            ← generated; never commit
```

## Defining an Entity

```typescript
import { entity, uuid, text, int, decimal, boolean, date, email, set, one, many } from '@microsoft/rayfin-core';

@entity()
export class Product {
  @uuid() id!: string;                                          // auto-generated if omitted at create
  @text() name!: string;
  @decimal() price!: number;
  @int() stockQuantity!: number;
  @boolean({ default: false }) isAvailable!: boolean;
  @date() createdAt!: Date;
  @set('draft', 'published', 'archived') status!: 'draft' | 'published' | 'archived';
  @text({ optional: true }) description?: string;              // { optional: true } = nullable column
}
```

## Field Decorator → DB Type Map

| Decorator | DB Type | TS Type | Notes |
|---|---|---|---|
| `@uuid()` | UNIQUEIDENTIFIER | string | PK only if named `id` |
| `@text()` | NVARCHAR | string | |
| `@int()` | INT | number | |
| `@decimal()` | DECIMAL | number | |
| `@boolean()` | BIT | boolean | |
| `@date()` | DATETIME2 | Date | ISO string or Date object |
| `@email()` | NVARCHAR + validation | string | |
| `@set('a','b')` | NVARCHAR + enum | string literal union | |

## Field Modifiers

| Modifier | Effect |
|---|---|
| `{ optional: true }` | NULL column — **only way to make column nullable** |
| `{ unique: true }` | Unique constraint |
| `{ default: value }` | Default value expression |
| `{ min: n }`, `{ max: n }` | String length or numeric range |

> **CRITICAL**: TypeScript `?` only affects static typing. It does NOT make
> the DB column nullable. You must add `{ optional: true }` to the decorator.
> Use `!` on required fields (initialized by framework).

## Relationships

### One-to-Many

```typescript
import { entity, uuid, text, date, one, many } from '@microsoft/rayfin-core';

@entity()
export class Notebook {
  @uuid() id!: string;
  @text() name!: string;
  @date() createdAt!: Date;
  @many(() => Note) notes?: Note[];                            // parent side
}

@entity()
export class Note {
  @uuid() id!: string;
  @text() title!: string;
  @text() content!: string;
  @date() createdAt!: Date;
  @text() notebook_id!: string;                               // FK field; {property}_id naming only
  @one(() => Notebook) notebook?: Notebook;                   // child side
}
```

FK column auto-generated from `@one()`. Declare FK field explicitly only when
reading/setting it in application code.

### Foreign Key Naming Rule

`{navigationProperty}_id` — always. No exceptions, no overrides.

```
notebook  → notebook_id   ✓
createdBy → createdBy_id  ✓
parentId  → ✗ (wrong naming)
```

### System Entity Exception

Cannot use `@one()` on the built-in `USER` entity. Use plain text field + populate from auth claims:

```typescript
@entity()
export class Task {
  @uuid() id!: string;
  @text() title!: string;
  @text() user_id!: string;    // populate with claims.sub; never @one(() => USER)
}
```

### Many-to-Many

Not supported natively. Use explicit join entity:

```typescript
@entity()
export class TaggedNote {
  @uuid() id!: string;
  @text() note_id!: string;
  @one(() => Note) note?: Note;
  @text() tag_id!: string;
  @one(() => Tag) tag?: Tag;
}
```

## `@role` Decorator

Attach authorization rules at class level. Compiled into RLS policies at `db apply`.

```typescript
@role(roleName, actions, options?)
```

| Param | Type | Values |
|---|---|---|
| `roleName` | string | `'authenticated'` or custom role |
| `actions` | string \| string[] | `'create'`, `'read'`, `'update'`, `'delete'`, `'*'` |
| `options.policy` | callback | `(claims, item) => expression` |
| `options.include` | string[] | Field whitelist (create/update) |
| `options.exclude` | string[] | Field blacklist (read) |

**Claims**: `claims.sub` (user ID), `claims.email`, `claims.role`.
**Operators**: `.eq()`, `.and()`, `.or()`.

### Common Patterns

```typescript
// Owner-only full access
@entity()
@role('authenticated', '*', {
  policy: (claims, item) => claims.sub.eq(item.userId)
})
export class PrivateNote {
  @uuid() id!: string;
  @text() userId!: string;
  @text() content!: string;
}

// Action-split with field filtering
@entity()
@role('authenticated', 'create', {
  policy: (claims, item) => claims.sub.eq(item.createdBy),
  include: ['title', 'content'],
})
@role('authenticated', 'read', {
  policy: (claims, item) => claims.sub.eq(item.createdBy),
})
@role('authenticated', 'update', {
  policy: (claims, item) => claims.sub.eq(item.createdBy),
  exclude: ['adminNotes'],
})
@role('authenticated', 'delete', {
  policy: (claims, item) => claims.sub.eq(item.createdBy),
})
export class SecureDocument {
  @uuid() id!: string;
  @text() title!: string;
  @text({ optional: true }) content?: string;
  @text({ optional: true }) adminNotes?: string;
  @text() createdBy!: string;
}

// Admin override
@entity()
@role('authenticated', ['create', 'read', 'update'], {
  policy: (claims, item) =>
    claims.role.eq('admin').or(claims.sub.eq(item.ownerId))
})
@role('authenticated', 'delete', {
  policy: (claims, _item) => claims.role.eq('admin')
})
export class ManagedResource {
  @uuid() id!: string;
  @text() ownerId!: string;
  @text() name!: string;
}
```

## Schema Registration

Every new entity must be added to `rayfin/data/schema.ts`:

```typescript
import type { Note } from './Note.js';        // .js extension required (ESM)
import type { Notebook } from './Notebook.js';

export type AppSchema = {
  Note: Note;
  Notebook: Notebook;
};
```

## Applying Schema Changes

```bash
npx rayfin up db apply          # standard apply
npx rayfin up db apply --force  # destructive changes (drop column, rename table)
```

> **WARNING**: `--force` can cause irreversible data loss. Review listed
> destructive operations before confirming.
