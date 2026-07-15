#!/usr/bin/env node
// PostToolUse hook (matcher: Edit|Write, global). Detects edits/writes landing in a
// known *downstream* install copy (a skill/hook/agent folder that's actually
// a mirror of the canonical upstream repo) and warns — non-blocking — that
// the change may also need to land upstream. Mechanical path-prefix matching
// only, no git/content diffing. Fails open: any error must never block or
// alter the edit/write that already happened.
//
// Motivating case: task 7's own hook (suggest-planning-skills.js) was
// written straight to ~/.claude/hooks/ and never landed in the canonical
// skills-plugins-hooks-agents/hooks/ repo — exactly the drift this detects.

const fs = require("fs");
const path = require("path");
const os = require("os");

const HOME = os.homedir();
const UPSTREAM_REPO = path.join(
  HOME,
  "OneDrive - Houston Independent School District",
  "Development",
  "repos",
  "GitHub",
  "skills-plugins-hooks-agents"
);

// Ordered list of downstream roots -> upstream subfolder. First match wins.
const ROOTS = [
  { downstream: path.join(HOME, ".claude", "skills"), upstream: path.join(UPSTREAM_REPO, "skills") },
  { downstream: path.join(HOME, ".agents", "skills"), upstream: path.join(UPSTREAM_REPO, "skills") },
  { downstream: path.join(HOME, ".copilot", "skills"), upstream: path.join(UPSTREAM_REPO, "skills") },
  { downstream: path.join(HOME, ".claude", "hooks"), upstream: path.join(UPSTREAM_REPO, "hooks") },
  { downstream: path.join(HOME, ".claude", "agents"), upstream: path.join(UPSTREAM_REPO, "agents") },
];

const COPILOT_INSTRUCTIONS = path.join(HOME, ".github", "copilot-instructions.md");

function normalize(p) {
  return p.replace(/\\/g, "/");
}

let input = "";

process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    const filePath = (payload.tool_input && payload.tool_input.file_path) || "";
    if (!filePath) {
      process.exit(0);
    }

    const normalizedFile = normalize(filePath);

    if (normalize(COPILOT_INSTRUCTIONS) === normalizedFile) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext:
            "This edit touched ~/.github/copilot-instructions.md, a generated " +
            "downstream artifact — check destinations-matrix.csv in " +
            "skills-plugins-hooks-agents for the render policy that produces it.",
        },
      };
      process.stdout.write(JSON.stringify(output));
      process.exit(0);
    }

    for (const root of ROOTS) {
      const normalizedRoot = normalize(root.downstream);
      if (normalizedFile.startsWith(normalizedRoot + "/")) {
        const suffix = normalizedFile.slice(normalizedRoot.length);
        const upstreamPath = normalize(root.upstream) + suffix;
        const exists = fs.existsSync(upstreamPath);
        const phrase = exists
          ? `update it there too: ${upstreamPath}`
          : `this may be a new file — add it upstream: ${upstreamPath}`;

        const output = {
          hookSpecificOutput: {
            hookEventName: "PostToolUse",
            additionalContext:
              `This edit landed in a downstream install copy (${normalizedRoot}). ` +
              `If this fix should persist past the next resync, ${phrase}.`,
          },
        };
        process.stdout.write(JSON.stringify(output));
        process.exit(0);
      }
    }
  } catch {
    // Fail open: malformed input, unexpected payload shape, fs errors, etc.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
