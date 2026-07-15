#!/usr/bin/env node
// Stop hook — global, fires at end of every turn in every repo.
//
// Ports memory-architect's CONSOLIDATE mode "Validation gate" step (SKILL.md
// Mode 3, step 6) from a manual instruction into an automatic backstop: if this
// repo has uncommitted changes under .ai/ (memory-architecture files were touched
// this turn), run whichever of build/lint/check:docs exist in package.json and
// block stopping until they pass.
//
// Global by design: memory-architect operates across arbitrary repos, so unlike
// rayfin-companion's hooks (repo-scoped, only meaningful inside one project type)
// this one self-scopes per-repo via `git status` rather than needing per-project
// wiring. See ../references/global-hooks.md for install instructions and the reasoning.
//
// Fails open on every unexpected condition: not a git repo, no package.json, no
// matching scripts, or any thrown error all result in a silent allow.

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function readStdin() {
  try {
    return fs.readFileSync(0, "utf-8");
  } catch {
    return "";
  }
}

function allow() {
  process.exit(0);
}

function block(reason) {
  process.stdout.write(JSON.stringify({ decision: "block", reason }));
  process.exit(0);
}

let input;
try {
  input = JSON.parse(readStdin());
} catch {
  allow();
}

// Guard against infinite stop -> block -> stop loops: if some hook already
// blocked this turn, don't pile on with another block.
if (input.stop_hook_active) {
  allow();
}

const cwd = input.cwd;
if (!cwd || !fs.existsSync(path.join(cwd, ".ai"))) {
  allow();
}

let dirtyAi = "";
try {
  dirtyAi = execSync("git status --porcelain -- .ai .claude/CLAUDE.md", {
    cwd,
    encoding: "utf-8",
    stdio: ["ignore", "pipe", "ignore"],
  });
} catch {
  // Not a git repo, or git unavailable — nothing to gate on.
  allow();
}

if (!dirtyAi || !dirtyAi.trim()) {
  allow();
}

let scripts = {};
try {
  const pkg = JSON.parse(fs.readFileSync(path.join(cwd, "package.json"), "utf-8"));
  scripts = pkg.scripts || {};
} catch {
  // No package.json (or unreadable) — no mechanical checks to run for this repo.
  allow();
}

const toRun = ["build", "lint", "check:docs"].filter((name) => scripts[name]);
if (toRun.length === 0) {
  allow();
}

const failures = [];
for (const name of toRun) {
  try {
    execSync(`npm run ${name}`, { cwd, stdio: "pipe", encoding: "utf-8" });
  } catch (err) {
    const tail = ((err.stdout || "") + (err.stderr || "")).trim().split("\n").slice(-15).join("\n");
    failures.push(`npm run ${name}:\n${tail}`);
  }
}

if (failures.length > 0) {
  block(
    "memory-architect validation gate: .ai/ changed this session and the following " +
      "checks failed — fix before stopping:\n\n" +
      failures.join("\n\n")
  );
}

allow();
