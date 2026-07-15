#!/usr/bin/env node
// PreToolUse hook (matcher: Bash). Blocks `git commit` whenever a staged file
// matches a known sensitive-file pattern (.env, private keys, credentials
// JSON, etc.), regardless of which skill or agent issued the commit — a
// systemic guardrail backing github-mastery's Guardrail 2.
// Checks the actual staged file list (git diff --cached --name-only), not
// the raw command text, so it catches `git add -A`/`git add .` too.
// Fails open: any error determining repo/staged state must never block Bash.

const { execFileSync } = require("child_process");

// Matches `git commit` as a subcommand, not `--help`/`-h` on it, and not
// unrelated commands that merely mention the word "commit".
const COMMIT_COMMAND_RE =
  /(^|[;&|]|\s)git\s+(?:-[a-zA-Z-]+\s+)*commit\b(?!.*(--help|\s-h\b))/;

const SENSITIVE_PATH_RES = [
  /(^|\/)\.env(\..+)?$/,
  /\.key$/,
  /\.pem$/,
  /\.pfx$/,
  /(^|\/)id_rsa(\.pub)?$/,
  /(^|\/)credentials\.json$/,
  /(^|\/)service[-_]account.*\.json$/,
];

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
    const staged = execFileSync(
      "git",
      ["-C", cwd, "diff", "--cached", "--name-only"],
      { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }
    )
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    const hit = staged.find((path) =>
      SENSITIVE_PATH_RES.some((re) => re.test(path))
    );

    if (hit) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason:
            `Blocked by guard-credential-leak: staged file '${hit}' matches a ` +
            `sensitive-file pattern (.env/.key/.pem/.pfx/id_rsa/credentials.json/` +
            `service-account json). Unstage it (\`git restore --staged ${hit}\`) ` +
            `and add it to .gitignore before committing.`,
        },
      };
      process.stdout.write(JSON.stringify(output));
    }
  } catch {
    // Fail open: not a git repo, git not resolvable, malformed input, etc. —
    // never block Bash on an error determining repo/staged state.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
