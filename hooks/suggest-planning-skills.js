#!/usr/bin/env node
// PreToolUse hook (matcher: EnterPlanMode). Non-blocking planning-phase
// skill fan-in nudge: cheap, mechanical project-type detection (file/dir
// presence only) surfacing relevant planning skills to consider via
// additionalContext. Never blocks, never invokes anything, and does not
// attempt to detect discovery-vs-design "session stage" (no real signal
// for that exists today — see .ai/rules/500-planning-skill-fan-in.md).
// Fails open: any error must never block or warn spuriously.

const fs = require("fs");
const path = require("path");

function hasAny(dir, names) {
  return names.some((name) => fs.existsSync(path.join(dir, name)));
}

function hasExt(dir, exts) {
  let entries;
  try {
    entries = fs.readdirSync(dir);
  } catch {
    return false;
  }
  return entries.some((entry) => exts.some((ext) => entry.endsWith(ext)));
}

let input = "";

process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input);
    const cwd = payload.cwd;
    if (!cwd || !fs.existsSync(cwd)) {
      process.exit(0);
    }

    const suggestions = ["`/grilling` (grill-me) for general planning rigor"];

    if (fs.existsSync(path.join(cwd, ".ai"))) {
      suggestions.push(
        "this repo already uses the memory-architecture (`.ai/` present) — " +
          "consider `/grill-with-docs` and memory-architect's AUDIT mode"
      );
    } else {
      suggestions.push(
        "no `.ai/` directory yet — consider memory-architect's SCAFFOLD mode"
      );
    }

    if (hasExt(cwd, [".pbip", ".tmdl"])) {
      suggestions.push(
        "Power BI/Fabric files detected — consider `fabric-skills` / " +
          "`semantic-model-authoring` for Fabric-specific planning"
      );
    }

    if (hasExt(cwd, [".bicep", ".tf"])) {
      suggestions.push(
        "Azure infra files detected — consider `azure-enterprise-infra-" +
          "planner` / `azure-prepare`"
      );
    }

    if (
      !hasExt(cwd, [".pbip", ".tmdl", ".bicep", ".tf"]) &&
      !hasAny(cwd, [".ai"])
    ) {
      suggestions.push(
        "no other project-type signal found — consider `wiki-architect` " +
          "for onboarding/architecture mapping of an unfamiliar codebase"
      );
    }

    const output = {
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        additionalContext:
          "Planning skills to consider this round: " + suggestions.join("; ") + ".",
      },
    };
    process.stdout.write(JSON.stringify(output));
  } catch {
    // Fail open: malformed input, unexpected payload shape, fs errors, etc.
  }
  process.exit(0);
});

process.stdin.on("error", () => {
  process.exit(0);
});
