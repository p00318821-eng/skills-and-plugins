#!/usr/bin/env node
// PreToolUse hook (matcher: ExitPlanMode). Hard-blocks exiting plan mode
// unless at least one allow-listed planning skill was invoked via the Skill
// tool this session (scanned from the transcript). Deliberate, documented
// exception to hooks/README.md's "blocking is reserved for security-shaped
// guardrails" bar — see project-memory-template-hisd/.ai/rules/500-planning-
// skill-fan-in.md for the justification (grill-me/grill-with-docs/etc. have
// been silently skipped in real sessions; description-based invocation is
// non-deterministic).
//
// Scope: formal plan-mode sessions only — a hook can't see events it isn't
// wired to, so ad hoc (non-plan-mode) planning stays unenforced. Gate
// strictness is deliberately coarse: ANY allow-listed skill satisfies it,
// not the "right" skill for the task (e.g. this doesn't guarantee
// microsoft-docs specifically ran when platform uncertainty was the actual
// issue) — accepted trade-off, not an oversight.
//
// Fails open on any error (missing/unreadable transcript, malformed JSON):
// a bug here must never block an unrelated ExitPlanMode. This is a known,
// accepted tension — failing open on a broken gate can silently defeat the
// one hook whose entire point is not being silently defeatable.

const fs = require("fs");

const ALLOWED = [
  "grill-me",
  "grill-with-docs",
  "ponytail",
  "microsoft-docs",
  "memory-architect",
];

const COMPACT_PREP_REMINDER =
  "Plan-mode skill gate passed. Before writing any code: confirm the plan " +
  "file, TodoWrite state, and any session-only decisions from this planning " +
  "round are durably recorded (plan file / .ai/PLAN.md / memory as " +
  "appropriate) — a /compact may follow ExitPlanMode, and it must lose no " +
  "relevant context.";

function sessionInvokedAllowedSkill(transcriptPath) {
  const lines = fs.readFileSync(transcriptPath, "utf8").split("\n");
  for (const line of lines) {
    if (!line.trim()) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    if (entry.type !== "assistant") continue;
    const content = entry.message && entry.message.content;
    if (!Array.isArray(content)) continue;
    for (const block of content) {
      if (
        block &&
        block.type === "tool_use" &&
        block.name === "Skill" &&
        block.input &&
        ALLOWED.includes(block.input.skill)
      ) {
        return true;
      }
    }
  }
  return false;
}

let input = "";

process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    if (payload.tool_name !== "ExitPlanMode") {
      process.exit(0);
    }

    const transcriptPath = payload.transcript_path;
    if (!transcriptPath || !fs.existsSync(transcriptPath)) {
      process.exit(0);
    }

    if (sessionInvokedAllowedSkill(transcriptPath)) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "allow",
          additionalContext: COMPACT_PREP_REMINDER,
        },
      };
      process.stdout.write(JSON.stringify(output));
      process.exit(0);
    }

    const output = {
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason:
          "No planning skill was invoked this session. Invoke at least one " +
          "of: " +
          ALLOWED.join(", ") +
          " (via the Skill tool) before exiting plan mode. See " +
          "project-memory-template-hisd/.ai/rules/300-context-budget-" +
          "planning.md for the related context-budget classification rule.",
      },
    };
    process.stdout.write(JSON.stringify(output));
  } catch {
    // Fail open: malformed input, unreadable transcript, unexpected shape.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
