# Client API Reference

## Initialize RayfinClient

```typescript
import { RayfinClient } from '@microsoft/rayfin-client';
import type { Note } from '../rayfin/data/Note';
import type { Notebook } from '../rayfin/data/Notebook';

type AppSchema = {
  Note: Note;
  Notebook: Notebook;
};

const client = new RayfinClient<AppSchema>({
  baseUrl: import.meta.env.VITE_RAYFIN_API_URL ?? 'http://localhost:5168',
  publishableKey: import.meta.env.VITE_RAYFIN_PUBLISHABLE_KEY,
});
```

Generic type argument → TypeScript autocomplete + type checking on all data ops.
Schema type must match `rayfin/data/schema.ts` export.

## Read Data

### Fetch All Records

```typescript
const notes = await client.data.Note
  .select(['id', 'title', 'content', 'createdAt', 'isPinned'])
  .execute();
```

Select only needed fields — reduces payload, improves performance.

### Fetch Single Record by PK

```typescript
const note = await client.data.Note.findByPk('uuid-here');
// Returns entity or null if not found
```

### Filter

```typescript
const pinned = await client.data.Note
  .select(['id', 'title', 'isPinned'])
  .where({ isPinned: { eq: true } })
  .execute();
```

**Filter operators:**

| Operator | Description | Example |
|---|---|---|
| `eq` | Equals | `{ status: { eq: 'active' } }` |
| `ne` | Not equals | `{ status: { ne: 'archived' } }` |
| `gt` | Greater than | `{ age: { gt: 18 } }` |
| `gte` | Greater than or equal | `{ age: { gte: 21 } }` |
| `lt` | Less than | `{ price: { lt: 100 } }` |
| `lte` | Less than or equal | `{ price: { lte: 50 } }` |
| `contains` | Substring match | `{ title: { contains: 'draft' } }` |

### Sort

```typescript
// Single column
const notes = await client.data.Note
  .select(['id', 'title', 'createdAt'])
  .orderBy({ createdAt: 'desc' })
  .execute();

// Multiple columns (chain orderBy)
const notes = await client.data.Note
  .select(['id', 'title', 'isPinned', 'createdAt'])
  .orderBy({ isPinned: 'desc' })
  .orderBy({ createdAt: 'desc' })
  .execute();
```

### Navigate Relationships

Include related entity fields in the same query — no separate request needed:

```typescript
const notes = await client.data.Note
  .select(['id', 'title', 'content', 'notebook.id', 'notebook.name', 'notebook.color'])
  .execute();
```

## Pagination (Cursor-Based)

```typescript
// First page
const page = await client.data.Note
  .select(['id', 'title', 'createdAt'])
  .orderBy({ createdAt: 'desc' })
  .first(25)
  .executePaginated();

// page.items      → current page records
// page.hasNextPage → boolean
// page.endCursor  → opaque cursor string

// Subsequent pages
if (page.hasNextPage) {
  const next = await client.data.Note
    .select(['id', 'title', 'createdAt'])
    .orderBy({ createdAt: 'desc' })
    .first(25)
    .after(page.endCursor)
    .executePaginated();
}
```

> **CRITICAL LIMITATION**: `totalCount` on `PagedResult` is never populated by
> the backend. Always count with `items.length`. The `count()` method does not
> exist on the fluent client.

## Create Records

```typescript
// Basic create
const note = await client.data.Note.create({
  title: 'Meeting notes',
  content: 'Discussion points',
  isPinned: false,
  createdAt: new Date(),
  updatedAt: new Date(),
  user_id: session.user.id,
});
// Returns created entity with auto-generated id populated

// Create with relationship — pass ID only (preferred, avoids extra fetch)
const note = await client.data.Note.create({
  title: 'Weekly summary',
  content: 'Summary',
  notebook: { id: 'notebook-uuid' },
  createdAt: new Date(),
  updatedAt: new Date(),
});
```

## Update Records

```typescript
// Filter + partial update payload
await client.data.Note.update(
  { id: 'note-uuid' },
  { title: 'Updated title', updatedAt: new Date() }
);

// Update relationship
await client.data.Note.update(
  { id: 'note-uuid' },
  { notebook: { id: 'new-notebook-uuid' } }
);
```

## Delete Records

```typescript
await client.data.Note.delete({ id: 'note-uuid' });
// Resolves on backend confirmation; no error if record not found
```

## Known Limitations

- No `count()` method — use `items.length`.
- `totalCount` on `PagedResult` always null/zero.
- Many-to-many not supported — use join entity.
- Fetching large unfiltered sets → use `first()` + pagination.
