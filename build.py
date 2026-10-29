#!/usr/bin/env python3
"""Build a dependency-free, bilingual static portfolio from content.json."""
import argparse
import html
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
parser = argparse.ArgumentParser()
parser.add_argument("--publish", action="store_true", help="Require complete, confirmed public content")
args = parser.parse_args()
data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
profile = data["profile"]

def esc(value):
    return html.escape(str(value), quote=True)

def tr(value, lang):
    return value.get(lang, value.get("en", "")) if isinstance(value, dict) else value

def safe_url(value):
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme and parsed.scheme not in ("http", "https", "mailto"):
        raise ValueError("Unsupported link protocol")
    if value.startswith("//"):
        raise ValueError("Use an explicit https URL")
    return esc(value)

def link(url, label, extra=""):
    external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
    return f'<a href="{safe_url(url)}"{external}{extra}>{esc(label)}</a>'

if args.publish:
    checks = [
        (data.get("publish_ready") is True, "Set publish_ready only after identity and content are confirmed."),
        (data.get("site_url", "").startswith("https://"), "Set the final site_url."),
        (profile["name"]["en"] not in ("", "Your Name"), "Add the confirmed public name."),
        (bool(profile.get("email") or profile.get("github")), "Add a public contact method."),
        (not any(p.get("draft") for p in data["projects"]), "Replace or remove sample project entries."),
    ]
    for valid, message in checks:
        if not valid:
            raise SystemExit("Publication blocked: " + message)

OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)

labels = {
    "en": {
        "lang": "en", "switch": "中文", "switch_file": "zh.html", "edition": "PERSONAL WEBSITE",
        "skip": "Skip to content", "photo": "Portrait to be added", "caption": "Your portrait will appear here.",
        "draft": "Layout preview · Personal information, project details, and photo are waiting to be added.",
        "tabs": ["Highlights", "Resources", "Experience"], "selected": "Selected publications", "selected_note": "Robotics · Reward modeling · 3D perception",
        "contribution": "My contribution", "result": "Evidence & result", "visual": "PROJECT VISUAL", "sample": "CONTENT PLACEHOLDER",
        "software_title": "Code & project resources", "software_empty": "A home for useful, reusable work.",
        "software_desc": "Selected repositories will appear here, with the problem each solves and my role in the work.",
        "about_title": "Professional experience", "about_empty": "A little more about me.", "education_title": "Education",
        "about_desc": "Education, professional experience, and current interests will be added once the details are confirmed.",
        "contact": "Let’s connect.", "contact_desc": "For conversations about embodied AI, research, and collaboration.",
        "contact_pending": "Contact details to be added", "email": "Email", "cv": "CV", "updated": "Updated", "draft_footer": "Draft · Not published",
    },
    "zh": {
        "lang": "zh-CN", "switch": "English", "switch_file": "index.html", "edition": "个人主页",
        "skip": "跳转到正文", "photo": "个人照片待补充", "caption": "这里将放置你的个人照片。",
        "draft": "版式预览 · 个人信息、项目细节与照片待补充，示例文案不代表真实履历。",
        "tabs": ["代表工作", "代码与资源", "职业经历"], "selected": "精选论文", "selected_note": "机器人 · 奖励建模 · 三维感知",
        "contribution": "我的贡献", "result": "结果与证据", "visual": "项目图片待补充", "sample": "内容占位",
        "software_title": "代码与项目资源", "software_empty": "让有用的工作被更多人使用。",
        "software_desc": "这里将展示精选代码仓库，说明它们解决的问题，以及我在其中的具体贡献。",
        "about_title": "职业经历", "about_empty": "关于我的更多信息。", "education_title": "教育背景",
        "about_desc": "教育背景、工作经历和当前关注的方向，将在信息确认后补充。",
        "contact": "保持联系。", "contact_desc": "欢迎交流具身智能、技术研究与合作。",
        "contact_pending": "联系方式待补充", "email": "邮件", "cv": "简历", "updated": "更新于", "draft_footer": "草稿 · 尚未发布",
    }
}

for lang, text in labels.items():
    name = tr(profile["name"], lang)
    role = tr(profile["role"], lang)
    intro = tr(profile["intro"], lang)
    social = []
    for key, label in [("email", text["email"]), ("github", "GitHub"), ("scholar", "Scholar"), ("linkedin", "LinkedIn"), ("cv", text["cv"])]:
        value = profile.get(key)
        if value:
            social.append(link("mailto:" + value if key == "email" else value, label))
    if profile.get("photo"):
        photo_class = ' class="rotate-photo"' if profile.get('photo_rotation') == -90 else ''
        portrait = f'<div class="portrait-frame"><img{photo_class} src="{safe_url(profile["photo"])}" alt="{esc(name)}" width="1331" height="2362" fetchpriority="high"></div>'
    else:
        portrait = f'''<div class="portrait-placeholder" role="img" aria-label="{esc(text['photo'])}">
          <svg viewBox="0 0 80 96" aria-hidden="true" fill="none"><circle cx="40" cy="28" r="17" stroke="currentColor" stroke-width="1.3"/><path d="M9 87c0-22 12-33 31-33s31 11 31 33" stroke="currentColor" stroke-width="1.3"/></svg><span>{esc(text['photo'])}</span></div>'''
    draft_note = f'<aside class="draft-note">{esc(text["draft"])}</aside>' if not data["publish_ready"] else ""
    projects = []
    for project in data["projects"]:
        if project.get("image"):
            visual = f'<img src="{safe_url(project["image"])}" alt="{esc(tr(project["title"],lang))}" loading="lazy" width="440" height="320">'
        else:
            visual = f'<div class="placeholder-visual" role="img" aria-label="{esc(text["visual"])}"><b>{esc(project["year"])}</b><span>{esc(text["visual"])}</span></div>'
        project_links = "".join(link(item["url"], tr(item["label"], lang)) for item in project.get("links", []))
        badge = f'<span class="draft-label">{esc(text["sample"])}</span>' if project.get("draft") else ""
        author_line = ''
        if project.get('authors'):
            author_list = ', '.join(f'<strong>{esc(author)}</strong>' if author == 'Yiming Mao' else esc(author) for author in project['authors'])
            author_line = f'<p class="authors">{author_list}</p>'
        role_label = tr(project.get('role_label', text['contribution']),lang)
        projects.append(f'''<article class="project" id="{esc(project['id'])}">
          <div class="project-visual">{visual}</div><div>
          <p class="project-kicker">{esc(tr(project['kind'],lang))} {badge}</p>
          <h3>{esc(tr(project['title'],lang))}</h3>
          {author_line}
          <p class="project-summary">{esc(tr(project['summary'],lang))}</p>
          <dl class="detail"><dt>{esc(role_label)}</dt><dd>{esc(tr(project['contribution'],lang))}</dd></dl>
          <dl class="detail"><dt>{esc(text['result'])}</dt><dd>{esc(tr(project['result'],lang))}</dd></dl>
          <div class="project-links">{project_links}</div></div></article>''')
    software = "".join(f'<article class="software-item"><h3>{link(item["url"],tr(item["name"],lang))}</h3><p>{esc(tr(item["description"],lang))}</p></article>' for item in data["software"])
    if not software:
        software = f'<div class="empty"><h3>{esc(text["software_empty"])}</h3><p>{esc(text["software_desc"])}</p></div>'
    experience_items = []
    for item in data["experience"]:
        company = link(item['url'], tr(item['title'], lang)) if item.get('url') else esc(tr(item['title'], lang))
        description = tr(item.get('description', ''), lang)
        detail = f'<p class="experience-description">{esc(description)}</p>' if description else ''
        current = ' experience-current' if item.get('current') else ''
        experience_items.append(f'''<article class="experience{current}" id="experience-{esc(item['id'])}">
          <div class="company-logo company-logo-{esc(item['id'])}"><img src="{safe_url(item['logo'])}" alt="" aria-hidden="true" loading="lazy"></div>
          <div class="experience-copy"><div class="experience-heading"><h3>{company}</h3><span class="experience-period">{esc(tr(item['period'],lang))}</span></div>
          <p class="experience-role">{esc(tr(item['role'],lang))}</p>{detail}</div></article>''')
    experience = ''.join(experience_items)
    if not experience:
        experience = f'<div class="empty"><h3>{esc(text["about_empty"])}</h3><p>{esc(text["about_desc"])}</p></div>'
    if data.get('experience_note'):
        experience += f'<p class="experience-note">{esc(tr(data["experience_note"],lang))}</p>'
    education_items = []
    for item in data.get("education", []):
        description = tr(item.get("description", ""), lang)
        detail = f'<p class="education-detail">{esc(description)}</p>' if description else ''
        education_items.append(f'''<article class="education-item">
          <div class="institution-logo institution-logo-{esc(item['id'])}"><img src="{safe_url(item['logo'])}" alt="" aria-hidden="true"></div>
          <div><h3>{link(item['url'], tr(item['name'], lang))}</h3><p class="education-role">{esc(tr(item['role'],lang))}</p>{detail}</div>
        </article>''')
    education = f'<section class="education" aria-labelledby="education-title"><h2 id="education-title">{esc(text["education_title"])}</h2><div class="education-grid">{"".join(education_items)}</div></section>' if education_items else ''
    tabs = "".join(f'<a class="tab" id="tab-{key}" href="#{key}">{esc(label)}</a>' for key,label in zip(["highlights","software","about"],text["tabs"]))
    contact = link("mailto:" + profile["email"], text["email"] + " ↗") if profile.get("email") else (link(profile["github"], "GitHub ↗") if profile.get("github") else f'<span class="edition">{esc(text["contact_pending"])}</span>')
    filename = "index.html" if lang == "en" else "zh.html"
    canonical = ""
    if data.get("site_url"):
        base = data["site_url"].rstrip("/") + "/"
        canonical = f'<link rel="canonical" href="{safe_url(base + ("" if lang == "en" else filename))}"><link rel="alternate" hreflang="en" href="{safe_url(base)}"><link rel="alternate" hreflang="zh-CN" href="{safe_url(base + "zh.html")}">'
    robots = "index,follow" if data["publish_ready"] else "noindex,nofollow"
    status = esc(text["draft_footer"]) if not data["publish_ready"] else esc(name)
    alternate_name = f'<span class="alternate-name">{esc(tr(profile["alternate_name"],lang))}</span>' if profile.get('alternate_name') else ''
    document = f'''<!doctype html>
<html lang="{text['lang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="{robots}"><meta name="theme-color" content="#ffffff">
<title>{esc(tr(data.get('page_title', name),lang))}</title>
<meta name="description" content="{esc(intro)}">
<meta property="og:title" content="{esc(name)}"><meta property="og:description" content="{esc(intro)}"><meta property="og:type" content="website">
{canonical}<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{esc(text['skip'])}</a>
<div class="page">
  <div class="utility"><span class="edition">{esc(text['edition'])}</span><a class="language" href="{text['switch_file']}" data-language="{text['switch_file']}" lang="{'zh-CN' if lang=='en' else 'en'}">{esc(text['switch'])}</a></div>
  <header class="hero">
    <div class="hero-copy"><h1>{esc(name)}{alternate_name}</h1><p class="role">{esc(role)}</p><p class="intro">{esc(intro)}</p><p class="bio">{esc(tr(profile['bio'],lang))}</p><p class="focus">{esc(tr(profile['focus'],lang))}</p><nav class="social" aria-label="{'Profile links' if lang=='en' else '个人链接'}">{''.join(social)}</nav></div>
    <figure class="portrait">{portrait}<figcaption>{esc(text['caption']) if not profile.get('photo') else ''}</figcaption></figure>
  </header>
  {education}
  {draft_note}
  <main id="main">
    <nav class="tabs" aria-label="{'Explore my work' if lang=='en' else '浏览我的工作'}">{tabs}</nav>
    <section class="panel" id="highlights"><div class="section-top"><h2>{esc(text['selected'])}</h2><span>{esc(text['selected_note'])}</span></div>{''.join(projects)}</section>
    <section class="panel" id="software"><div class="section-top"><h2>{esc(text['software_title'])}</h2></div>{software}</section>
    <section class="panel" id="about"><div class="section-top"><h2>{esc(text['about_title'])}</h2></div>{experience}</section>
    <section class="contact"><div><h2>{esc(text['contact'])}</h2><p>{esc(text['contact_desc'])}</p></div>{contact}</section>
  </main>
  <footer><span>{status}</span><span>{esc(text['updated'])} {esc(data['updated'])}</span></footer>
</div>
</body>
</html>'''
    (OUT / filename).write_text(document, encoding="utf-8")

(OUT / ".nojekyll").touch()
(OUT / "robots.txt").write_text("User-agent: *\n" + ("Allow: /\n" if data["publish_ready"] else "Disallow: /\n"), encoding="utf-8")
if data.get('site_url') and data['publish_ready']:
    base = data['site_url'].rstrip('/') + '/'
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{esc(url)}</loc><lastmod>{esc(data["updated"])}</lastmod></url>' for url in [base,base+'zh.html']) + '</urlset>',encoding='utf-8')
    with (OUT / 'robots.txt').open('a',encoding='utf-8') as stream:
        stream.write('Sitemap: ' + base + 'sitemap.xml\n')
print(f"Built English and Chinese pages in {OUT}")
