প্লাম্বার ওয়েবসাইট জেনারেটর
================================

ফোল্ডারে কোন ফাইল কী কাজ করে
-----------------------------
config.txt         -> তোর GitHub ইউজারনেম, ইমেইল, টোকেন (এখানে বসাতে হবে)
data/plumbers.csv  -> প্লাম্বারদের লিস্ট (এখানে সারি যোগ করবি)
images/<slug>/     -> নিজের ছবি (ঐচ্ছিক): hero.jpg, about.jpg, service1.jpg ...
templates/site.html-> সাইটের ডিজাইন (HTML)
assets/style.css   -> রঙ, ফন্ট, লেআউট
generate.py        -> CSV পড়ে সাইট বানায় (docs/ ফোল্ডারে)
setup.sh           -> একবারই চালাবি
publish.sh         -> সাইট বানিয়ে GitHub-এ পুশ করে
docs/              -> তৈরি হওয়া সাইট (এটা হাত দিবি না, নিজে নিজে বানায়)

ধাপে ধাপে
---------
1. nano config.txt  -> EMAIL আর TOKEN বসা, Ctrl+X, Y, Enter
2. bash setup.sh    (একবারই)
3. bash publish.sh
4. GitHub রেপো -> Settings -> Pages -> Branch: main, Folder: /docs -> Save

নতুন প্লাম্বার যোগ করতে
-----------------------
data/plumbers.csv-তে নতুন সারি লিখে bash publish.sh চালা।

নিজের ছবি দিতে
--------------
images/pipepro-plumbing/hero.jpg (ব্যবসার নাম ছোট হাতের অক্ষরে, ড্যাশ দিয়ে)
ছবি না থাকলে নীল গ্র্যাডিয়েন্ট আর আইকন বসে।
