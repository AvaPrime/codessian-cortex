# Ava Prime Dashboard v2.0 - Cheat Sheet 📋

> **Quick reference for common operations and commands**

---

## 🚀 Quick Start Commands

```bash
# Setup
./setup.sh                    # Automated setup
python verify_setup.py        # Verify installation
python ava_prime_integration.py  # Run demo

# Daily Operations
python codessa_sync_daemon.py   # Sync Notion ↔ GitHub
python health_check.py          # System health
python generate_briefing.py     # Morning briefing

# Testing
pytest -v                      # Run all tests
pytest --cov                   # With coverage
pytest -m "not slow"           # Skip slow tests

# Deployment
python deploy_v2.py --environment staging --enable-features all
```

---

## 🔑 Environment Variables Quick Reference

```bash
# Essential
NOTION_API_KEY=secret_xxx
GITHUB_TOKEN=ghp_xxx
ANTHROPIC_API_KEY=sk-ant_xxx

# Configuration
ENVIRONMENT=development|staging|production
DEBUG=true|false
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# Feature Flags
ENABLE_RBAC=true
ENABLE_AUDIT_LOGGING=true
ENABLE_RATE_LIMITING=true
```

---

## 👤 User Roles & Permissions

| Role | Execute Commands | AI Prompts | Modify Data | View Only |
|------|------------------|------------|-------------|-----------|
| **Admin** | ✅ | ✅ | ✅ | ✅ |
| **Developer** | ❌ | ✅ | ✅ | ✅ |
| **Viewer** | ❌ | ❌ | ❌ | ✅ |

---

## 🔒 Security Quick Checks

```python
# Check user permissions
from ava_prime_integration import get_user
user = get_user("user@example.com")
print(user.has_permission(Permission.EXECUTE_COMMANDS))

# Validate command before execution
from ava_prime_integration import CommandSandbox
sandbox = CommandSandbox(config)
sandbox.validate_command("python3", ["script.py"])

# Sanitize AI prompt
from ava_prime_integration import PromptSanitizer
safe_prompt = PromptSanitizer.build_safe_prompt(template, variables)

# Validate AI response
from ava_prime_integration import ResponseValidator
validated = ResponseValidator.validate_code_review(response)
```

---

## 📝 Audit Log Queries

```bash
# View recent events
tail -n 100 logs/audit.log

# Search for failed operations
grep '"success": false' logs/audit.log

# Find permission denials
grep "permission_denied" logs/audit.log

# User activity
grep '"user_email": "admin@example.com"' logs/audit.log

# Critical failures
grep '"action_type": "external_command_execution"' logs/audit.log | grep 'false'
```

---

## 🤖 AI Prompt Templates

### Code Review
```python
template = """Review this code:
---CODE_START---
{code_content}
---CODE_END---

Provide JSON:
{
  "ecl_score": 0.0-1.0,
  "recommended_status": "string",
  "strengths": ["string"],
  "weaknesses": ["string"]
}
"""
```

### Morning Briefing
```python
template = """Generate briefing for {date}

Data: {intelligence_streams}

Format:
## Executive Summary
## Key Themes
## Recommended Actions
"""
```

---

## ⚡ Workflow Engine

```python
# Execute with retry
from ava_prime_integration import WorkflowEngine

engine = WorkflowEngine(max_retries=3, retry_delay=60)

result = engine.execute_with_retry(
    your_function,
    "Workflow Name",
    **kwargs
)

if result["status"] == "success":
    print(f"Completed in {result['duration_ms']}ms")
else:
    print(f"Failed: {result['error']}")
```

---

## 💾 Caching Patterns

```python
# Use cache decorator
from ava_prime_integration import cache

@cache.cached(ttl_seconds=300)  # 5 minutes
def expensive_operation(param):
    return compute_result(param)

# Manual caching
cache.set("key", value, ttl_seconds=3600)
result = cache.get("key")

# Invalidate cache
cache.invalidate("key")
cache.clear()  # Clear all
```

---

## 🎯 Rate Limiting

```python
# Check rate limit
from ava_prime_integration import rate_limiter

if rate_limiter.check_rate_limit(user_id, "ai_prompts"):
    # Execute operation
    pass
else:
    raise RateLimitExceeded("Too many requests")

# Get remaining quota
remaining = rate_limiter.get_remaining(user_id, "ai_prompts")
```

---

## 📊 Monitoring Commands

```bash
# System health
python -c "from ava_prime_integration import HealthMonitor; 
monitor = HealthMonitor(); print(monitor.run_all_checks())"

# Check API connectivity
curl -H "Authorization: Bearer $NOTION_API_KEY" \
  https://api.notion.com/v1/users/me

# Database status
python -c "from ava_prime_integration import check_database; check_database()"

# Cache statistics
python -c "from ava_prime_integration import cache; 
print(f'Size: {cache.get_size_mb()}MB, Hits: {cache.hit_count}')"
```

---

## 🔧 Common Fixes

### Reset Rate Limits
```python
from ava_prime_integration import rate_limiter
rate_limiter.reset_user("user_id")
```

### Clear All Caches
```bash
rm -rf cache/*
python -c "from ava_prime_integration import cache; cache.clear()"
```

### Regenerate Audit Report
```bash
python -c "from ava_prime_integration import AuditLogger;
logger = AuditLogger(); logger.generate_report('2025-11-01', '2025-11-11')"
```

### Force Workflow Retry
```python
from ava_prime_integration import retry_failed_workflows
retry_failed_workflows(max_age_hours=24)
```

---

## 🐛 Debug Snippets

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Trace API Calls
```python
import http.client
http.client.HTTPConnection.debuglevel = 1
```

### Profile Performance
```python
import cProfile
cProfile.run('your_function()')
```

### Memory Usage
```python
import tracemalloc
tracemalloc.start()
# ... your code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

---

## 📈 Performance Tuning

```bash
# Increase cache size
CACHE_MAX_SIZE_MB=500

# Adjust batch size
BATCH_SIZE=100

# Tune rate limits
RATE_LIMIT_AI_PROMPTS_PER_HOUR=20
RATE_LIMIT_COMMANDS_PER_HOUR=10

# Worker pool size
MAX_WORKERS=10
```

---

## 🚨 Emergency Commands

### Stop All Services
```bash
pkill -f codessa_sync_daemon
pkill -f ava_prime
```

### Emergency Rollback
```bash
BACKUP_DIR="backups/production/$(ls -t backups/production | head -1)"
cp $BACKUP_DIR/*.json .
cp $BACKUP_DIR/.env .
```

### Revoke Compromised Keys
```bash
# 1. Revoke in provider dashboard (Notion/GitHub)
# 2. Generate new keys
# 3. Update .env
nano .env
# 4. Restart services
./restart.sh
```

### View Critical Errors
```bash
tail -f logs/audit.log | grep '"success": false'
```

---

## 📚 Documentation Links

- [Full README](README_V2.md)
- [Implementation Guide](implementation_guide.md)
- [API Documentation](https://docs.codessa.ai/api)
- [Security Guide](https://docs.codessa.ai/security)

---

## 🆘 Support Contacts

- **Emergency**: security@codessa.ai
- **Support**: support@codessa.ai
- **GitHub Issues**: https://github.com/codessian/codessian-cortex/issues

---

## 💡 Pro Tips

1. **Always test in development first**
   ```bash
   ENVIRONMENT=development python your_script.py
   ```

2. **Use feature flags for gradual rollout**
   ```bash
   ENABLE_NEW_FEATURE=true  # Test first
   ```

3. **Monitor audit logs regularly**
   ```bash
   watch -n 60 'tail -20 logs/audit.log'
   ```

4. **Keep backups recent**
   ```bash
   # Add to crontab
   0 */6 * * * cd /path/to/ava-prime && ./backup.sh
   ```

5. **Update dependencies monthly**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

---

**Quick Help**: Run `python -c "from ava_prime_integration import show_help; show_help()"`

**Last Updated**: 2025-11-11