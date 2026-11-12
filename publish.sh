#!/data/data/com.termux/files/usr/bin/bash
# সাইট বানিয়ে GitHub-এ পুশ: bash publish.sh
cd "$(dirname "$0")"
source ./config.txt
python generate.py || exit 1
git add -A
git commit -m "update sites" >/dev/null 2>&1
git push -u origin main && echo "✅ পুশ হয়েছে। লাইভ লিংক: https://$GITHUB_USER.github.io/$REPO/"
