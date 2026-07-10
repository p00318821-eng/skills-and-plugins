# Global Hooks (reference copy)

This skill's HISD context is delivered to Claude Code via two **global** hooks — they live
outside this repo, in the user's own `~/.claude/settings.json` and `~/.claude/hooks/`, so
they fire regardless of which repo or which skill (this one, a vendored plugin, or none)
is driving an edit. This file is a courtesy copy for reference; it is **not** wired into
this repo's distribution and there is no automated sync between this copy and the live
global config — the same caveat pattern `.ai/LINEAGE.md` uses for its own Standard. If the
live config drifts from this copy, trust the live config and update this file to match.

**Version prerequisite:** the `if`-field glob-scoping syntax on `PostToolUse` requires
Claude Code v2.1.85+.

## `~/.claude/settings.json` (hooks section)

```jsonc
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"$HOME/.claude/hooks/hisd-session-start.js\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "if": "Edit(*.tmdl)|Write(*.tmdl)",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$HOME/.claude/hooks/hisd-tmdl-reminder.js\""
          }
        ]
      }
    ]
  }
}
```

## `~/.claude/hooks/hisd-session-start.js`

Fires once per session. Emits a static string — no file I/O at hook-execution time, zero
failure surface. Fails open (any error → emit nothing, session starts normally).

```js
#!/usr/bin/env node
try {
  const output = {
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext:
        "If working on an HISD/Houston ISD Power BI or Fabric semantic model this " +
        "session, read ~/.claude/skills/semantic-modeling-prepforai/references/" +
        "hisd-power-bi-context.md for HISD-specific naming/synonym conventions and " +
        "AI-readiness templates.",
    },
  };
  process.stdout.write(JSON.stringify(output));
} catch {
  // Fail open: emit nothing, session starts normally without the pointer.
}
process.exit(0);
```

## `~/.claude/hooks/hisd-tmdl-reminder.js`

Fires after any `.tmdl` edit/write (scoped by the `if` clause above), regardless of which
skill drove it. Appends a reminder via `hookSpecificOutput.additionalContext` — **not**
`updatedToolOutput`, which *replaces* the tool result rather than appending to it and would
risk clobbering the real edit confirmation. Fails open.

```js
#!/usr/bin/env node
const REMINDER =
  "This edit touched a .tmdl file. If it's an HISD/Houston ISD semantic model, " +
  "check ~/.claude/skills/semantic-modeling-prepforai/references/" +
  "hisd-power-bi-context.md for HISD-specific naming/synonym conventions and " +
  "AI-readiness requirements before finishing.";

let input = "";
process.stdin.on("data", (chunk) => { input += chunk; });
process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    const filePath = (payload.tool_input && payload.tool_input.file_path) || "";
    if (!filePath.toLowerCase().endsWith(".tmdl")) {
      process.exit(0);
    }
    const output = {
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: REMINDER,
      },
    };
    process.stdout.write(JSON.stringify(output));
  } catch {
    // Fail open: emit nothing, edit result reaches Claude unmodified.
  }
  process.exit(0);
});
process.stdin.on("error", () => { process.exit(0); });
```
