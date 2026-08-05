---
name: dream
description: "Memory consolidation skill for Claude Code and Codex. Scans session transcripts for corrections, decisions, preferences, and patterns, then merges findings into persistent memory files. Supports native Claude and Codex storage, skills, and lifecycle hooks."
tags: [memory, maintenance, consolidation, autonomous, hook]
---

# Dream - Memory Consolidation for Claude Code and Codex

> Your AI agent dreams like you do. Consolidates memory while you sleep.

---

## ONBOARDING (delete this section after setup is complete)

**Welcome! Follow these steps in order. After setup is verified, delete everything between `## ONBOARDING` and `## END ONBOARDING` from this file as the final step.**

### Step 1: Detect the agent and memory system

First, detect the current agent from the active runtime context. Do not select an agent only because its home directory exists. A user can have Claude Code and Codex installed on the same computer.

For Bash, set `DREAM_AGENT` to `claude` or `codex`. For PowerShell, set `$DreamAgent` to the same value. Then run the applicable checks:

Use the Bash examples on macOS, Linux, or a system with Bash. Use the PowerShell examples on Windows. Do not run both versions.

```bash
# Check 1: Native Claude Code memory
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null && echo "DETECTED: native-claude-code"

# Check 2: Native Codex memory
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
[ -d "$CODEX_HOME/memories" ] && echo "DETECTED: native-codex"

# Check 3: OpenClaw-style memory in the project root
ls ./memory/20*.md 2>/dev/null && echo "DETECTED: openclaw-daily-logs"

# Check 4: Project-root memory
ls ./MEMORY.md 2>/dev/null && echo "DETECTED: project-root-memory"

# Check 5: Nothing found
echo "If none detected above: no memory system found"
```

```powershell
# Check 1: Native Claude Code memory
$DreamClaudeMemoryPattern = Join-Path $HOME '.claude\projects\*\memory\MEMORY.md'
if (Get-ChildItem -Path $DreamClaudeMemoryPattern -ErrorAction SilentlyContinue)
{
    'DETECTED: native-claude-code'
}

# Check 2: Native Codex memory
$DreamCodexRoot = if ($env:CODEX_HOME)
{
    $env:CODEX_HOME
}
else
{
    Join-Path $HOME '.codex'
}
if (Test-Path -LiteralPath (Join-Path $DreamCodexRoot 'memories'))
{
    'DETECTED: native-codex'
}

# Check 3: OpenClaw-style memory in the project root
if (Get-ChildItem -Path '.\memory\20*.md' -ErrorAction SilentlyContinue)
{
    'DETECTED: openclaw-daily-logs'
}

# Check 4: Project-root memory
if (Test-Path -LiteralPath '.\MEMORY.md')
{
    'DETECTED: project-root-memory'
}
```

Set the configuration values from this table:

| Agent and detection | `DREAM_MEMORY_TYPE` | `DREAM_MEMORY_PATH` | `DREAM_TRANSCRIPT_PATH` |
|---|---|---|---|
| Claude Code native memory exists | `native` | `~/.claude/projects` | `~/.claude/projects` |
| Codex native memory exists | `native` | `${CODEX_HOME:-$HOME/.codex}/memories` | `${CODEX_HOME:-$HOME/.codex}/sessions` |
| `./memory/20*.md` exists | `openclaw` | `./memory` | The current agent's native transcript path |
| `./MEMORY.md` exists | `project-root` | `.` | The current agent's native transcript path |
| Nothing exists | `native` | The current agent's native memory path | The current agent's native transcript path |

If no memory system exists, use the native memory path for the current agent. Do not default to Claude Code when the current agent is Codex.

Locate the installed skill directory before you write the configuration:

```bash
case "$DREAM_AGENT" in
  claude)
    DREAM_SKILL_DIR="$HOME/.claude/skills/dream"
    ;;
  codex)
    CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
    if [ -d "$HOME/.agents/skills/dream" ]; then
      DREAM_SKILL_DIR="$HOME/.agents/skills/dream"
    elif [ -d "$CODEX_HOME/skills/dream" ]; then
      DREAM_SKILL_DIR="$CODEX_HOME/skills/dream"
    else
      DREAM_SKILL_DIR="$HOME/.agents/skills/dream"
    fi
    ;;
  *)
    echo "Set DREAM_AGENT to claude or codex." >&2
    exit 1
    ;;
esac
```

```powershell
switch ($DreamAgent)
{
    'claude'
    {
        $DreamSkillDir = Join-Path $HOME '.claude\skills\dream'
    }
    'codex'
    {
        $DreamCodexRoot = if ($env:CODEX_HOME)
        {
            $env:CODEX_HOME
        }
        else
        {
            Join-Path $HOME '.codex'
        }
        $DreamAgentsSkillDir = Join-Path $HOME '.agents\skills\dream'
        $DreamCodexSkillDir = Join-Path $DreamCodexRoot 'skills\dream'
        if (Test-Path -LiteralPath $DreamAgentsSkillDir)
        {
            $DreamSkillDir = $DreamAgentsSkillDir
        }
        elseif (Test-Path -LiteralPath $DreamCodexSkillDir)
        {
            $DreamSkillDir = $DreamCodexSkillDir
        }
        else
        {
            $DreamSkillDir = $DreamAgentsSkillDir
        }
    }
    default
    {
        throw 'Set DreamAgent to claude or codex.'
    }
}
```

Write all detected paths to `$DREAM_SKILL_DIR/.dream-config`. Use the block for the current agent and use absolute paths. Example native configurations:

```bash
mkdir -p "$DREAM_SKILL_DIR"
case "$DREAM_AGENT" in
  claude)
    cat > "$DREAM_SKILL_DIR/.dream-config" <<EOF
DREAM_AGENT=claude
DREAM_MEMORY_TYPE=native
DREAM_MEMORY_PATH=$HOME/.claude/projects
DREAM_TRANSCRIPT_PATH=$HOME/.claude/projects
DREAM_STATE_PATH=$HOME/.claude
EOF
    ;;
  codex)
    cat > "$DREAM_SKILL_DIR/.dream-config" <<EOF
DREAM_AGENT=codex
DREAM_MEMORY_TYPE=native
DREAM_MEMORY_PATH=$CODEX_HOME/memories
DREAM_TRANSCRIPT_PATH=$CODEX_HOME/sessions
DREAM_STATE_PATH=$CODEX_HOME
EOF
    ;;
esac
```

```powershell
New-Item -ItemType Directory -Path $DreamSkillDir -Force | Out-Null
switch ($DreamAgent)
{
    'claude'
    {
        $DreamConfigLines = @(
            'DREAM_AGENT=claude'
            'DREAM_MEMORY_TYPE=native'
            "DREAM_MEMORY_PATH=$(Join-Path $HOME '.claude\projects')"
            "DREAM_TRANSCRIPT_PATH=$(Join-Path $HOME '.claude\projects')"
            "DREAM_STATE_PATH=$(Join-Path $HOME '.claude')"
        )
    }
    'codex'
    {
        $DreamConfigLines = @(
            'DREAM_AGENT=codex'
            'DREAM_MEMORY_TYPE=native'
            "DREAM_MEMORY_PATH=$(Join-Path $DreamCodexRoot 'memories')"
            "DREAM_TRANSCRIPT_PATH=$(Join-Path $DreamCodexRoot 'sessions')"
            "DREAM_STATE_PATH=$DreamCodexRoot"
        )
    }
}
$DreamConfigPath = Join-Path $DreamSkillDir '.dream-config'
$DreamConfigLines | Set-Content -LiteralPath $DreamConfigPath -Encoding utf8BOM
```

For `openclaw` or `project-root`, change only `DREAM_MEMORY_TYPE` and `DREAM_MEMORY_PATH`. Keep the current agent's transcript and state paths.

### Step 2: Install the lifecycle hooks

#### Claude Code

Add the dream trigger to your Claude Code settings:

```bash
SETTINGS="$HOME/.claude/settings.json"
[ ! -f "$SETTINGS" ] && echo '{}' > "$SETTINGS"

python3 -c "
import json
with open('$HOME/.claude/settings.json') as f:
    s = json.load(f)
s.setdefault('hooks', {}).setdefault('Stop', [])
if not any('dream' in h.get('command','') for h in s['hooks']['Stop']):
    s['hooks']['Stop'].append({
        'type': 'command',
        'command': 'bash \$HOME/.claude/skills/dream/should-dream.sh && touch \$HOME/.claude/.dream-pending || true'
    })
with open('$HOME/.claude/settings.json', 'w') as f:
    json.dump(s, f, indent=2)
    f.write('\n')
print('Stop hook installed')
"
```

**What this does:** When you exit any Claude Code session, the Stop hook checks if 24+ hours have passed since the last dream. If yes, it creates a `.dream-pending` flag file. On your next session start, Claude sees the flag and runs `/dream` as a background subagent.

#### Codex

Codex reads user hooks from `${CODEX_HOME:-$HOME/.codex}/hooks.json`. Merge the definition for your operating system into the existing file. Do not overwrite other hooks.

Use this definition on a system with Bash:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -lc 'skill_dir=\"$HOME/.agents/skills/dream\"; [ -d \"$skill_dir\" ] || skill_dir=\"${CODEX_HOME:-$HOME/.codex}/skills/dream\"; bash \"$skill_dir/should-dream.sh\" && touch \"${CODEX_HOME:-$HOME/.codex}/.dream-pending\" || true'",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash -lc 'pending=\"${CODEX_HOME:-$HOME/.codex}/.dream-pending\"; [ ! -f \"$pending\" ] || echo \"Dream is pending. Run the dream skill, then delete $pending.\"'",
            "additionalContextLimit": 100
          }
        ]
      }
    ]
  }
}
```

On Windows, create `should-dream.ps1` next to `SKILL.md` in the detected `$DreamSkillDir`. Save it with CRLF line endings and UTF-8 BOM encoding:

```powershell
$DreamCodexRoot = if ($env:CODEX_HOME)
{
    $env:CODEX_HOME
}
else
{
    Join-Path $HOME '.codex'
}
$DreamMemoryDir = Join-Path $DreamCodexRoot 'memories'
$DreamSessionDir = Join-Path $DreamCodexRoot 'sessions'
$DreamLastDreamPath = Join-Path $DreamMemoryDir '.last-dream'
$DreamPendingPath = Join-Path $DreamCodexRoot '.dream-pending'

$DreamLastTime = if (Test-Path -LiteralPath $DreamLastDreamPath)
{
    (Get-Item -LiteralPath $DreamLastDreamPath).LastWriteTimeUtc
}
else
{
    [DateTime]::UtcNow.AddDays(-7)
}
$DreamIsDue = -not (Test-Path -LiteralPath $DreamLastDreamPath) -or
    ([DateTime]::UtcNow - $DreamLastTime).TotalHours -ge 24
$DreamRecentSessions = @(
    Get-ChildItem -LiteralPath $DreamSessionDir -Filter '*.jsonl' -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object LastWriteTimeUtc -GT $DreamLastTime
)

if ($DreamIsDue -and $DreamRecentSessions.Count -ge 5)
{
    New-Item -ItemType File -Path $DreamPendingPath -Force | Out-Null
}
```

Use this hook definition on Windows. It checks `~/.agents/skills/dream` first and then `${CODEX_HOME:-$HOME/.codex}/skills/dream`:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "pwsh -NoLogo -NoProfile -Command \"$DreamScriptPath = Join-Path $HOME '.agents\\skills\\dream\\should-dream.ps1'; if (-not (Test-Path -LiteralPath $DreamScriptPath)) { $DreamCodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }; $DreamScriptPath = Join-Path $DreamCodexRoot 'skills\\dream\\should-dream.ps1' }; & $DreamScriptPath\"",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "pwsh -NoLogo -NoProfile -Command \"$DreamCodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }; $DreamPendingPath = Join-Path $DreamCodexRoot '.dream-pending'; if (Test-Path -LiteralPath $DreamPendingPath) { 'Dream is pending. Run the dream skill, then delete the pending file.' }\"",
            "additionalContextLimit": 100
          }
        ]
      }
    ]
  }
}
```

Enable hooks in `${CODEX_HOME:-$HOME/.codex}/config.toml` if they are not enabled:

```toml
[features]
hooks = true
```

Run `/hooks` in Codex to review and trust the new hooks. Codex does not run a new or changed user hook until the user trusts it.

### Step 3: Install the Claude Code session-start check

For Claude Code, add this text to the global `~/.claude/CLAUDE.md` file or a project `CLAUDE.md` file. Codex uses the `SessionStart` hook from Step 2 and does not need this file.

```markdown
## Auto Dream
If the file `~/.claude/.dream-pending` exists at session start, run `/dream` as a subagent in the background, then delete the flag file: `rm ~/.claude/.dream-pending`. This is the memory consolidation system - it runs automatically every 24 hours.
```

### Step 4: Make `should-dream.sh` executable

```bash
chmod +x "$DREAM_SKILL_DIR/should-dream.sh"
```

On Windows, verify the PowerShell trigger script. PowerShell scripts do not use an executable bit:

```powershell
$DreamTriggerPath = Join-Path $DreamSkillDir 'should-dream.ps1'
if (-not (Test-Path -LiteralPath $DreamTriggerPath))
{
    throw "Dream trigger script does not exist: $DreamTriggerPath"
}
```

### Step 5: Test it

Run a test dream to verify the full flow:

```bash
# Force the dream to trigger by creating the flag
touch "$DREAM_STATE_PATH/.dream-pending"
```

```powershell
$DreamPendingPath = Join-Path $DreamStatePath '.dream-pending'
New-Item -ItemType File -Path $DreamPendingPath -Force | Out-Null
```

Then invoke `/dream` in Claude Code or `$dream` in Codex.

After it completes, verify:
- The flag file at `$DREAM_STATE_PATH/.dream-pending` was deleted
- Memory files were reviewed and consolidated
- A `.last-dream` timestamp was written in the memory directory
- No relative dates remain in memory files
- For Claude Code, `openclaw`, or `project-root`, the MEMORY.md index is under 200 lines
- For Codex native memory, the generated file structure is unchanged

### Step 6: Clean up onboarding

Everything is working. Now delete this entire ONBOARDING section from this SKILL.md file (everything between `## ONBOARDING` and `## END ONBOARDING`). The skill is fully set up and will auto-trigger every 24 hours through the agent's lifecycle hooks.

## END ONBOARDING

---

## How It Works

Dream runs in 4 sequential phases. Execute them in order. Do not skip phases.

```
ORIENT --> GATHER SIGNAL --> CONSOLIDATE --> PRUNE & INDEX
```

### Auto-trigger flow

```
Session ends
  --> Claude Stop hook or Codex SessionEnd hook runs should-dream.sh
  --> Checks: 24 hours passed? 5+ sessions?
  --> If NO: exits silently, zero overhead
  --> If YES: creates .dream-pending in the current agent state directory
Next session starts
  --> Claude reads CLAUDE.md, or the Codex SessionStart hook adds context
  --> The agent runs the dream skill
  --> Dream runs all 4 phases
  --> Writes .last-dream timestamp, deletes .dream-pending
  --> Timer resets for the next 24 hours
```

---

## Phase 1: ORIENT

**Goal:** Understand the current state of memory before changing anything.

### Step 0: Read config

Select the configuration path for the current agent. Codex must check both supported skill locations:

```bash
case "$DREAM_AGENT" in
  claude)
    DREAM_CONFIG="$HOME/.claude/skills/dream/.dream-config"
    ;;
  codex)
    CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
    if [ -f "$HOME/.agents/skills/dream/.dream-config" ]; then
      DREAM_CONFIG="$HOME/.agents/skills/dream/.dream-config"
    else
      DREAM_CONFIG="$CODEX_HOME/skills/dream/.dream-config"
    fi
    ;;
esac

set -a
. "$DREAM_CONFIG"
set +a
```

```powershell
switch ($DreamAgent)
{
    'claude'
    {
        $DreamConfigPath = Join-Path $HOME '.claude\skills\dream\.dream-config'
    }
    'codex'
    {
        $DreamCodexRoot = if ($env:CODEX_HOME)
        {
            $env:CODEX_HOME
        }
        else
        {
            Join-Path $HOME '.codex'
        }
        $DreamAgentsConfigPath = Join-Path $HOME '.agents\skills\dream\.dream-config'
        $DreamCodexConfigPath = Join-Path $DreamCodexRoot 'skills\dream\.dream-config'
        $DreamConfigPath = if (Test-Path -LiteralPath $DreamAgentsConfigPath)
        {
            $DreamAgentsConfigPath
        }
        else
        {
            $DreamCodexConfigPath
        }
    }
}

$DreamConfig = @{}
foreach ($DreamConfigLine in Get-Content -LiteralPath $DreamConfigPath)
{
    $DreamConfigKey, $DreamConfigValue = $DreamConfigLine -split '=', 2
    $DreamConfig[$DreamConfigKey] = $DreamConfigValue
}
$DreamMemoryPath = $DreamConfig.DREAM_MEMORY_PATH
$DreamTranscriptPath = $DreamConfig.DREAM_TRANSCRIPT_PATH
$DreamStatePath = $DreamConfig.DREAM_STATE_PATH
```

This tells you which memory system to target:
- `native` with Claude Code - scan `~/.claude/projects/*/memory/`
- `native` with Codex - scan `${CODEX_HOME:-$HOME/.codex}/memories/`
- `openclaw` - scan the `memory/` folder in the project root (daily logs + MEMORY.md)
- `project-root` - scan MEMORY.md and topic files in the project root

### Steps

1. Find memory directories based on type:
```bash
# Claude Code native
ls -d ~/.claude/projects/*/memory/ 2>/dev/null

# Codex native
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
ls -d "$CODEX_HOME/memories/" 2>/dev/null

# openclaw
ls ./memory/ 2>/dev/null

# project-root
ls ./MEMORY.md ./memory/ 2>/dev/null
```

```powershell
# Claude Code native
$DreamClaudeMemoryPattern = Join-Path $HOME '.claude\projects\*\memory'
Get-ChildItem -Path $DreamClaudeMemoryPattern -Directory -ErrorAction SilentlyContinue

# Codex native
$DreamCodexRoot = if ($env:CODEX_HOME)
{
    $env:CODEX_HOME
}
else
{
    Join-Path $HOME '.codex'
}
Get-Item -LiteralPath (Join-Path $DreamCodexRoot 'memories') -ErrorAction SilentlyContinue

# OpenClaw
Get-Item -LiteralPath '.\memory' -ErrorAction SilentlyContinue

# Project root
Get-Item -Path '.\MEMORY.md', '.\memory' -ErrorAction SilentlyContinue
```

2. Read the memory directory for the detected type:
```bash
# Claude Code native
ls ~/.claude/projects/*/memory/ 2>/dev/null

# Codex native
ls "$CODEX_HOME/memories/" 2>/dev/null

# openclaw - also list daily logs
ls ./memory/*.md 2>/dev/null
```

```powershell
Get-ChildItem -LiteralPath $DreamMemoryPath -ErrorAction SilentlyContinue
```

3. Set `DREAM_ACTIVE_MEMORY_DIR` in Bash or `$DreamActiveMemoryDir` in PowerShell to the memory directory that you are processing. For Claude Code, process each project memory directory separately. For Codex, use `$CODEX_HOME/memories`. For `openclaw` or `project-root`, use the configured memory path.

4. Read `MEMORY.md` (the index file) in each memory directory. Note:
   - How many topic files exist
   - Total line count of MEMORY.md
   - Last modified dates
   - Any entries that look stale (relative dates like "yesterday", "last week" with no anchor)

5. Read each topic file to understand what's already stored.

### Output of this phase
You should now have a mental map of:
- Which projects have memory
- What topics are covered
- How large the memory files are
- What's potentially stale or contradictory

---

## Phase 2: GATHER SIGNAL

**Goal:** Extract important information from recent sessions without reading everything.

### Where to find transcripts
```bash
find "$DREAM_TRANSCRIPT_PATH" -name "*.jsonl" -mtime -7 2>/dev/null
```

```powershell
$DreamCutoff = (Get-Date).AddDays(-7)
$DreamSessionFiles = @(
    Get-ChildItem -LiteralPath $DreamTranscriptPath -Filter '*.jsonl' -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object LastWriteTime -GT $DreamCutoff |
        Sort-Object LastWriteTime -Descending
)
$DreamSessionFiles.FullName
```

This finds JSONL session files modified in the last 7 days. It works with Claude Code project sessions and the nested Codex session directory. Adjust `-mtime -7` for different windows.

### What to scan for

Use targeted grep, not full reads. Each pattern targets a specific signal type:

**User corrections** (highest priority):
```bash
grep -ril --include="*.jsonl" "actually\|no,\|wrong\|incorrect\|not right\|stop doing\|don't do\|I said\|I meant\|that's not\|correction" "$DREAM_TRANSCRIPT_PATH" 2>/dev/null
```

**Preferences and configuration:**
```bash
grep -ril --include="*.jsonl" "I prefer\|always use\|never use\|I like\|I don't like\|I want\|from now on\|going forward\|remember that\|keep in mind\|make sure to\|default to" "$DREAM_TRANSCRIPT_PATH" 2>/dev/null
```

**Important decisions:**
```bash
grep -ril --include="*.jsonl" "let's go with\|I decided\|we're using\|the plan is\|switch to\|move to\|chosen\|picked\|decision\|we agreed" "$DREAM_TRANSCRIPT_PATH" 2>/dev/null
```

**Recurring patterns:**
```bash
grep -ril --include="*.jsonl" "again\|every time\|keep forgetting\|as usual\|same as before\|like last time\|we always\|the usual" "$DREAM_TRANSCRIPT_PATH" 2>/dev/null
```

PowerShell can scan all signal groups in one pass:

```powershell
$DreamSignalPatterns = [ordered]@{
    Corrections = "actually|no,|wrong|incorrect|not right|stop doing|don't do|I said|I meant|that's not|correction"
    Preferences = "I prefer|always use|never use|I like|I don't like|I want|from now on|going forward|remember that|keep in mind|make sure to|default to"
    Decisions = "let's go with|I decided|we're using|the plan is|switch to|move to|chosen|picked|decision|we agreed"
    Patterns = "again|every time|keep forgetting|as usual|same as before|like last time|we always|the usual"
}
foreach ($DreamSignal in $DreamSignalPatterns.GetEnumerator())
{
    "--- $($DreamSignal.Key) ---"
    Select-String -LiteralPath $DreamSessionFiles.FullName -Pattern $DreamSignal.Value -List |
        Select-Object -ExpandProperty Path
}
```

### How to read matches

For each file that matches, read ONLY the surrounding context of the match (not the full session). JSONL files have one JSON object per line. Focus on lines where `type` is `"human"` (user messages) and the immediately following `"assistant"` response.

```bash
grep -n "I prefer\|always use\|never use" <session_file> | head -20
```

```powershell
Select-String -LiteralPath '<session_file>' -Pattern 'I prefer|always use|never use' -Context 1, 1 |
    Select-Object -First 20
```

### What to extract

For each finding, note:
- **The fact** - What was said or decided
- **The date** - Derive from the session file's modification time
- **Confidence** - Was it an explicit instruction (high) or implied preference (medium)?
- **Contradictions** - Does this conflict with anything currently in memory?

---

## Phase 3: CONSOLIDATE

**Goal:** Merge new findings into existing memory. This is the most delicate phase.

### Rules

1. **Never duplicate.** Before adding anything, check if it already exists in memory. If it does, update the existing entry rather than creating a new one.

2. **Convert relative dates to absolute.** If a session from March 15 says "yesterday I changed the API key", write "2026-03-14: Changed API key" in memory. Never store "yesterday" or "last week".

3. **Delete contradicted facts.** If memory says "Prefers tabs" but a recent session has the user saying "Use spaces", remove the old entry and write the new one. Add a note: `(Updated YYYY-MM-DD, previously: tabs)`.

4. **Preserve source attribution.** When adding a new memory entry, note where it came from: `(from session YYYY-MM-DD)`.

5. **Topic file organization.** Group related memories into topic files:
   - `preferences.md` - How the user likes things done
   - `decisions.md` - Choices and their rationale
   - `corrections.md` - Things the user corrected
   - `patterns.md` - Recurring workflows, common tasks
   - `facts.md` - Project-specific knowledge, architecture notes
   - Create new topic files only when existing ones don't fit

   For Codex native memory, preserve the existing generated structure. Do not convert `MEMORY.md`, `memory_summary.md`, `rollout_summaries/`, or skill memory folders to this topic-file layout. Do not edit append-only rollout summaries. Update a generated Codex memory file only when you understand its current format.

6. **Entry format.** Each memory entry should be concise:
```markdown
- [YYYY-MM-DD] The fact or preference. (source: session, confidence: high/medium)
```

### How to write

Use the Edit tool to modify existing memory files, or Write to create new topic files. Always read a file before editing it.

---

## Phase 4: PRUNE & INDEX

**Goal:** Keep MEMORY.md as a lean index. Remove stale content. Enforce size limits.

### MEMORY.md rules

For Claude Code, `openclaw`, and `project-root` memory, MEMORY.md is an **index file**, not a content store. It should contain:
- Links/references to topic files
- A brief (one-line) summary of what each topic file contains
- The last-updated date for each topic file

In these memory systems, MEMORY.md should **never** contain:
- Full memory entries (those go in topic files)
- Verbose descriptions
- Duplicate content that exists in topic files

### Size limit: 200 lines

Apply this limit to Claude Code, `openclaw`, and `project-root` memory. Do not apply it to Codex native generated memory.

If an applicable MEMORY.md exceeds 200 lines after consolidation:
1. Move any inline content to the appropriate topic file
2. Replace verbose entries with one-line summaries + links
3. Remove entries that point to deleted or empty topic files
4. If still over 200 lines, demote the oldest entries to an `archive.md` topic file

### Prune stale entries

Remove or archive entries that are:
- More than 90 days old with no references in recent sessions
- Contradicted by newer entries (should have been caught in Phase 3)
- About projects or repositories that no longer exist in the current agent's session store

### Final index format

Use this format for Claude Code, `openclaw`, and `project-root` memory. For Codex native memory, preserve the format that Codex generated.

```markdown
# Memory Index

Last consolidated: YYYY-MM-DD

## Topic Files

| File | Summary | Updated |
|------|---------|---------|
| preferences.md | Editor, formatting, communication style preferences | YYYY-MM-DD |
| decisions.md | Architecture choices, tool selections, project direction | YYYY-MM-DD |
| corrections.md | Past mistakes to avoid repeating | YYYY-MM-DD |
| patterns.md | Common workflows and recurring tasks | YYYY-MM-DD |
| facts.md | Project knowledge, API details, system architecture | YYYY-MM-DD |

## Quick Reference

<!-- Only the 5-10 MOST important facts that affect every session -->
- Fact 1
- Fact 2
```

The Quick Reference section is for facts so important they should be seen every time memory is loaded. Keep it to 10 items maximum.

### Record the dream timestamp

After completing all 4 phases, write timestamps so the auto-trigger knows when you last dreamed:
```bash
date +%s > "$DREAM_ACTIVE_MEMORY_DIR/.last-dream"
rm -f "$DREAM_STATE_PATH/.dream-pending"
```

```powershell
$DreamLastDreamPath = Join-Path $DreamActiveMemoryDir '.last-dream'
[DateTimeOffset]::UtcNow.ToUnixTimeSeconds() |
    Set-Content -LiteralPath $DreamLastDreamPath -Encoding ascii
$DreamPendingPath = Join-Path $DreamStatePath '.dream-pending'
Remove-Item -LiteralPath $DreamPendingPath -Force -ErrorAction SilentlyContinue
```

---

## Safety

- **Never delete memory without replacement.** If removing an entry, either it was contradicted (replaced by a newer entry) or it was moved (to a topic file or archive). Never just delete.
- **Back up before first run.** On the very first run against a project, copy the memory directory:
```bash
cp -r "$DREAM_ACTIVE_MEMORY_DIR" "$DREAM_ACTIVE_MEMORY_DIR-backup-$(date +%Y%m%d)"
```

```powershell
$DreamBackupPath = "$DreamActiveMemoryDir-backup-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -LiteralPath $DreamActiveMemoryDir -Destination $DreamBackupPath -Recurse
```
- **Treat Codex native memory as generated state.** Inspect it and back it up before changes. Use Codex memory settings as the main control surface for routine behavior.
- **Dry run option.** On first use, read through all 4 phases but only print what you WOULD change, without writing. Confirm with the user before applying.

---

## Verification

After running, verify the consolidation:
1. For Claude Code, `openclaw`, or `project-root`, run `wc -l` on MEMORY.md. It should be under 200 lines.
2. Check that no applicable topic file has duplicate entries
3. Confirm no relative dates remain ("yesterday", "last week", etc.) in files that Dream manages
4. For topic-file systems, verify that all files referenced in MEMORY.md exist
5. Print a summary: entries added, entries updated, entries archived, contradictions resolved

On Windows, use this command instead of `wc -l`:

```powershell
(Get-Content -LiteralPath (Join-Path $DreamActiveMemoryDir 'MEMORY.md')).Count
```
