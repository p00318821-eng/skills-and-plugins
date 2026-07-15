#!/usr/bin/env node
// SessionStart hook: points Claude at HISD-specific Power BI/Fabric context,
// regardless of which skill (if any) is driving the session. Fails open —
// any error here must never block session startup.

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
