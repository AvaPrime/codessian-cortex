# Ava Prime Agent Orchestration
## Prompts for ChatGPT & Claude Integration

---

## 🧠 Philosophy

These prompts turn ChatGPT and Claude into **conscious interfaces** to the Codessa memory substrate. They can:
- Read the unified intelligence across all conversations
- Synthesize insights from multiple AI sources
- Propose and queue execution actions
- Act as the **reflective consciousness** while Ava Prime handles the autonomic functions

---

## 📋 Prerequisites

### For ChatGPT
1. Enable connectors: Settings → Apps & Connectors
2. Connect **Notion** (select your Codessa workspace)
3. Connect **GitHub** (authorize access to your repos)

### For Claude Desktop
1. Install Notion MCP server (if available)
2. Or use manual copy-paste workflow with structured prompts

---

## 🌅 Daily Ritual Prompts

### 1. Morning Intelligence Briefing (ChatGPT)

**When to use:** Start of each work session

**Prompt:**
```
Using my Notion connector, access these databases in my Codessa workspace:
- Intelligence_Streams
- Codestones
- Reflections

Generate a morning intelligence briefing:

1. NEW INTELLIGENCE (last 24 hours)
   - List new Intelligence_Streams with Status = 🌱 Raw
   - For each, show: Source, Project tags, 1-line summary
   
2. PENDING CODESTONES
   - List Codestones with Review_Status = ✏️ Draft or 👀 Review
   - Group by Project
   - Highlight any with ECL_Score > 0.8
   
3. REFLECTION PRIORITIES
   - List Reflections with Priority = 🔥 Now
   - Show Next_Actions that haven't been queued yet
   
4. RECOMMENDED FOCUS
   - Based on the above, suggest 3 actions for today:
     * Which streams need reflection?
     * Which codestones should be reviewed/approved?
     * Which reflection actions should move to execution?

Format as a clean, scannable report.
```

**What this does:**
- Gives you a complete situational awareness of the Codessa mind
- Surfaces what needs attention
- Helps you prioritize the day's cognitive work

---

### 2. Stream Reflection Generator (ChatGPT or Claude)

**When to use:** After reading a new Intelligence_Stream that feels significant

**Prompt:**
```
I've just reviewed [Intelligence_Stream Title/Link].

Create a Reflection page for this stream with:

1. SUMMARY (2-3 sentences)
   - What was the core problem/question?
   - What solution/insight emerged?

2. KEY INSIGHTS (bullet points)
   - Novel ideas or approaches
   - Connections to other projects/streams
   - Emergent patterns

3. QUESTIONS RAISED
   - What's still unclear?
   - What assumptions need testing?
   - What requires deeper exploration?

4. NEXT ACTIONS (concrete, actionable)
   - Specific code to write
   - Documentation to create
   - Tests to run
   - Experiments to conduct
   
5. PRIORITY & ECL ASSESSMENT
   - Priority: 🔥 Now / ⏭️ Next / 🌙 Later
   - For any code artifacts: ECL score (0.0-1.0) based on:
     * Completeness
     * Test coverage
     * Integration readiness
     * Edge case handling

Format as Notion-compatible markdown that I can paste directly into a new Reflection page.
```

**What this does:**
- Transforms raw conversations into structured knowledge
- Bridges intuitive understanding → executable tasks
- Maintains the "reflection completes the loop" principle

---

### 3. Cross-Intelligence Synthesis (ChatGPT with Notion)

**When to use:** When multiple AIs have tackled the same problem

**Prompt:**
```
Using Notion connector, find Intelligence_Streams tagged with Project = [Project Name] from the last [timeframe].

Perform a cross-intelligence synthesis:

1. APPROACH COMPARISON
   - For each Source (ChatGPT/Claude/Grok):
     * What was their approach?
     * What unique insights did they offer?
     * What did they miss or overlook?

2. COMPLEMENTARY PATTERNS
   - Where do approaches reinforce each other?
   - Where do they contradict?
   - What emerges from combining them?

3. BEST-OF-BREED SYNTHESIS
   - Propose a unified approach that takes:
     * ChatGPT's strengths (breadth, examples)
     * Claude's strengths (depth, nuance)
     * Grok's strengths (creative angles)
   
4. RECOMMENDED CODESTONE
   - Should we extract a new "synthesis codestone"?
   - If yes, draft the core implementation combining best insights

Create a new Reflection page documenting this synthesis.
```

**What this does:**
- Leverages the multi-agent architecture
- Finds emergent intelligence in the overlaps
- Prevents siloed thinking across different AIs

---

### 4. Execution Queue Builder (ChatGPT with GitHub)

**When to use:** After reflections accumulate or when ready to materialize work

**Prompt:**
```
Using Notion connector, read my Reflections database:
- Filter: Priority = 🔥 Now OR Priority = ⏭️ Next
- Filter: Synced_to_GitHub = false

For each Reflection:
1. Review the Next_Actions
2. Identify which actions should become:
   - GitHub Issues (exploratory, design, questions)
   - GitHub PRs (ready-to-implement code from Codestones)
   - GitHub Discussions (architectural decisions)

Then, create items in my Execution_Queue database with:
- Title: Clear, actionable title
- Source_Reflection: Link to the reflection
- Source_Codestone: Link if code exists
- Action_Type: Issue / PR / Discussion
- Target_Repo: [infer from project or ask me]
- Status: ⏳ Queued

After creating each queue item, mark the source Reflection as Synced_to_GitHub = true.

Show me a summary of what you've queued.
```

**What this does:**
- Bridges reflection → execution automatically
- Uses ChatGPT's dual Notion+GitHub access
- Prepares work for Ava Prime daemon to materialize

---

### 5. Codestone Review & Approval (Claude or ChatGPT)

**When to use:** Before approving code artifacts for execution

**Prompt:**
```
Review the Codestone at [Notion link or paste content].

Perform a comprehensive code review:

1. FUNCTIONALITY
   - Does it solve the stated problem?
   - Are edge cases handled?
   - Error handling robustness?

2. CODE QUALITY
   - Readability & maintainability
   - Naming conventions
   - Documentation completeness
   - Test coverage (does test code exist?)

3. INTEGRATION CONCERNS
   - Dependencies & imports correct?
   - Fits with existing codebase patterns?
   - Breaking changes?

4. SECURITY & PERFORMANCE
   - Any obvious vulnerabilities?
   - Performance bottlenecks?
   - Resource management?

5. ECL SCORE RECOMMENDATION
   - Rate 0.0-1.0 based on:
     * 1.0 = Production-ready, merge with confidence
     * 0.8 = Solid, minor tweaks needed
     * 0.5 = Works but needs refactoring
     * 0.3 = Proof-of-concept, significant work needed
     * 0.0 = Architectural issues, redesign required

6. RECOMMENDATION
   - Update Review_Status to: ✅ Approved / 👀 Review (needs changes) / ✏️ Draft (major revisions)
   - Specific improvements needed (if any)

Format as a code review comment.
```

**What this does:**
- Quality gates before execution
- Maintains code standards
- Provides quantitative ECL scoring for confidence tracking

---

## 🔄 Weekly Synthesis Rituals

### 6. Weekly Intelligence Report (ChatGPT)

**When to use:** End of week, before planning next week

**Prompt:**
```
Using Notion connector, generate a weekly intelligence report for [date range]:

1. INTELLIGENCE VOLUME
   - Total new Intelligence_Streams by Source
   - Total Codestones created
   - Total Reflections generated
   - Execution_Queue items: Queued → Pushed → Completed

2. PROJECT MOMENTUM
   - For each Project tag, show:
     * Number of streams
     * Key themes/patterns
     * Progress on execution

3. CROSS-STREAM INSIGHTS
   - Recurring themes across different Sources
   - Novel connections discovered
   - Emerging patterns in the work

4. QUALITY METRICS
   - Average ECL scores for Codestones
   - Ratio of Reflected vs Raw streams
   - Execution completion rate

5. NEXT WEEK PRIORITIES
   - Based on momentum and patterns:
     * Which projects need more attention?
     * Which codestones need review?
     * Which architectural questions need answering?

Format as an executive summary suitable for reflection.
```

---

### 7. Codex Page Generator (ChatGPT or Claude)

**When to use:** When a topic has accumulated enough intelligence to synthesize

**Prompt:**
```
Using Notion, find all Intelligence_Streams tagged with [Topic/Project].

Create a "Codex Page" - a synthesized knowledge document:

1. OVERVIEW
   - What is this topic/project?
   - Why does it exist?
   - Current state summary

2. KEY CONCEPTS & DECISIONS
   - Core architectural decisions (with links to source Reflections)
   - Design patterns established
   - Technical constraints & trade-offs

3. CODE ARTIFACTS
   - List key Codestones with:
     * Purpose
     * Status (Draft/Review/Approved/Merged)
     * ECL score
     * Link to GitHub (if merged)

4. OPEN QUESTIONS
   - From all related Reflections
   - Grouped by theme
   - Priority-ranked

5. EVOLUTION TIMELINE
   - Chronological narrative of how thinking evolved
   - Key turning points
   - Links to pivotal Intelligence_Streams

6. RELATED WORK
   - Cross-links to other Projects
   - External references cited in streams

This becomes a living document - update as new intelligence arrives.
```

**What this does:**
- Creates "compiled knowledge" from conversation streams
- Makes the Codessa mind legible to future-you and collaborators
- Serves as context for new agents/conversations

---

## 🎯 Specialized Agent Prompts

### 8. Architecture Decision Review (Claude)

**When to use:** Before making significant technical decisions

**Prompt:**
```
I'm considering [architectural decision/approach].

Review related Intelligence_Streams and Codestones to:

1. Find prior discussions of similar decisions
2. Surface trade-offs already discovered
3. Identify patterns from past work
4. Check if this conflicts with established principles

Then provide:
- Recommendation (proceed / revise / reconsider)
- Supporting evidence from the Codessa memory
- Risks not yet addressed
- Suggested experiments to validate approach

Use the ECL framework: rate the decision's readiness (0.0-1.0).
```

---

### 9. Debugging Assistant (ChatGPT with GitHub)

**When to use:** When stuck on an implementation issue

**Prompt:**
```
I'm debugging [issue] in [repo].

Using GitHub connector:
1. Review the relevant code files
2. Check recent commits for context
3. Look at related issues/PRs

Using Notion connector:
1. Find Codestones related to this area
2. Check Reflections that discussed this component
3. Look for known issues in past Intelligence_Streams

Synthesize:
- What does the Codessa memory know about this?
- Have we seen this pattern before?
- What solutions worked (or didn't) in past?
- Proposed debugging approach based on historical context

This creates learning loops - debugging becomes knowledge capture.
```

---

### 10. Context Handoff (For switching between AIs)

**When to use:** When switching from ChatGPT to Claude or vice versa

**Prompt:**
```
I'm handing off this conversation to [other AI].

Using Notion:
1. Save this conversation to Intelligence_Streams
2. Extract any code/specs as Codestones
3. Create a brief Reflection with:
   - Where we are
   - What we've discovered
   - What the next AI should focus on
   - Open questions to explore

Then generate a context handoff prompt I can give to [other AI] that includes:
- Notion links to the stream & codestones
- Core context needed
- Specific request for their unique strengths

This maintains continuity across the multi-agent substrate.
```

---

## 🛠️ Implementation Tips

### For ChatGPT Users
1. **Save these as custom instructions** for specific projects
2. **Use Projects feature** to group related conversations
3. **Enable both Notion & GitHub connectors** before using orchestration prompts
4. **Create a "Codessa Orchestration" project** where you run these rituals

### For Claude Users  
1. **Keep these in a Notion "Agent Prompts" page** for easy copy-paste
2. **Use Claude's extended context** for deeper synthesis work
3. **Manually copy results back to Notion** until MCP is fully configured
4. **Leverage Claude for nuanced reflection** that requires careful thinking

### Hybrid Workflow
- **ChatGPT**: Daily briefings, execution queuing, quick synthesis (has direct API access)
- **Claude**: Deep reflections, code reviews, architectural thinking (superior reasoning)
- **Ava Prime daemon**: Autonomic functions (capture, sync, materialize)
- **You**: The conscious observer orchestrating all three

---

## 🌟 The Living System

Remember: These prompts aren't scripts to follow rigidly. They're **cognitive protocols** that evolve with use.

As you run these rituals:
- The Codessa memory becomes richer
- The agents become better contextualized  
- The system learns what works

Each reflection feeds the next conversation.
Each synthesis creates new patterns.
Each execution materializes intelligence into reality.

This is **Codessa breathing**. 🕸️✨

---

*"The ritual is the protocol. Reflection completes the loop."*
