import csv, re, html, shutil, datetime
from pathlib import Path

ROOT = Path(__file__).parent
CSV_FILE = ROOT / "data" / "plumbers.csv"
IMG = ROOT / "images"
OUT = ROOT / "docs"
TPL = (ROOT / "templates" / "site.html").read_text(encoding="utf-8")
EXTS = ["jpg", "jpeg", "png", "webp"]
DEFAULT_SERVICES = ["Leak Repair", "Drain Cleaning", "Water Heater Services",
                    "Pipe Repair & Replacement", "Bathroom Plumbing"]
ICONS = [("leak", "💧"), ("drain", "🚿"), ("heater", "🔥"), ("pipe", "🔧"),
         ("bath", "🛁"), ("kitchen", "🍽️"), ("sewer", "🕳️"),
         ("emergency", "🚨"), ("commercial", "🏢")]
DESCS = {"leak": "Quick and effective leak detection and repair.",
         "drain": "Keep your drains clear and flowing smoothly.",
         "heater": "Installation, repair and maintenance.",
         "pipe": "Reliable solutions for all pipe issues.",
         "bath": "Expert plumbing for renovations and new installs."}

def esc(s): return html.escape((s or "").strip())
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "plumber"

def icon(s):
    for k, v in ICONS:
        if k in s.lower(): return v
    return "🔧"

def desc(s):
    for k, v in DESCS.items():
        if k in s.lower(): return v
    return "Professional service you can count on."

def find_img(slug, base):
    for e in EXTS:
        p = IMG / slug / f"{base}.{e}"
        if p.exists():
            (OUT / slug).mkdir(parents=True, exist_ok=True)
            shutil.copy(p, OUT / slug / p.name)
            return p.name
    return None

def build(row):
    g = lambda k: (row.get(k) or "").strip()
    name = g("name")
    slug = slugify(name)
    (OUT / slug).mkdir(parents=True, exist_ok=True)
    phone = g("phone")
    tel = re.sub(r"[^\d+]", "", phone)
    emergency = g("emergency").lower() in ("yes", "y", "true", "1")
    services = [s.strip() for s in g("services").split(",") if s.strip()] or DEFAULT_SERVICES

    wa = re.sub(r"[^0-9]", "", g("whatsapp"))
    if wa:
        quote = "https://wa.me/" + wa
    elif g("email"):
        quote = "mailto:" + g("email") + "?subject=Free%20Quote%20Request"
    else:
        quote = "tel:" + tel

    hero = find_img(slug, "hero")
    hero_style = ("background-image:linear-gradient(90deg,rgba(8,24,48,.92),rgba(8,24,48,.35)),url('%s')" % hero
                  if hero else "")
    about = find_img(slug, "about")
    about_style = "background-image:url('%s')" % about if about else ""

    badges = ["<li><b>Licensed &amp; Insured</b></li>"]
    if emergency: badges.append("<li><b>24/7</b>Emergency Service</li>")
    badges.append("<li><b>Experienced</b>Professionals</li>")
    if g("rating"):
        badges.append("<li><b>★ %s</b>%s reviews</li>" % (esc(g("rating")), esc(g("reviews"))))
    else:
        badges.append("<li><b>100%</b>Satisfaction Guarantee</li>")

    cards = []
    for i, s in enumerate(services, 1):
        pic = find_img(slug, "service%d" % i)
        if pic:
            top = '<div class="pic" style="background-image:url(\'%s\')"></div>' % pic
        else:
            top = '<div class="pic">%s</div>' % icon(s)
        cards.append('<div class="card">%s<div class="body"><h3>%s</h3><p>%s</p></div></div>'
                     % (top, esc(s), desc(s)))

    stats = []
    for key, label in [("years", "Years of Experience"), ("customers", "Happy Customers"),
                       ("projects", "Plumbing Projects")]:
        if g(key): stats.append("<div><b>%s+</b><span>%s</span></div>" % (esc(g(key)), label))
    stats.append("<div><b>100%</b><span>Satisfaction Guarantee</span></div>")
    stats_block = '<section class="stats"><div class="wrap statgrid">%s</div></section>' % "".join(stats)

    rep = {
        "name": esc(name), "name_upper": esc(name.upper()), "phone": esc(phone), "tel": tel,
        "city": esc(g("city")), "address": esc(g("address")),
        "service_area": esc(g("service_area") or g("city")),
        "hours": esc(g("hours") or "Mon - Sat: 8AM - 6PM"),
        "tagline": esc(g("tagline") or "Trusted, high-quality plumbing for homes and businesses. We keep your water flowing and your life hassle-free."),
        "emerg_short": "24/7 Emergency Service" if emergency else "Call for a free quote",
        "quote_link": quote, "hero_style": hero_style, "about_style": about_style,
        "badges": "".join(badges), "service_cards": "".join(cards), "stats_block": stats_block,
        "footer_services": "".join("<li>%s</li>" % esc(s) for s in services),
        "email_li": "<li>✉️ %s</li>" % esc(g("email")) if g("email") else "",
        "year": str(datetime.date.today().year),
    }
    page = TPL
    for k, v in rep.items():
        page = page.replace("{{" + k + "}}", v)
    (OUT / slug / "index.html").write_text(page, encoding="utf-8")
    return slug, name, g("city")

def main():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    (OUT / ".nojekyll").touch()
    done = []
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if (row.get("name") or "").strip():
                done.append(build(row))
    items = "".join('<div class="card"><div class="body"><h3><a href="%s/">%s</a></h3><p>%s</p></div></div>'
                    % (s, esc(n), esc(c)) for s, n, c in done)
    (OUT / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Plumbers Directory</title><link rel="stylesheet" href="assets/style.css">'
        '<div class="wrap"><h2 style="padding-top:30px">Plumbers</h2><div class="dir">%s</div></div>' % items,
        encoding="utf-8")
    print("Done: %d sites built in docs/" % len(done))

main()
