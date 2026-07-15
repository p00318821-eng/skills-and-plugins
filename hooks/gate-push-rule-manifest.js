#!/usr/bin/env node
// PreToolUse hook (matcher: Bash). Blocks `git push` from a repo that has a
// `.ai/` rule directory but no `.ai/rule-manifest.json` — the manifest is how
// a consuming repo pins which template rule-shape it was scaffolded against.
// Stale (but present) manifests only warn, never block. Fails open on any
// parse/fs error: a bug in this gate must never block an unrelated push.
//
// Deliberate, documented exception to hooks/README.md's "blocking is reserved
// for security-shaped guardrails" bar — see .ai/rules/502-rule-shape-
// manifest.md for the justification (unambiguous violation, one-time trivial
// fix, avoids training people to ignore an advisory warning).

const fs = require("fs");
const path = require("path");
const os = require("os");

const HOME = os.homedir();
const TEMPLATE_MANIFEST = path.join(
  HOME,
  "OneDrive - Houston Independent School District",
  "Development",
  "repos",
  "GitHub",
  "project-memory-template-hisd",
  ".ai",
  "rule-manifest.json"
);

// Matches `git push` as a subcommand, not `--help`/`-h` on it.
const PUSH_COMMAND_RE =
  /(^|[;&|]|\s)git\s+(?:-[a-zA-Z-]+\s+)*push\b(?!.*(--help|\s-h\b))/;

function findRepoRoot(startDir) {
  let dir = startDir;
  while (true) {
    if (fs.existsSync(path.join(dir, ".git"))) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) {
      return null;
    }
    dir = parent;
  }
}

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
    if (!PUSH_COMMAND_RE.test(command)) {
      process.exit(0);
    }

    const cwd = payload.cwd || process.cwd();
    const repoRoot = findRepoRoot(cwd);
    if (!repoRoot) {
      process.exit(0);
    }

    const aiDir = path.join(repoRoot, ".ai");
    if (!fs.existsSync(aiDir)) {
      process.exit(0);
    }

    const manifestPath = path.join(aiDir, "rule-manifest.json");
    if (!fs.existsSync(manifestPath)) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason:
            `This repo has a '.ai/' rules directory but no ` +
            `'.ai/rule-manifest.json', so its rule shape isn't pinned to a ` +
            `template version. Create ${manifestPath} with:\n` +
            `{"formatVersion": 1, "shapeVersion": 1}\n` +
            `then push again.`,
        },
      };
      process.stdout.write(JSON.stringify(output));
      process.exit(0);
    }

    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    const templateManifest = JSON.parse(
      fs.readFileSync(TEMPLATE_MANIFEST, "utf8")
    );

    if (manifest.shapeVersion < templateManifest.shapeVersion) {
      const output = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          additionalContext:
            `This repo's rule shapeVersion (${manifest.shapeVersion}) is ` +
            `behind the template's current shapeVersion ` +
            `(${templateManifest.shapeVersion}). See ` +
            `project-memory-template-hisd/.ai/rule-manifest.json's ` +
            `shapeChangelog for what changed, and consider running the ` +
            `memory-architect skill's CONSOLIDATE mode / memory-consolidator ` +
            `agent to help migrate — this is never applied unilaterally.`,
        },
      };
      process.stdout.write(JSON.stringify(output));
    }
  } catch {
    // Fail open: malformed input/manifest, unresolvable repo root, fs errors.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
