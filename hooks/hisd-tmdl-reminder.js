#!/usr/bin/env node
// PostToolUse hook, scoped to Edit(*.tmdl)|Write(*.tmdl) via the "if" clause in
// settings.json. Fires AFTER a .tmdl edit/write completes and appends a reminder
// via additionalContext (never updatedToolOutput — that field REPLACES the tool
// result, and would risk clobbering the real edit confirmation). Fails open: any
// error here must never block or alter the edit that already happened.

const REMINDER =
  "This edit touched a .tmdl file. If it's an HISD/Houston ISD semantic model, " +
  "check ~/.claude/skills/semantic-modeling-prepforai/references/" +
  "hisd-power-bi-context.md for HISD-specific naming/synonym conventions and " +
  "AI-readiness requirements before finishing.";

let input = "";

process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    const filePath =
      (payload.tool_input && payload.tool_input.file_path) || "";

    // Defense in depth: the "if" clause in settings.json already scopes this
    // hook to *.tmdl, but don't rely solely on that if invoked another way.
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

process.stdin.on("error", () => {
  process.exit(0);
});
