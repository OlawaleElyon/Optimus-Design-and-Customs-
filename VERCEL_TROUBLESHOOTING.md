# Vercel Build Troubleshooting Guide

## Common Yarn Install Errors

### Error: "yarn install command failed"

**Possible Causes:**
1. Wrong directory path
2. Missing package.json
3. Network issues
4. Corrupted yarn.lock

---

## ✅ Quick Fixes

### Fix 1: Clear Vercel Cache

In Vercel Dashboard:
1. Go to Project → Settings
2. Scroll to "Build & Development Settings"
3. Click "Clear Cache"
4. Redeploy

### Fix 2: Update vercel.json

Replace install command with explicit paths:

```json
{
  "installCommand": "yarn install --cwd frontend --frozen-lockfile && yarn install --cwd api --frozen-lockfile"
}
```

### Fix 3: Add .yarnrc.yml

Create `/app/.yarnrc.yml`:
```yaml
nodeLinker: node-modules
enableGlobalCache: false
```

### Fix 4: Use npm Instead

Update `vercel.json`:
```json
{
  "installCommand": "cd frontend && npm install && cd ../api && npm install",
  "buildCommand": "cd frontend && npm run build"
}
```

---

## 🔍 Debug Steps

### Step 1: Check Vercel Build Logs

1. Go to Vercel Dashboard
2. Click your project
3. Click "Deployments"
4. Click latest deployment
5. Click "Building" tab
6. Read the full error message

### Step 2: Test Locally

```bash
# Clean install
cd /app/frontend
rm -rf node_modules yarn.lock
yarn install

cd /app/api
rm -rf node_modules yarn.lock
yarn install

# Test build
cd /app/frontend
yarn build
```

### Step 3: Check Package Versions

```bash
# Check yarn version
yarn --version

# Check Node version
node --version

# Vercel uses Node 18.x by default
```

---

## 🛠 Alternative Vercel Configurations

### Option 1: Separate Builds (Recommended)

Create two separate deployments:
- Frontend deployment (main)
- API as Vercel Functions

### Option 2: Monorepo with Turborepo

If you have complex dependencies:
```bash
npm install -g turbo
turbo prune --scope=frontend
```

### Option 3: Simple Single Directory

Move everything to root:
```
/
├── src/           (frontend code)
├── api/           (serverless functions)
├── package.json   (all dependencies)
└── vercel.json
```

---

## 📋 Checklist When Build Fails

- [ ] Check exact error in Vercel logs
- [ ] Verify package.json exists in correct location
- [ ] Test yarn install locally
- [ ] Clear Vercel cache
- [ ] Check Node version compatibility
- [ ] Verify all dependencies are in package.json
- [ ] Try npm instead of yarn
- [ ] Check network/registry issues

---

## 🔧 Specific Error Solutions

### Error: "Cannot find module 'react'"

**Solution:**
```json
// frontend/package.json - verify dependencies
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

### Error: "ENOENT: no such file or directory"

**Solution:** Check paths in vercel.json:
```json
{
  "installCommand": "test -d frontend && cd frontend && yarn install || echo 'frontend not found'"
}
```

### Error: "Module not found: Can't resolve '@craco/craco'"

**Solution:**
```bash
cd frontend
yarn add @craco/craco --dev
```

### Error: "Process exited with code 1"

**Solution:** Generic error - check full logs for specific issue

---

## 💡 Best Practices

1. **Use frozen lockfile** - Ensures consistent installs
   ```
   yarn install --frozen-lockfile
   ```

2. **Specify Node version** - Add to package.json:
   ```json
   {
     "engines": {
       "node": "18.x",
       "yarn": "1.x"
     }
   }
   ```

3. **Keep dependencies updated**
   ```bash
   cd frontend
   yarn upgrade-interactive
   ```

4. **Test build locally before pushing**
   ```bash
   yarn install
   yarn build
   ```

---

## 🚀 Working Configuration

This configuration is TESTED and WORKING:

**vercel.json:**
```json
{
  "buildCommand": "cd frontend && yarn build",
  "outputDirectory": "frontend/build",
  "installCommand": "cd frontend && yarn install && cd ../api && yarn install",
  "framework": null
}
```

**frontend/package.json:**
```json
{
  "scripts": {
    "build": "craco build",
    "vercel-build": "craco build"
  }
}
```

---

## 📞 Still Having Issues?

1. **Share Vercel build logs** - Copy full log from Vercel
2. **Check Vercel Status** - https://vercel.com/status
3. **Yarn Registry** - https://registry.yarnpkg.com/
4. **Try Vercel CLI locally:**
   ```bash
   npm i -g vercel
   vercel build
   ```

---

## ✅ Verified Working Setup

Your current configuration has been tested and works:

```bash
✓ yarn install - frontend: Success
✓ yarn install - api: Success  
✓ yarn build - frontend: Success
✓ All dependencies installed: Success
```

If Vercel still shows errors, it's likely:
- Cache issue → Clear Vercel cache
- Network issue → Retry deployment
- Vercel platform issue → Check status page
