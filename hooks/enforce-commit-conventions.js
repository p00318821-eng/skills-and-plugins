#!/usr/bin/env node
// PreToolUse hook (matcher: Bash). Non-blocking style guardrail backing
// github-mastery's commit-message and branch-naming conventions
// (`type(scope): subject`, `type/scope/description`).
// Warn-only by design: legitimate exceptions (merge commits, revert commits,
// WIP/exploratory branches) are common, so this never denies — it only adds
// additionalContext reminding the agent of the expected format. Mirrors the
// already-decided philosophy that local hooks stay mechanical/non-blocking
// for style/staleness concerns; real teeth belong to security guardrails
// (see guard-credential-leak.js) or a future pre-push check, not this hook.
// Fails open: any error parsing input must never block or warn spuriously.

const TYPES = "feat|fix|refactor|docs|test|chore|ci";

// `-m "message"` or `-m 'message'` on a `git commit` invocation.
const COMMIT_MSG_RE = new RegExp(
  `\\bgit\\s+(?:-[a-zA-Z-]+\\s+)*commit\\b[^|;&]*-m\\s+("([^"]*)"|'([^']*)')`
);
const COMMIT_FORMAT_RE = new RegExp(
  `^(${TYPES})(\\([\\w/-]+\\))?: .{1,72}$`
);

// `git checkout -b <name>` or `git branch <name>` (creation only — a name
// starting with `-` is a flag like `--show-current`/`-a`/`-d`, a query or
// deletion, not a name to validate).
const BRANCH_CREATE_RE =
  /\bgit\s+(?:checkout\s+-b|branch)\s+(?!-)([^\s;&|]+)/;
const BRANCH_FORMAT_RE = new RegExp(`^(${TYPES})/[\\w-]+/[\\w-]+$`);

let input = "";

process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    if (payload.tool_name !== "Bash") {
      process.exit(0);
    }
    const command = (payload.tool_input && payload.tool_input.command) || "";

    const warnings = [];

    const msgMatch = command.match(COMMIT_MSG_RE);
    if (msgMatch) {
      const message = msgMatch[2] !== undefined ? msgMatch[2] : msgMatch[3];
      const subjectLine = message ? message.split("\n")[0] : message;
      if (subjectLine && !COMMIT_FORMAT_RE.test(subjectLine)) {
        warnings.push(
          `Commit message "${subjectLine}" doesn't match the expected ` +
            `\`type(scope): subject\` format (type: ${TYPES.replace(
              /\|/g,
              "/"
            )}; subject imperative, ≤72 chars, no period).`
        );
      }
    }

    const branchMatch = command.match(BRANCH_CREATE_RE);
    if (branchMatch) {
      const name = branchMatch[1];
      if (name && !BRANCH_FORMAT_RE.test(name)) {
        warnings.push(
          `Branch name "${name}" doesn't match the expected ` +
            `\`type/scope/description\` format (type: ${TYPES.replace(
              /\|/g,
              "/"
            )}).`
        );
      }
    }

    if (warnings.length > 0) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          additionalContext: warnings.join(" "),
        },
      };
      process.stdout.write(JSON.stringify(output));
    }
  } catch {
    // Fail open: malformed input, unexpected payload shape, etc. — never
    // block or warn spuriously on an error parsing the command.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
