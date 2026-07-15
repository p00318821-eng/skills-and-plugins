#!/usr/bin/env node
// PreToolUse hook (matcher: Bash). Blocks `git commit` while checked out on a
// protected branch, regardless of which skill or agent issued the command —
// a systemic guardrail, not a rule an agent has to remember to self-enforce.
// Fails open: any error determining repo state must never block Bash itself.

const { execFileSync } = require("child_process");

const PROTECTED_BRANCHES = new Set(["main", "master", "staging", "develop"]);

// Matches `git commit` as a subcommand, not `--help`/`-h` on it, and not
// unrelated commands that merely mention the word "commit".
const COMMIT_COMMAND_RE =
  /(^|[;&|]|\s)git\s+(?:-[a-zA-Z-]+\s+)*commit\b(?!.*(--help|\s-h\b))/;

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
    if (!COMMIT_COMMAND_RE.test(command)) {
      process.exit(0);
    }

    const cwd = payload.cwd || process.cwd();
    const branch = execFileSync(
      "git",
      ["-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
      { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }
    ).trim();

    if (PROTECTED_BRANCHES.has(branch)) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason:
            `Direct commits to '${branch}' are not allowed. Create a feature ` +
            `branch first (e.g. \`git checkout -b feat/scope/description\`), ` +
            `commit there, then open a PR.`,
        },
      };
      process.stdout.write(JSON.stringify(output));
    }
  } catch {
    // Fail open: not a git repo, git not resolvable, malformed input, etc. —
    // never block Bash on an error determining repo state.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
