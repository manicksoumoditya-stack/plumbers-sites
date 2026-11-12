#!/data/data/com.termux/files/usr/bin/bash
# একবারই চালাবি: bash setup.sh
cd "$(dirname "$0")"
source ./config.txt
if [ "$TOKEN" = "YOUR_TOKEN_HERE" ] || [ "$EMAIL" = "YOUR_EMAIL_HERE" ]; then
  echo "❌ আগে config.txt-তে EMAIL আর TOKEN বসা (nano config.txt)"; exit 1
fi
pkg install -y python git >/dev/null 2>&1
git config --global user.name "$GITHUB_USER"
git config --global user.email "$EMAIL"
[ -d .git ] || git init -b main
git remote remove origin 2>/dev/null
git remote add origin "https://$TOKEN@github.com/$GITHUB_USER/$REPO.git"
echo "✅ সেটআপ শেষ। এবার: bash publish.sh"
