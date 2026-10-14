#!/usr/bin/env python3
"""Regenerate all five pages from content/*.json. Python 3; no packages required."""
from pathlib import Path
import json,re
from html import escape as e
ROOT=Path(__file__).resolve().parent
def load(n):return json.loads((ROOT/'content'/f'{n}.json').read_text())
team,pubs,research,education=[load(n) for n in ['team','publications','research','education']]
highlights=[p for p in pubs if p.get('featured')][:3]
assert len({p['id'] for p in pubs})==len(pubs), 'Publication IDs must be unique'
assert all(p.get('title') for p in highlights), 'Featured publications need titles'
nav=[('index','Home'),('research','Research'),('team','Team'),('publications','Publications'),('education','Education')]
def links(items):return ' '.join(f'<a class="text-link" href="{e(x["url"],quote=True)}">{e(x["label"])} <span aria-hidden="true">↗</span></a>' for x in items)
def page(name,title,content):
 navigation=''.join(f'<a href="{f}.html"'+(' aria-current="page"' if f==name else '')+f'>{t}</a>' for f,t in nav)
 html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Nano Thermal Mechanical Engineering Laboratory</title>
<meta name="description" content="{e(title)} — Yan Wang’s research group at the University of Nevada, Reno. Thermal transport, advanced manufacturing, and energy materials.">
<meta name="theme-color" content="#003366"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script><noscript><style>@media(max-width:760px){{.header-inner{{flex-wrap:wrap;padding-block:15px}}nav{{display:flex;position:static;flex-wrap:wrap;gap:12px;width:100%;padding:0;box-shadow:none;border:0}}nav a{{padding:8px 0}}nav a[aria-current]:after{{bottom:0}}.menu-toggle{{display:none}}}}</style></noscript></head>
<body class="page-{name}"><a class="skip" href="#main">Skip to content</a>
<div class="university"><div class="container"><span>UNIVERSITY OF NEVADA, RENO</span><span>Mechanical Engineering</span></div></div>
<header class="header"><div class="container header-inner"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">W<span>↗</span></span><span>WANG RESEARCH GROUP<small>Nano Thermal Mechanical Engineering Laboratory</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{navigation}</nav></div></header>
<main id="main">{content}</main>
<footer id="contact"><div class="container footer-grid"><div><p class="eyebrow">University of Nevada, Reno</p><h2>Let’s explore what’s next.</h2><p>Interested in our research, collaboration, or joining the group?</p><a class="button light" href="mailto:yanwang@unr.edu">Contact Dr. Yan Wang <span aria-hidden="true">↗</span></a></div><div class="footer-address"><strong>Nano Thermal Mechanical<br>Engineering Laboratory</strong><p>1664 N. Virginia Street<br>Reno, NV 89557-0312<br>Office: PE229</p><a href="mailto:yanwang@unr.edu">yanwang@unr.edu</a><br><a href="tel:+17757846468">(775) 784-6468</a></div></div><div class="container footer-bottom"><span>© <span id="copyright-year">2026</span> Wang Research Group</span><a href="https://www.unr.edu/engineering">College of Engineering ↗</a><a href="#main">Back to top ↑</a></div></footer></body></html>'''
 (ROOT/f'{name}.html').write_text(html)
def intro(label,title,description):return f'<section class="page-intro"><div class="container"><p class="eyebrow">{label}</p><h1>{title}</h1><p class="lede">{description}</p></div></section>'
def heading(kicker,title,link='',label='Explore more'):
 return f'<div class="section-heading"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2></div>'+ (f'<a class="text-link" href="{link}">{label} ↗</a>' if link else '')+'</div>'
areas=[('Thermal & fluid science','Understanding heat carriers, their interactions, and transport across materials and interfaces.','topic-1'),('Advanced manufacturing','Exploring laser–material interactions and the physics of next-generation manufacturing.','topic-2'),('Energy material design','Engineering materials for thermal management, energy conversion, and energy storage.','topic-3'),('Multiphysics modeling','Connecting atomistic insight to coupled thermal, mechanical, chemical, and optical processes.','topic-5')]
area_html=''.join(f'<a class="area" href="research.html#{r}"><span class="index">0{i+1}</span><div><h3>{t}</h3><p>{d}</p></div><span class="arrow" aria-hidden="true">↗</span></a>' for i,(t,d,r) in enumerate(areas))
highlight_html=''.join(f'<a class="publication-teaser" href="publications.html#{h["id"]}"><span class="eyebrow">{h["year"]} / Journal paper</span><h3>{e(h["title"])}</h3><span class="text-link">View publication <span aria-hidden="true">↗</span></span></a>' for i,h in enumerate(highlights[:3]))
home=f'''<section class="hero"><img class="hero-image" src="images/home.jpg" alt="Snow-dusted Nevada mountains above a valley filled with low clouds" fetchpriority="high"><div class="hero-shade"></div><div class="container hero-inner"><p class="eyebrow">Nano Thermal Mechanical Engineering Laboratory</p><h1>Small-scale physics.<br><em>Wide-reaching impact.</em></h1><p class="hero-description">Advancing the science of heat, materials, and energy. <br>From fundamental interactions to engineered possibilities.</p><div class="hero-actions"><a class="button light" href="research.html">Explore our research <span aria-hidden="true">↗</span></a><a class="hero-secondary" href="team.html">Meet the group <span aria-hidden="true">→</span></a></div><div class="hero-bottom"><span>Yan Wang Research Group<br><strong>University of Nevada, Reno</strong></span><span class="landscape-note">Rooted in Nevada. Exploring across scales.</span><a href="#about" aria-label="Scroll to about the laboratory">↓</a></div></div></section>
<section id="about" class="section container about"><div><p class="eyebrow">A closer look. A broader perspective.</p><h2>Understanding energy.<br>Engineering possibility.</h2></div><div><p class="large-copy">We study how thermal and mechanical processes shape the way energy moves, transforms, and can be put to work.</p><p>Led by Dr. Yan Wang, our group combines theoretical and computational approaches to investigate transport across length and time scales—with a focus on energy applications and advanced manufacturing.</p><a class="text-link" href="team.html">Get to know our laboratory ↗</a></div></section>
<section class="research-band"><div class="container section">{heading('What we investigate','Research across scales.','research.html','All research')}<div class="areas">{area_html}</div></div></section>
<section class="section container" id="publications">{heading('From the laboratory','Recent publications.','publications.html','Full publication record')}<div class="teasers">{highlight_html}</div></section>
<section class="people-feature" id="team"><div class="container people-feature-inner"><div><p class="eyebrow">The people behind the science</p><h2>Curiosity is a<br>collaborative pursuit.</h2><p>Meet the researchers exploring thermal transport, materials, and energy at the University of Nevada, Reno.</p><a class="button" href="team.html">Meet our team ↗</a></div><div class="portrait-strip">{''.join(f'<a href="team.html#person-{i}" aria-label="Meet {e(team[i]["name"])}"><img src="{team[i]["image"]}" alt="{e(team[i]["name"])}" loading="lazy"></a>' for i in [0,1,3])}</div></div></section>
<section class="section container education-home" id="education"><p class="eyebrow">Teaching & mentorship</p><h2>The next generation<br>of engineering starts here.</h2><div><p>From heat transfer courses to undergraduate research and K–12 outreach, we connect scientific ideas with hands-on learning.</p><a class="text-link" href="education.html">Explore education & outreach ↗</a></div></section>'''
page('index','Home',home)
pi=team[0]
people=intro('Our people','A shared curiosity.','Meet the people advancing thermal science, materials, and energy in the Wang Research Group.')
people+=f'<section class="section container"><div class="pi" id="person-0"><img src="{pi["image"]}" alt="Portrait of Dr. Yan Wang"><div><p class="eyebrow">Principal investigator</p><h2>{e(pi["name"])}</h2><p class="role">{e(pi["role"])} · Mechanical Engineering</p><p>{e(pi["bio"])}</p><div class="person-links">{links(pi["links"])}</div></div></div></section>'
people+='<section class="team-section section container">'+heading('Research team','Meet the group.')+'<div class="team-grid">'
for i,p in enumerate(team[1:],1):
 people+=f'<article class="person" id="person-{i}"><img src="{p["image"]}" alt="Portrait of {e(p["name"])}" loading="lazy"><div class="person-copy"><p class="eyebrow">{e(p["role"])}</p><h3>{e(p["name"])}</h3><details><summary>Biography <span aria-hidden="true">+</span></summary><p>{e(p["bio"])}</p></details><div class="person-links">{links(p["links"])}</div></div></article>'
people+='</div></section>';page('team','Team',people)
res=intro('Our research','From atoms to applications.','Thermal transport, light–matter interactions, and materials design—connected through theory and computation.')
res+='<div class="container research-layout section"><aside class="topic-nav"><p class="eyebrow">Explore the research</p>'+''.join(f'<a href="#{r["id"]}"><span>0{i+1}</span> {e(r["title"].split(":")[0])}</a>' for i,r in enumerate(research))+'</aside><div>'
for i,r in enumerate(research):
 body=r['body_html'];split=body.find('<h4>');description=body if split<0 else body[:split];extra='' if split<0 else '<details class="research-details"><summary>Related publications & highlights <span aria-hidden="true">+</span></summary>'+body[split:]+'</details>'
 res+=f'<article class="research-topic" id="{r["id"]}"><p class="eyebrow">0{i+1} / {e(r["category"])}</p><h2>{e(r["title"])}</h2><div class="prose">{description}{extra}</div></article>'
res+='</div></div>';page('research','Research',res)
categories=list(dict.fromkeys((p['category_id'],p['category']) for p in pubs));years=sorted(set(p['year'] for p in pubs),reverse=True)
publication=intro('Publications & scholarly activity','Ideas, shared.','Explore journal articles, conference contributions, research tools, and presentations from our group.')
publication+='''<section class="section container publication-section"><div class="filters" hidden><div class="search-field"><label for="search">Search the research record</label><input id="search" type="search" placeholder="Search author, title, journal, or keyword…"></div><div><label for="category">Type</label><select id="category"><option value="">All types</option>'''+''.join(f'<option value="{c}">{e(t)}</option>' for c,t in categories)+'''</select></div><div><label for="year">Year</label><select id="year"><option value="">All years</option>'''+''.join(f'<option>{y}</option>' for y in years)+'''</select></div><button id="reset" class="reset">Clear filters</button></div><p id="result-count" class="result-count" role="status" aria-live="polite">'''+str(len(pubs))+''' records</p><div class="publication-layout"><aside class="publication-nav"><p class="eyebrow">Browse by type</p>'''+''.join(f'<a href="#{c}">{e(t)} <span>{sum(p["category_id"]==c for p in pubs)}</span></a>' for c,t in categories)+'''</aside><div class="records">'''
for c,t in categories:
 publication+=f'<section class="record-group" id="{c}"><h2>{e(t)}</h2><ol class="record-list">'
 for i,p in enumerate(pubs):
  if p['category_id']!=c:continue
  publication+=f'<li class="record" id="{p["id"]}" data-year="{p["year"]}" data-category="{c}"><span class="record-year">{p["year"]}</span><div>{p["citation_html"]}</div></li>'
 publication+='</ol></section>'
publication+='</div></div><div class="empty-state" hidden><h2>No matching records.</h2><p>Try another keyword, year, or publication type.</p></div></section>'
page('publications','Publications',publication)
ed=intro('Education & outreach','Learning through discovery.','Connecting the fundamentals of heat transfer with research, design, and the next generation of engineers.')
ed+='<section class="section container education-list">'
for i,item in enumerate(education):
 ed+=f'<article class="education-item" id="education-{i+1}"><div class="education-image"><img src="{item["image"]}" alt="{e(item["title"])}" loading="lazy"></div><div><p class="eyebrow">0{i+1} / '+e(item.get('category','Education'))+f'</p><h2>{e(item["title"])}</h2><p>{e(item["description"])}</p>'
 if item.get('courses'):ed+='<div class="course-tags">'+''.join('<span>'+e(course)+'</span>' for course in item['courses'])+'</div>'
 else:ed+='<a class="text-link" href="mailto:yanwang@unr.edu">Get in touch to learn more ↗</a>'
 ed+='</div></article>'
ed+='</section>';page('education','Education',ed)
print('Built 5 pages from content files.')
