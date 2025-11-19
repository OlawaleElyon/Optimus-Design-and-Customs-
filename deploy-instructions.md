# Deployment Instructions for Optimus Design & Customs

## Option 1: Vercel with Correct Settings

### Required Settings:
- **Root Directory:** `app/frontend`
- **Build Command:** `yarn build`
- **Output Directory:** `build`
- **Install Command:** `yarn install`
- **Environment Variable:** `REACT_APP_BACKEND_URL`

### Vercel Configuration File Created:
- `/app/frontend/vercel.json` - Contains build configuration
- `/app/frontend/.nvmrc` - Specifies Node.js 18

## Option 2: Netlify (Recommended if Vercel fails)

### Netlify Settings:
- **Base directory:** `app/frontend`
- **Build command:** `yarn build`
- **Publish directory:** `app/frontend/build`
- **Environment Variable:** `REACT_APP_BACKEND_URL`

## Build Verification:
✅ Local build tested successfully
✅ Build output: 147.39 kB (main.js), 11.39 kB (main.css)
✅ All dependencies resolved
✅ No build errors

## Troubleshooting:
1. Ensure Node.js 18.x is being used
2. Verify all environment variables are set
3. Check that yarn.lock is committed to Git
4. Confirm Root Directory is set to `app/frontend`

## Next Steps:
1. Push all changes to GitHub
2. Try Vercel with updated settings
3. If Vercel fails, switch to Netlify
4. Verify deployment and test all features
