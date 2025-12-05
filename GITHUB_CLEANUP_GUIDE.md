# GitHub Repository Cleanup Guide

## Complete Cleanup Steps

### Step 1: Remove Sensitive/Unused Files from History

```bash
# Navigate to your project
cd /path/to/your/project

# Install git-filter-repo (if not installed)
# macOS: brew install git-filter-repo
# Linux: pip install git-filter-repo

# Remove old env files from history
git filter-repo --path .env.old --invert-paths --force
git filter-repo --path backend/.env.old --invert-paths --force
git filter-repo --path frontend/.env.old --invert-paths --force

# Remove backup files
git filter-repo --path-glob '*backup*' --invert-paths --force
git filter-repo --path-glob '*old*' --invert-paths --force

# Remove MongoDB-related files
git filter-repo --path-glob '*mongo*' --invert-paths --force
git filter-repo --path-glob '*mongoose*' --invert-paths --force

# Remove Mailtrap files
git filter-repo --path-glob '*mailtrap*' --invert-paths --force

# Remove Railway configs
git filter-repo --path-glob '*railway*' --invert-paths --force
```

### Step 2: Update .gitignore

Create or update `.gitignore`:

```gitignore
# Environment variables
.env
.env.local
.env.*.local
*.env
.env.old
.env.backup

# Dependencies
node_modules/
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
build/
dist/
*.pyc
coverage/
.coverage
htmlcov/
.pytest_cache/

# OS
Thumbs.db
Desktop.ini

# Backup files
*.backup
*.old
*_backup.*
*_old.*

# Database
*.db
*.sqlite
*.sqlite3

# Misc
.cache/
temp/
tmp/
```

### Step 3: Clean Current Working Directory

```bash
# Remove any remaining backup/old files
find . -name "*backup*" -type f -delete
find . -name "*old*" -type f -delete
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Remove node_modules to save space (will be reinstalled)
rm -rf frontend/node_modules
rm -rf backend/node_modules

# Remove build artifacts
rm -rf frontend/build
rm -rf backend/dist
```

### Step 4: Stage Clean Files

```bash
# Add all clean files
git add .

# Commit the cleanup
git commit -m "refactor: complete codebase cleanup - removed MongoDB, Mailtrap, Railway; kept only Supabase + Resend"
```

### Step 5: Force Push (WARNING: This rewrites history)

```bash
# IMPORTANT: Inform team members before doing this
# They will need to re-clone the repository

# Force push to remote
git push origin main --force

# Or if using a different branch
git push origin <your-branch> --force
```

### Step 6: Verify Cleanup

```bash
# Check repo size
du -sh .git

# Verify no sensitive files remain
git log --all --full-history --source --pretty=format: --name-only -- .env | sort -u
git log --all --full-history --source --pretty=format: --name-only -- "*backup*" | sort -u

# Check for MongoDB references
git grep -i "mongodb\|mongoose\|mongo_url" -- "*.py" "*.js" "*.jsx" "*.json"

# Should return nothing or only expected references in documentation
```

---

## Alternative: Clean Branch Strategy

If you don't want to rewrite history:

### Option A: Create Fresh Branch

```bash
# Create a new orphan branch (no history)
git checkout --orphan clean-main

# Add all current clean files
git add .

# Make first commit
git commit -m "feat: production-ready booking system with Supabase + Resend"

# Delete old main branch
git branch -D main

# Rename clean branch to main
git branch -m main

# Force push
git push origin main --force
```

### Option B: New Repository

1. Create new GitHub repository
2. Copy only necessary files
3. Initialize new git repo
4. Push to new remote
5. Archive old repository

```bash
# In your clean project directory
git init
git add .
git commit -m "feat: production-ready booking system"
git remote add origin <new-repo-url>
git push -u origin main
```

---

## Files That Should Be in Clean Repo

### Backend
```
/app/backend/
├── server.py
├── appointment_api.py
├── requirements.txt
└── .env (gitignored, but documented in README)
```

### Frontend
```
/app/frontend/
├── src/
│   ├── components/
│   │   └── Booking.jsx
│   ├── pages/
│   ├── App.js
│   └── index.js
├── public/
│   └── index.html
├── package.json
└── .env (gitignored, but documented in README)
```

### Root
```
/app/
├── README.md
├── .gitignore
├── DEPLOYMENT_GUIDE.md
└── SUPABASE_EMAIL_FALLBACK_SETUP.md
```

---

## Post-Cleanup Verification Checklist

- [ ] No `.env` files in history
- [ ] No backup/old files in history
- [ ] No MongoDB/Mailtrap/Railway references in code
- [ ] .gitignore properly excludes sensitive files
- [ ] README.md is up to date
- [ ] Repository size is reasonable
- [ ] All team members notified about force push
- [ ] GitHub Actions/CI still works
- [ ] Deployment still works

---

## Maintenance

### Regular Cleanup Commands

```bash
# Check for large files
git rev-list --all | xargs git ls-tree -r --long | sort -uk3 | sort -rnk4 | head -10

# Check repo size
git count-objects -vH

# Garbage collection
git gc --aggressive --prune=now
```

### Prevent Future Issues

1. **Always use .gitignore before first commit**
2. **Never commit .env files**
3. **Use git-secrets or pre-commit hooks**
4. **Regular repository audits**
5. **Document environment variables in README, not in code**

---

## Emergency: Leaked Secrets

If you accidentally pushed secrets:

1. **Immediately rotate/revoke the secret** (API keys, passwords)
2. **Clean git history as shown above**
3. **Force push**
4. **Audit access logs** (GitHub, AWS, etc.)
5. **Enable 2FA and security scanning**

```bash
# GitHub secret scanning
# Go to: Repository → Settings → Security → Secret scanning
```

---

## Final Commit Message Template

```
refactor: complete codebase cleanup and production hardening

BREAKING CHANGES:
- Removed MongoDB, Mailtrap, Railway dependencies
- Now using only Supabase (database) + Resend (email)
- Cleaned repository history of sensitive files
- Updated all documentation

Features:
- ✅ Production-grade booking API
- ✅ Guaranteed data persistence via Supabase
- ✅ Email fallback system
- ✅ Comprehensive error handling
- ✅ Professional logging
- ✅ Clean, maintainable codebase

Chore:
- Removed all backup/old files
- Updated .gitignore
- Cleaned git history
- Optimized repository size

Docs:
- Updated README with current tech stack
- Added deployment guides
- Added Supabase email fallback setup guide
```
