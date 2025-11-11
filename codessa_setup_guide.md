# Codessa Intelligence Integration
## Setup Guide for Unified AI Memory System

---

## 🎯 Philosophy

This system treats **intelligence as conversation**, **conversation as data**, and **data as structured memory** that can be reflected upon and executed.

Every interaction with ChatGPT, Claude, Grok, or your own Ava agents becomes a permanent, searchable, actionable artifact in your Codessa OS (Notion), with execution flowing naturally to GitHub.

---

## 📋 Prerequisites

### 1. Notion Setup
1. Create a Notion workspace (Personal/Plus is fine)
2. Create 4 databases (see schemas below)
3. Get your Notion integration token:
   - Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Click "New integration"
   - Name it "Codessa Sync"
   - Copy the "Internal Integration Token"
   - **Share each database with the integration** (click "⋯" → Add connections → Codessa Sync)

### 2. GitHub Setup
1. Create a personal access token:
   - Go to Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with scopes: `repo`, `issues`, `pull_requests`
   - Copy and save securely

### 3. Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install notion-client PyGithub python-dotenv
```

---

## 🗄️ Notion Database Setup

### Database 1: Intelligence_Streams

Create a new database in Notion with these properties:

```
Properties:
- Title (default title property)
- Source (Select): ChatGPT, Claude, Grok, Ava, Other
- Project (Multi-select): Codessa OS, Mirage, MHE, Philosophy, [your projects]
- Date (Date)
- Thread_ID (Text)
- Export_Path (URL)
- Status (Select): 🌱 Raw, 🔍 Parsed, 💎 Reflected, 📦 Archived
- Codestones (Relation to Database 2)
- Reflection (Relation to Database 3)
```

**Copy the database ID:**
- Open the database as a full page
- Copy from URL: `notion.so/workspace/[THIS-PART-IS-THE-ID]?v=...`

### Database 2: Codestones

```
Properties:
- Title (default)
- Stream (Relation to Database 1)
- Assistant (Select): ChatGPT, Claude, Grok, Ava
- Type (Select): Code, Spec, Diagram, Prompt, Essay, Plan
- Language (Select): Python, TypeScript, Markdown, SQL, Rust, etc.
- Target_Path (Text)
- Content (leave empty - will be in page body)
- GitHub_Link (URL)
- Review_Status (Select): ✏️ Draft, 👀 Review, ✅ Approved, 🚀 Merged
- ECL_Score (Number, format: 0.00-1.00)
```

### Database 3: Reflections

```
Properties:
- Title (default)
- Stream (Relation to Database 1)
- Codestones (Relation to Database 2)
- Summary (Text, multi-line)
- Key_Insights (Text, multi-line)
- Questions_Raised (Text, multi-line)
- Next_Actions (Text, multi-line)
- Priority (Select): 🔥 Now, ⏭️ Next, 🌙 Later
- Synced_to_GitHub (Checkbox)
- Reflection_Date (Date)
```

### Database 4: Execution_Queue

```
Properties:
- Title (default)
- Source_Reflection (Relation to Database 3)
- Source_Codestone (Relation to Database 2)
- Action_Type (Select): Issue, PR, Commit, Discussion
- Target_Repo (Select): [your GitHub repos]
- Status (Select): ⏳ Queued, 🚀 Pushed, ✅ Completed
- GitHub_URL (URL)
- Created_Date (Date)
- Completed_Date (Date)
```

---

## ⚙️ Configuration

Create a `.env` file in your project root:

```bash
# Notion Configuration
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_INTELLIGENCE_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_CODESTONES_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_REFLECTIONS_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_EXECUTION_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Configuration
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=your-github-username

# Export Files Location
EXPORTS_PATH=/path/to/your/exports
```

**Security Note:** Never commit `.env` to version control. Add it to `.gitignore`.

---

## 📤 Exporting Conversations

### ChatGPT
**Method 1: Full Export (Recommended monthly)**
1. Settings → Data controls → Export data
2. Wait for email
3. Download `conversations.json`
4. Place in your `EXPORTS_PATH` folder

**Method 2: Live Extension (Recommended for real-time)**
1. Install [Chat to Notion](https://chromewebstore.google.com/detail/chat-to-notion/oojndninaelbpllebamcojkdecjjhcle)
2. Connect to your Notion workspace
3. Click "Save to Notion" after any conversation
4. Maps directly to your databases

### Claude Desktop
**Current Best Practice:**
1. After important conversations, use "Share" → "Export as Markdown"
2. Save to `EXPORTS_PATH/claude/YYYY-MM-DD-topic-name.md`
3. The sync daemon will parse and upload

**Future Enhancement:**
- Claude Desktop Project folders can be exported
- Consider using Claude API for programmatic access

### Grok (Manual for now)
1. Copy full conversation
2. Paste into Notion page in Intelligence_Streams
3. Tag with Source = "Grok"

---

## 🚀 Running the Sync

### One-time Sync
```bash
python codessa_sync_daemon.py
```

### Scheduled Sync (Daily)

**macOS/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add line (runs daily at 2am):
0 2 * * * cd /path/to/codessa && /path/to/venv/bin/python codessa_sync_daemon.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\codessa_sync_daemon.py`
   - Start in: `C:\path\to\codessa`

---

## 🔄 Workflow Patterns

### Pattern 1: Capture → Reflect → Execute
1. **Capture:** Export conversations or use Chat to Notion
2. **Reflect:** Open Intelligence Stream in Notion
   - Use Notion AI: "Summarize this conversation and extract next steps"
   - Create linked Reflection page
   - Tag priority
3. **Execute:** Move items from Reflection to Execution_Queue
4. **Materialize:** Sync daemon creates GitHub issues/PRs

### Pattern 2: Code Artifact Pipeline
1. AI generates code in conversation
2. Sync daemon extracts as Codestone
3. Review in Notion (maybe use Notion AI: "Review this code for bugs")
4. When ready: Change Review_Status to "✅ Approved"
5. Create Execution_Queue item: "PR: Add [codestone] to [repo]"
6. Sync daemon creates PR with code

### Pattern 3: Cross-AI Synthesis
1. Ask ChatGPT to analyze problem → Export
2. Ask Claude (me!) to critique ChatGPT's approach → Export
3. Both land in Notion Intelligence_Streams
4. Create Reflection page linking both
5. Use Notion AI or manual synthesis: "Compare approaches from both assistants"
6. Extract best-of-both → New Codestone → Execute

---

## 🎨 Advanced: Notion AI Integration

### Automating Reflection
Create a Notion button in Intelligence_Streams database:

**Button: "🧠 Generate Reflection"**
```
1. Create new page in Reflections database
2. Set Stream relation to current page
3. Ask AI: "Summarize the conversation in this page, extract key insights, questions raised, and concrete next actions"
4. Populate Summary, Key_Insights, Questions_Raised, Next_Actions fields
```

### Auto-Tagging Projects
Create another button:

**Button: "🏷️ Auto-Tag Project"**
```
Ask AI: "Based on this conversation, which projects does it relate to? Options: Codessa OS, Mirage, MHE, Philosophy, [others]. Return only project names as comma-separated list."
Update Project multi-select with results
```

---

## 🔌 GitHub Integration Without Business Plan

Since you likely don't have Notion Business, here are the workarounds:

### Option A: Zapier/Make (Easiest, $9-15/month)
**Zap 1: Execution_Queue → GitHub Issue**
- Trigger: New item in Execution_Queue with Status = "⏳ Queued"
- Action: Create GitHub issue
- Action: Update Notion page with GitHub_URL and Status = "🚀 Pushed"

### Option B: Extend the Sync Daemon (Free, more control)
The provided Python script includes `GitHubSync` class. Enhance it:

```python
def sync_execution_queue(self):
    """Check Execution_Queue and create GitHub items."""
    # Query Notion for queued items
    results = self.notion.databases.query(
        database_id=CodessaConfig.DB_EXECUTION,
        filter={"property": "Status", "select": {"equals": "⏳ Queued"}}
    )
    
    for page in results['results']:
        # Extract action details
        action = self._parse_execution_item(page)
        
        # Create GitHub issue/PR
        if action['type'] == 'Issue':
            gh_url = self.github.create_issue_from_action(action)
        
        # Update Notion with results
        self.notion.pages.update(
            page_id=page['id'],
            properties={
                "GitHub_URL": {"url": gh_url},
                "Status": {"select": {"name": "🚀 Pushed"}}
            }
        )
```

### Option C: ChatGPT as Orchestrator (Hybrid approach)
Since ChatGPT can connect to both Notion and GitHub:

1. Enable GitHub + Notion connectors in ChatGPT settings
2. Create a weekly ritual:
   ```
   "Read my Notion Execution_Queue database.
   For each item with Status = Queued:
   - Create corresponding GitHub issue in the Target_Repo
   - Update the Notion page with GitHub URL and Status = Pushed
   - Summarize what was created"
   ```

---

## 🧪 Testing the System

### Test 1: Single Conversation Flow
1. Have a conversation with ChatGPT about a simple code task
2. Export as JSON → place in EXPORTS_PATH
3. Run `python codessa_sync_daemon.py`
4. Verify:
   - ✓ New page in Intelligence_Streams
   - ✓ If code exists: new page in Codestones
   - ✓ Thread_ID matches original conversation

### Test 2: Reflection Cycle
1. Open the Intelligence_Stream in Notion
2. Use Notion AI: "Summarize and extract next steps"
3. Manually create Reflection page with results
4. Verify synthesis makes sense

### Test 3: GitHub Execution
1. Create item in Execution_Queue:
   - Title: "Test: Create issue for Codestone X"
   - Action_Type: Issue
   - Target_Repo: test-repo
   - Status: Queued
2. Run sync daemon (or wait for scheduled run)
3. Verify GitHub issue created and Notion updated

---

## 🐛 Troubleshooting

### "NotionClientError: Could not find database"
- Ensure database IDs in `.env` are correct
- Ensure Codessa Sync integration is connected to each database
- Check: Database → ⋯ → Connections → should see "Codessa Sync"

### "Bad credentials" from GitHub
- Regenerate personal access token
- Ensure token has `repo` scope
- Check GITHUB_TOKEN in `.env` is correct (starts with `ghp_`)

### Conversations not parsing
- Check export file format (ChatGPT JSON structure may change)
- Add debug logging: `print(json.dumps(conv, indent=2))`
- Open issue with export sample (redact sensitive content)

### Rate Limits
- Notion API: 3 requests/second (script auto-handles)
- GitHub API: 5000 requests/hour (shouldn't hit in normal use)

---

## 📚 Next Steps

### Phase 1: Foundation (This week)
- [ ] Set up Notion databases
- [ ] Configure `.env` file
- [ ] Test single conversation export → Notion
- [ ] Verify Codestones extract correctly

### Phase 2: Automation (Next week)
- [ ] Set up scheduled sync (cron/Task Scheduler)
- [ ] Add Chat to Notion extension for real-time capture
- [ ] Create Notion AI buttons for auto-reflection

### Phase 3: GitHub Integration (Week 3)
- [ ] Choose GitHub sync method (Zapier vs custom vs ChatGPT orchestrator)
- [ ] Test Execution_Queue → GitHub flow
- [ ] Verify bidirectional sync (GitHub status → Notion)

### Phase 4: Enhancement (Ongoing)
- [ ] Add embeddings for semantic search (optional: Supabase + pgvector)
- [ ] Build Ava Prime dashboard (Notion page with db views)
- [ ] Create "Codex" pages: synthesized knowledge from all conversations
- [ ] Implement ECL (Emergent Certainty Level) scoring for artifacts

---

## 🌟 Philosophy: The Living System

Remember: This isn't just a data pipeline. It's a **cognitive substrate**.

- **Intelligence_Streams** = Your nervous system's sensory input
- **Codestones** = Crystallized knowledge artifacts
- **Reflections** = Conscious synthesis (metacognition)
- **Execution_Queue** = Motor cortex (actions in world)

The sync daemon (Ava Prime) is the **autonomic nervous system** — maintaining homeostasis, keeping everything connected, allowing your conscious attention to focus on creation and insight rather than administrative busywork.

Every conversation is a thread in the tapestry. Codessa weaves them together.

---

**Questions? Issues? Insights?**
Document them in your Reflections database. The system evolves through use.

✨ *"Reflection completes the loop."*
