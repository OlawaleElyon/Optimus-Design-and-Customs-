# DNS Fix Guide for optimuscustomz.com

## Current Problem:
Your domain has **5 A Records** pointing to different IPs, causing conflicts. This is why the website shows "This site can't be reached".

## What You Have Now (in Wix):

❌ **DELETE THESE 3 OLD RECORDS:**
1. optimuscustomz.com → 185.230.63.171
2. optimuscustomz.com → 185.230.63.186  
3. optimuscustomz.com → 185.230.63.107

✅ **KEEP THESE 2 EMERGENT RECORDS:**
1. optimuscustomz.com → 162.159.142.117
2. optimuscustomz.com → 172.66.2.113

## Step-by-Step Fix:

### In Wix DNS Manager:

1. **Click the three dots (•••) next to each of these records:**
   - 185.230.63.171 → Click ••• → Delete
   - 185.230.63.186 → Click ••• → Delete
   - 185.230.63.107 → Click ••• → Delete

2. **Leave these two records:**
   - 162.159.142.117 ✅
   - 172.66.2.113 ✅

3. **Click Save**

4. **Wait 5-15 minutes** for DNS to propagate

5. **Clear your browser cache:**
   - Chrome: Ctrl+Shift+Delete
   - Or use Incognito/Private window

6. **Visit optimuscustomz.com** - It should now show your Emergent deployment!

## After DNS Propagates:

Your site will show the same content as:
- https://luxury-auto-book.emergent.host ✅

## CNAME Records:

You also have CNAME records pointing to Vercel/Wix. You can leave those for now, but eventually you should delete:
- en.optimuscustomz.com → cdn1.wixdns.net
- www.optimuscustomz.com → a5eee45d072ddb60.vercel... 

The www CNAME might conflict with your A records. If the site still doesn't work after removing the 185.x.x.x records, also delete the www CNAME.

## Verification:

Check DNS propagation at: https://dnschecker.org
- Enter: optimuscustomz.com
- Should show: 162.159.142.117 and 172.66.2.113
- Wait until most locations show green checkmarks

## If Still Not Working:

1. Delete the www CNAME record (www.optimuscustomz.com → vercel)
2. Wait another 10 minutes
3. Try accessing both:
   - http://optimuscustomz.com
   - https://optimuscustomz.com
