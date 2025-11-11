"""
Codessa Sync Daemon (Ava Prime)
===============================
Orchestrates intelligence flow between AI assistants, Notion, and GitHub.

Setup:
1. pip install notion-client PyGithub python-dotenv
2. Create .env file with:
   NOTION_TOKEN=secret_xxx
   NOTION_INTELLIGENCE_DB=xxx
   NOTION_CODESTONES_DB=xxx
   NOTION_REFLECTIONS_DB=xxx
   NOTION_EXECUTION_DB=xxx
   GITHUB_TOKEN=ghp_xxx
   GITHUB_OWNER=your-username
   EXPORTS_PATH=/path/to/exports
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from github import Github

load_dotenv()

# ==================== CONFIGURATION ====================

class CodessaConfig:
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")
    EXPORTS_PATH = Path(os.getenv("EXPORTS_PATH", "./exports"))
    
    # Notion Database IDs
    DB_INTELLIGENCE = os.getenv("NOTION_INTELLIGENCE_DB")
    DB_CODESTONES = os.getenv("NOTION_CODESTONES_DB")
    DB_REFLECTIONS = os.getenv("NOTION_REFLECTIONS_DB")
    DB_EXECUTION = os.getenv("NOTION_EXECUTION_DB")

# ==================== PARSERS ====================

class ConversationParser:
    """Parse conversations from different AI assistants."""
    
    @staticmethod
    def parse_chatgpt_export(file_path: Path) -> Dict:
        """Parse ChatGPT conversations.json export."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        for conv in data:
            # Extract messages
            messages = []
            if 'mapping' in conv:
                for node_id, node in conv['mapping'].items():
                    msg = node.get('message')
                    if msg and msg.get('content'):
                        role = msg.get('author', {}).get('role', 'unknown')
                        content_parts = msg['content'].get('parts', [])
                        text = '\n'.join(str(part) for part in content_parts if part)
                        
                        if text.strip():
                            messages.append({
                                'role': role,
                                'content': text,
                                'timestamp': msg.get('create_time')
                            })
            
            conversations.append({
                'source': 'ChatGPT',
                'thread_id': conv.get('id', 'unknown'),
                'title': conv.get('title', 'Untitled'),
                'created': conv.get('create_time'),
                'messages': messages
            })
        
        return conversations
    
    @staticmethod
    def parse_claude_markdown(file_path: Path) -> Dict:
        """Parse Claude conversation exported as markdown."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parser: split on user/assistant markers
        messages = []
        current_role = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('# ') or line.startswith('## '):
                # Assume headers indicate role switches
                if current_role and current_content:
                    messages.append({
                        'role': current_role,
                        'content': '\n'.join(current_content).strip()
                    })
                    current_content = []
                
                if 'user' in line.lower():
                    current_role = 'user'
                elif 'assistant' in line.lower() or 'claude' in line.lower():
                    current_role = 'assistant'
            else:
                current_content.append(line)
        
        # Add final message
        if current_role and current_content:
            messages.append({
                'role': current_role,
                'content': '\n'.join(current_content).strip()
            })
        
        return [{
            'source': 'Claude',
            'thread_id': file_path.stem,
            'title': file_path.stem.replace('_', ' ').title(),
            'created': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
            'messages': messages
        }]

# ==================== ARTIFACT EXTRACTOR ====================

class ArtifactExtractor:
    """Extract code and other artifacts from conversations."""
    
    # Regex to find code blocks
    CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    
    @staticmethod
    def extract_artifacts(messages: List[Dict]) -> List[Dict]:
        """Extract code blocks and other artifacts from messages."""
        artifacts = []
        
        for msg in messages:
            if msg['role'] != 'assistant':
                continue
            
            content = msg['content']
            
            # Find all code blocks
            for match in ArtifactExtractor.CODE_BLOCK_PATTERN.finditer(content):
                language = match.group(1) or 'text'
                code = match.group(2).strip()
                
                if len(code) < 20:  # Skip trivial snippets
                    continue
                
                # Infer artifact type
                artifact_type = 'Code'
                if language.lower() in ['markdown', 'md', 'text']:
                    artifact_type = 'Spec'
                elif language.lower() in ['mermaid', 'dot']:
                    artifact_type = 'Diagram'
                
                # Try to extract title from nearby text
                title = ArtifactExtractor._infer_title(code, language)
                
                artifacts.append({
                    'type': artifact_type,
                    'language': language,
                    'content': code,
                    'title': title
                })
        
        return artifacts
    
    @staticmethod
    def _infer_title(code: str, language: str) -> str:
        """Try to infer a title from code content."""
        # Look for common title patterns
        patterns = [
            r'^#\s+(.+)$',  # Markdown header
            r'^class\s+(\w+)',  # Python/JS class
            r'^def\s+(\w+)',  # Python function
            r'^function\s+(\w+)',  # JS function
            r'^\s*\/\/\s*(.+)$',  # Single-line comment
        ]
        
        for pattern in patterns:
            match = re.search(pattern, code, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return f"{language}_artifact"

# ==================== NOTION SYNC ====================

class NotionSync:
    """Sync conversations and artifacts to Notion."""
    
    def __init__(self):
        self.notion = NotionClient(auth=CodessaConfig.NOTION_TOKEN)
    
    def create_intelligence_stream(self, conv: Dict) -> str:
        """Create a page in Intelligence_Streams database."""
        properties = {
            "Title": {
                "title": [{"text": {"content": f"{conv['source']} – {conv['title']}"}}]
            },
            "Source": {"select": {"name": conv['source']}},
            "Thread_ID": {"rich_text": [{"text": {"content": conv['thread_id']}}]},
            "Date": {"date": {"start": conv['created'][:10]}},
            "Status": {"select": {"name": "🌱 Raw"}}
        }
        
        # Add full conversation as page content
        children = []
        for msg in conv['messages']:
            role_emoji = "👤" if msg['role'] == 'user' else "🤖"
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": f"{role_emoji} {msg['role'].title()}"}}]
                }
            })
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": msg['content'][:2000]}}]  # Notion limit
                }
            })
        
        page = self.notion.pages.create(
            parent={"database_id": CodessaConfig.DB_INTELLIGENCE},
            properties=properties,
            children=children[:100]  # Notion API limits blocks per request
        )
        
        return page['id']
    
    def create_codestone(self, artifact: Dict, stream_id: str) -> str:
        """Create a page in Codestones database."""
        properties = {
            "Title": {
                "title": [{"text": {"content": artifact['title']}}]
            },
            "Stream": {"relation": [{"id": stream_id}]},
            "Type": {"select": {"name": artifact['type']}},
            "Language": {"select": {"name": artifact['language']}},
            "Review_Status": {"select": {"name": "✏️ Draft"}}
        }
        
        children = [{
            "object": "block",
            "type": "code",
            "code": {
                "language": artifact['language'].lower(),
                "rich_text": [{"text": {"content": artifact['content'][:2000]}}]
            }
        }]
        
        page = self.notion.pages.create(
            parent={"database_id": CodessaConfig.DB_CODESTONES},
            properties=properties,
            children=children
        )
        
        return page['id']

# ==================== GITHUB SYNC ====================

class GitHubSync:
    """Sync execution queue to GitHub."""
    
    def __init__(self):
        self.gh = Github(CodessaConfig.GITHUB_TOKEN)
        self.owner = CodessaConfig.GITHUB_OWNER
    
    def create_issue_from_action(self, action: Dict) -> str:
        """Create a GitHub issue from an execution queue item."""
        repo_name = action['target_repo']
        repo = self.gh.get_repo(f"{self.owner}/{repo_name}")
        
        # Extract priority for label
        priority = action.get('priority', 'normal').lower()
        labels = ['codessa-generated']
        if priority == 'now':
            labels.append('priority: high')
        elif priority == 'next':
            labels.append('priority: medium')
        
        issue = repo.create_issue(
            title=action['title'],
            body=f"""
Automated issue from Codessa Reflection System

**Source:** {action.get('source', 'Unknown')}
**Priority:** {action.get('priority', 'Normal')}

{action.get('description', '')}

---
*Created by Ava Prime | [View in Notion]({action.get('notion_url', '#')})*
            """.strip(),
            labels=labels
        )
        
        return issue.html_url
    
    def create_pr_from_codestone(self, action: Dict, codestone: Dict) -> str:
        """Create a GitHub PR from a codestone artifact."""
        repo_name = action['target_repo']
        repo = self.gh.get_repo(f"{self.owner}/{repo_name}")
        
        # Create a new branch
        default_branch = repo.default_branch
        base_ref = repo.get_git_ref(f"heads/{default_branch}")
        branch_name = f"codessa/{codestone['title'].lower().replace(' ', '-')}"
        
        try:
            repo.create_git_ref(f"refs/heads/{branch_name}", base_ref.object.sha)
        except Exception:
            # Branch might already exist
            pass
        
        # Create or update file
        file_path = codestone.get('target_path', f"codessa_artifacts/{codestone['title']}.py")
        content = codestone['content']
        
        try:
            # Try to get existing file
            existing_file = repo.get_contents(file_path, ref=branch_name)
            repo.update_file(
                file_path,
                f"Update {codestone['title']} via Codessa",
                content,
                existing_file.sha,
                branch=branch_name
            )
        except Exception:
            # File doesn't exist, create it
            repo.create_file(
                file_path,
                f"Add {codestone['title']} via Codessa",
                content,
                branch=branch_name
            )
        
        # Create PR
        pr = repo.create_pull(
            title=f"[Codessa] {action['title']}",
            body=f"""
Automated PR from Codessa Reflection System

**Codestone:** {codestone['title']}
**ECL Score:** {codestone.get('ecl_score', 'N/A')}
**Language:** {codestone.get('language', 'Unknown')}

{action.get('description', '')}

## Changes
- {file_path}

## Context
{codestone.get('context', 'Artifact extracted from Intelligence Stream')}

---
*Created by Ava Prime | [View Codestone in Notion]({codestone.get('notion_url', '#')})*
            """.strip(),
            head=branch_name,
            base=default_branch
        )
        
        return pr.html_url
    
    def create_discussion_from_action(self, action: Dict) -> str:
        """Create a GitHub discussion from an execution queue item."""
        repo_name = action['target_repo']
        repo = self.gh.get_repo(f"{self.owner}/{repo_name}")
        
        # Note: GitHub Discussions API requires GraphQL
        # For now, we'll create an issue with a 'discussion' label
        issue = repo.create_issue(
            title=f"[Discussion] {action['title']}",
            body=f"""
Architectural Discussion from Codessa Reflection System

{action.get('description', '')}

## Questions to Address
- How does this fit with our current architecture?
- What are the trade-offs?
- What experiments should we run?

---
*Initiated by Ava Prime | [View in Notion]({action.get('notion_url', '#')})*
            """.strip(),
            labels=['codessa-generated', 'discussion', 'architecture']
        )
        
        return issue.html_url

# ==================== ORCHESTRATOR ====================

class AvaPrime:
    """Main orchestration engine."""
    
    def __init__(self):
        self.parser = ConversationParser()
        self.extractor = ArtifactExtractor()
        self.notion = NotionSync()
        self.github = GitHubSync()
    
    def run_sync_cycle(self):
        """Execute a full sync cycle."""
        print("🌟 Ava Prime awakening...")
        
        # 1. Scan exports folder
        exports = self._scan_exports()
        print(f"📂 Found {len(exports)} export files")
        
        # 2. Parse conversations
        conversations = []
        for export_file in exports:
            if export_file.suffix == '.json':
                convs = self.parser.parse_chatgpt_export(export_file)
            elif export_file.suffix in ['.md', '.markdown']:
                convs = self.parser.parse_claude_markdown(export_file)
            else:
                continue
            conversations.extend(convs)
        
        print(f"💬 Parsed {len(conversations)} conversations")
        
        # 3. Sync to Notion
        for conv in conversations:
            try:
                # Create Intelligence Stream
                stream_id = self.notion.create_intelligence_stream(conv)
                print(f"  ✓ Created stream: {conv['title'][:50]}...")
                
                # Extract and create Codestones
                artifacts = self.extractor.extract_artifacts(conv['messages'])
                for artifact in artifacts:
                    codestone_id = self.notion.create_codestone(artifact, stream_id)
                    print(f"    ✓ Created codestone: {artifact['title']}")
                
            except Exception as e:
                print(f"  ✗ Error processing {conv['title']}: {e}")
        
        print("✨ Sync cycle complete")
    
    def sync_execution_queue(self):
        """Check Execution_Queue and materialize actions in GitHub."""
        print("\n🚀 Checking execution queue...")
        
        # Query Notion for queued items
        try:
            results = self.notion.notion.databases.query(
                database_id=CodessaConfig.DB_EXECUTION,
                filter={
                    "property": "Status",
                    "select": {"equals": "⏳ Queued"}
                }
            )
            
            queued_items = results.get('results', [])
            print(f"📋 Found {len(queued_items)} queued actions")
            
            for page in queued_items:
                try:
                    # Parse execution item
                    action = self._parse_execution_item(page)
                    
                    # Create GitHub artifact based on action type
                    if action['type'] == 'Issue':
                        gh_url = self.github.create_issue_from_action(action)
                        print(f"  ✓ Created issue: {action['title'][:50]}...")
                    elif action['type'] == 'PR':
                        print(f"  ⚠ PR creation not yet implemented for: {action['title'][:50]}...")
                        continue
                    else:
                        print(f"  ⚠ Unknown action type: {action['type']}")
                        continue
                    
                    # Update Notion page with results
                    self.notion.notion.pages.update(
                        page_id=page['id'],
                        properties={
                            "GitHub_URL": {"url": gh_url},
                            "Status": {"select": {"name": "🚀 Pushed"}},
                            "Completed_Date": {"date": {"start": datetime.now().isoformat()[:10]}}
                        }
                    )
                    print(f"    ✓ Updated Notion with GitHub URL")
                    
                except Exception as e:
                    print(f"  ✗ Error processing action: {e}")
            
            print("✨ Execution queue synced")
            
        except Exception as e:
            print(f"✗ Error querying execution queue: {e}")
    
    def _parse_execution_item(self, page: Dict) -> Dict:
        """Parse a Notion execution queue page into action dict."""
        props = page['properties']
        
        # Extract title
        title_prop = props.get('Title', {}).get('title', [])
        title = title_prop[0]['text']['content'] if title_prop else 'Untitled Action'
        
        # Extract action type
        action_type_prop = props.get('Action_Type', {}).get('select')
        action_type = action_type_prop['name'] if action_type_prop else 'Issue'
        
        # Extract target repo
        target_repo_prop = props.get('Target_Repo', {}).get('select')
        target_repo = target_repo_prop['name'] if target_repo_prop else 'codessa-os'
        
        # Get page content as description
        description = self._get_page_content(page['id'])
        
        # Build Notion URL
        notion_url = f"https://notion.so/{page['id'].replace('-', '')}"
        
        return {
            'title': title,
            'type': action_type,
            'target_repo': target_repo,
            'description': description,
            'notion_url': notion_url,
            'page_id': page['id']
        }
    
    def _get_page_content(self, page_id: str) -> str:
        """Retrieve text content from a Notion page."""
        try:
            blocks = self.notion.notion.blocks.children.list(block_id=page_id)
            content_parts = []
            
            for block in blocks.get('results', [])[:10]:  # First 10 blocks
                block_type = block['type']
                if block_type == 'paragraph':
                    text_parts = block['paragraph'].get('rich_text', [])
                    text = ''.join([t['text']['content'] for t in text_parts])
                    if text.strip():
                        content_parts.append(text)
                elif block_type in ['heading_1', 'heading_2', 'heading_3']:
                    text_parts = block[block_type].get('rich_text', [])
                    text = ''.join([t['text']['content'] for t in text_parts])
                    if text.strip():
                        content_parts.append(f"## {text}")
            
            return '\n\n'.join(content_parts) if content_parts else "No description provided."
            
        except Exception as e:
            return f"Error retrieving content: {e}"
    
    def _scan_exports(self) -> List[Path]:
        """Scan exports folder for new conversation files."""
        exports_path = CodessaConfig.EXPORTS_PATH
        if not exports_path.exists():
            exports_path.mkdir(parents=True)
            return []
        
        # Scan for JSON and Markdown files
        files = []
        files.extend(exports_path.glob("*.json"))
        files.extend(exports_path.glob("*.md"))
        files.extend(exports_path.glob("*.markdown"))
        
        # Sort by modification time (newest first)
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        return files

# ==================== MAIN ====================

def main():
    """Run Ava Prime sync daemon."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Codessa Sync Daemon - Ava Prime's autonomic nervous system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python codessa_sync_daemon.py                    # Full sync cycle
  python codessa_sync_daemon.py --capture-only      # Just parse & upload conversations
  python codessa_sync_daemon.py --execute-only      # Just sync execution queue to GitHub
  python codessa_sync_daemon.py --continuous        # Run continuously with 1h interval
        """
    )
    
    parser.add_argument('--capture-only', action='store_true',
                       help='Only capture and upload conversations (skip execution queue)')
    parser.add_argument('--execute-only', action='store_true',
                       help='Only sync execution queue to GitHub (skip captures)')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuously with 1 hour intervals')
    parser.add_argument('--interval', type=int, default=3600,
                       help='Interval in seconds for continuous mode (default: 3600)')
    
    args = parser.parse_args()
    
    ava = AvaPrime()
    
    def run_cycle():
        """Execute appropriate sync operations based on args."""
        if args.execute_only:
            ava.sync_execution_queue()
        elif args.capture_only:
            ava.run_sync_cycle()
        else:
            # Full cycle: capture + execute
            ava.run_sync_cycle()
            ava.sync_execution_queue()
    
    # Run once or continuously
    if args.continuous:
        import time
        print(f"🔄 Running in continuous mode (interval: {args.interval}s)")
        print("   Press Ctrl+C to stop\n")
        
        while True:
            try:
                run_cycle()
                print(f"\n💤 Sleeping for {args.interval}s...")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n\n✨ Ava Prime resting. Until next time.")
                break
    else:
        run_cycle()

if __name__ == "__main__":
    main()
