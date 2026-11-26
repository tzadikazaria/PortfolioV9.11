#!/usr/bin/env python3
"""Generates the V9 pages from one shared template so every page stays consistent."""
import os
from PIL import Image

import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = ROOT + '/assets/'

# ---------------------------------------------------------------- site settings
# Absolute address of the published site (needed for Open Graph previews). Include the trailing slash.
# Override at build time:  SITE_URL=https://yourname.github.io/PortfolioV9/ python3 tools/build_v9.py
SITE_URL = os.environ.get('SITE_URL', 'https://tzadikazaria.com/')

# ---------------------------------------------------------------- helpers
def dims(name):
    with Image.open(A + name + '.webp') as im:
        return im.size

def img(name, alt, sizes='(max-width:700px) 92vw, 50vw', eager=False, cls=''):
    w, h = dims(name)
    ss = []
    for v in (480, 960):
        if os.path.exists(A + f'{name}-{v}.webp') and v < w:
            ss.append(f'assets/{name}-{v}.webp {v}w')
    ss.append(f'assets/{name}.webp {w}w')
    srcset = ', '.join(ss)
    load = 'loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="assets/{name}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}"{c} {load} decoding="async">')

def fig(name, alt, cap=None, num=None, sizes=None, zoom=True, style='', eager=False):
    sz = sizes or '(max-width:700px) 92vw, 40vw'
    im = img(name, alt, sz, eager)
    inner = (f'<button class="zoom" data-lightbox aria-label="Enlarge: {alt}">{im}</button>'
             if zoom else im)
    c = ''
    if cap:
        n = f'<b>{num}</b>' if num else ''
        c = f'<figcaption>{n}<span>{cap}</span></figcaption>'
    st = f' style="{style}"' if style else ''
    return f'<figure class="fg"{st}>{inner}{c}</figure>'

def note(label, text, n=None):
    num = f'<b>{n}</b> ' if n else ''
    return (f'<div class="note wrap"><p class="lab">{num}{label}</p><p class="txt">{text}</p></div>')

def gal(figs, n=3, bg=None, cls='', wide=False):
    body = f'<div class="gal n{n} {cls}">' + ''.join(figs) + '</div>'
    if bg:
        return f'<div class="panel {"wide" if wide else "wrap"}" style="--bg:{bg}">{body}</div>'
    return f'<div class="{"wide" if wide else "wrap"}">{body}</div>'


def band(num, label, text, inner, bg='#F3F3F2', mode='side', dark=False, cls=''):
    """Full-bleed colour band. mode 'side': sticky text column + large images. mode 'top': text row above a wide gallery."""
    lab = f'<p class="lab"><b>{num}</b>{label}</p>' if label else ''
    txt = f'<p class="txt">{text}</p>' if text else ''
    head_ = f'<div class="band-txt">{lab}{txt}</div>' if (label or text) else ''
    d = ' dark' if dark else ''
    return (f'<section class="band {mode}{d} {cls}" style="--bg:{bg}"><div class="band-in">{head_}<div class="band-body">{inner}</div></div></section>')

def g(figs, n=3, cls=''):
    return f'<div class="gal n{n} {cls}">' + ''.join(figs) + '</div>'

# ---------------------------------------------------------------- shared chrome
def head(title, desc, body_class, robots='', og=None, home=False):
    ogm = ''
    if og:
        ogm = (f'<meta property="og:type" content="website"><meta property="og:image" content="{SITE_URL}assets/og/{og}.jpg">'
               f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
               f'<meta property="og:image:alt" content="Selected work by Tzadik Azaria">'
               f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE_URL}assets/og/{og}.jpg">')
    return f'''<!doctype html><html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#F3F3F2"><meta name="description" content="{desc}">{robots}<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">{ogm}<title>{title}</title><link rel="icon" href="favicon-tz-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)"><link rel="icon" href="favicon-tz-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)"><link rel="apple-touch-icon" href="apple-touch-icon-v94.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="v9.css"><script src="app.js" defer></script></head><body class="{body_class}"><a class="skip" href="#main">Skip to content</a>
'''

def header(current):
    def cur(k):
        if k == current:
            return ' aria-current="page"'
        # project pages: the Projects link marks the section the visitor is in
        return ' aria-current="true"' if (current == 'section' and k == 'work') else ''
    return f'''<header class="site-header" id="siteheader"><div class="hdr"><a class="brand" href="index.html" aria-label="Tzadik Azaria — home"><svg class="logo" role="img" aria-label="Tzadik" viewBox="0 0 117 35" fill="currentColor" xmlns="http://www.w3.org/2000/svg"> <path d="M37.1564 4.64562L37.1545 4.65131L28.2211 28.5096H32.526L30.4352 34.5H19.3094L21.0225 29.9664L24.1695 21.6005L25.112 19.0617L25.1129 19.0589L29.9721 6.03693H21.3063V0H38.8818L37.1564 4.64562Z" /> <path d="M19.3892 5.90406H12.797V34.4943H6.59402V5.90406H0V0.000949054H19.3892V5.90406Z" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M49.2473 0.000949054H51.3106L64.2339 34.4943H57.5146L54.563 26.5631H42.8536L39.9011 34.4943H33.1799L46.1534 0.000949054H48.2233L48.7368 0L49.2473 0.000949054ZM45.0649 20.622H52.3593L48.7235 10.8401L45.0649 20.622Z" /> <path d="M102.191 9.38994L108.365 0.000949054H116.034L104.317 17.2861L116.101 34.4943H108.37L102.191 25.1822V34.4943H95.9863V0.000949054H102.191V9.38994Z" /> <path d="M92.5897 34.4934H86.3867V0H92.5897V34.4934Z" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M65.9497 0.00474527C69.5105 0.00483633 72.6817 0.639252 75.3492 1.93512C81.1321 4.70135 84.0614 10.2331 84.0615 17.2946C84.0615 17.7243 84.0494 18.1661 84.0245 18.5977L84.0235 18.6214L84.0207 18.6451L83.9941 19.0295C83.9836 19.1686 83.9687 19.3233 83.9523 19.467C83.7431 21.7793 83.1843 23.9159 82.2687 25.8114L82.2621 25.8238L82.2573 25.8361L81.9954 26.3334C81.9095 26.4908 81.8259 26.6386 81.7524 26.77L81.1422 27.8623H81.0406C79.8883 29.4922 78.4177 30.8483 76.657 31.9005L76.6465 31.9062L76.0543 32.2403C75.45 32.5647 74.8076 32.8605 74.1249 33.1144L74.1239 33.1134C73.0869 33.5118 71.9676 33.8349 70.7795 34.0568L70.5859 34.0938H67.3221L66.8077 32.6987L66.5401 31.9765L57.4102 7.74333L57.4083 7.73858L56.2514 4.64467L56.2504 4.64372L54.5174 0.00474527H65.9497ZM68.293 19.0523L68.2939 19.056L69.2363 21.5948L71.5425 27.7266C71.8018 27.6319 72.0504 27.5306 72.2875 27.421L72.2951 27.4172C72.9233 27.1299 73.4905 26.789 74.0157 26.4008C74.6381 25.9278 75.1645 25.4215 75.5997 24.8586L75.6007 24.8576C75.7712 24.6373 75.9121 24.4431 76.0268 24.2607L76.0391 24.2426L76.0505 24.2236C76.9368 22.8759 77.5154 21.1668 77.7123 19.0646L77.7161 19.0285L77.7199 18.9934C77.7447 18.7997 77.7624 18.5925 77.7712 18.3841L77.7731 18.3367L77.7778 18.2902C77.8022 18.0079 77.8034 17.7005 77.8034 17.2946C77.8034 13.8413 76.9242 11.2344 75.3985 9.426C73.9038 7.6545 71.5868 6.41146 68.2047 6.03124H63.4366L68.293 19.0523Z" /> </svg> </a><nav class="nav" id="navigation" aria-label="Main navigation"><div class="nav-main"><a href="index.html#work"{cur('work')}>Projects</a><a href="about.html"{cur('about')}>About</a><a href="#contact">Contact</a></div><div class="nav-side"><a class="pill" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV</a></div></nav><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu</button></div></header>
'''

FOOTER = '''<footer class="footer" id="contact"><div class="wrap"><p class="eyebrow">Have something in mind?</p><a class="footer-title" href="mailto:tzadikazaria@gmail.com">Let’s work <em>together.</em></a>
<div class="footer-grid">
<div class="fg-mail"><p class="fl">Email</p><span class="mail"><a href="mailto:tzadikazaria@gmail.com">tzadikazaria@gmail.com</a><button class="copy" type="button" data-copy="tzadikazaria@gmail.com" aria-label="Copy email address">Copy</button></span></div>
<div><p class="fl">Elsewhere</p><ul><li><a href="https://www.linkedin.com/in/tzadik-azaria" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a></li><li><a href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV ↓</a></li></ul></div>
<div><p class="fl">Site</p><ul><li><a href="index.html#work">Projects</a></li><li><a href="about.html">About</a></li><li><a href="#top">Back to top ↑</a></li></ul></div>
<div class="fg-status"><p class="fl">Status</p><p class="fstatus">Open to full-time opportunities</p></div>
</div>
<p class="fcopy">© 2026 Tzadik Azaria</p></div></footer>
<dialog class="lightbox" aria-label="Project image viewer"><button class="lightbox-close" aria-label="Close image viewer">Close ×</button><button class="lb-nav prev" aria-label="Previous image">←</button><button class="lb-nav next" aria-label="Next image">→</button><div class="lightbox-inner"><img alt=""><p></p></div></dialog></body></html>'''

# ---------------------------------------------------------------- projects
PROJECTS = [
    dict(slug='campaign', n='01', title='Campaign &amp; <em>digital design.</em>', short='Campaign &amp; Digital Design',
         kind='real', kind_label='Commercial work', bg='#171719',
         cat='Commercial design', tag='Campaigns · Social · Email · Banners',
         blurb='Multi-channel creative across social, web, email and paid media for beauty and lifestyle brands.',
         desc='Commercial campaign and promotional visuals for beauty and wellness brands, designed for social, web, email and banners.',
         lead='Multi-channel creative across social, web, email and paid media for beauty and lifestyle brands.',
         detail='Commercial work for the boutique retailer Fine Rituals, designed for social, web, email and paid media. The featured products belong to different brands.',
         meta=[('Work', 'Commercial'), ('Store', 'Fine Rituals (OG Global Import)'), ('Formats', 'Social · Web · Email · Paid'), ('Platforms', 'Meta Ads · Google Ads · Flashy')]),
    dict(slug='marketplace', n='02', title='Marketplace<br><em>product visuals.</em>', short='Marketplace Product Visuals',
         kind='real', kind_label='Commercial work', bg='#E8E4DE',
         cat='E-commerce systems', tag='E-commerce · Infographics · Systems',
         blurb='Scalable product-listing systems designed to communicate benefits quickly across multiple beauty and wellness brands.',
         desc='Product listing visuals for beauty and wellness brands on Asian e-commerce marketplaces.',
         lead='Designing scalable product visuals for beauty and wellness brands across Asian e-commerce marketplaces, turning product benefits into clear, consistent listing systems.',
         detail='Benefits, product photography and usage information organized into layouts that stay clear at different sizes.',
         meta=[('Role', 'Digital & visual designer'), ('Focus', 'Scalable listings'), ('Markets', 'Asia / E-commerce'), ('Output', 'Product visual systems')]),
    dict(slug='hatachana', n='03', title='Hatachana', short='Hatachana',
         kind='acad', kind_label='Academic concept', bg='#ECBA40',
         cat='Brand + mobile experience', tag='Identity · Illustration · Mobile UI',
         blurb='Brand identity and digital experience for guided tours inside Tel Aviv’s Central Bus Station.',
         desc='Academic concept: an identity, character illustrations and a mobile app for guided tours of Tel Aviv’s Central Bus Station.',
         lead='Brand identity and digital experience for guided tours inside Tel Aviv’s Central Bus Station.',
         detail='Hatachana is Hebrew for “the station”. The concept presents the Central Bus Station as a place to explore through guided tours. A yellow, black and white palette and illustrated explorer characters carry from the identity into the app.',
         meta=[('Project', 'Academic concept'), ('Type', 'Brand identity &amp; digital experience'), ('Deliverables', 'Identity · Illustration · Iconography · Mobile app'), ('Subject', 'Tel Aviv Central Bus Station'), ('Focus', 'Guided tours')]),
    dict(slug='sambusak', n='04', title='Give Me<br><em>Sambusak.</em>', short='Give Me Sambusak',
         kind='acad', kind_label='Academic concept', bg='#DDDADF',
         cat='Brand experience', tag='Identity · Packaging · Spatial',
         blurb='A playful street-food identity spanning packaging, spatial design and a self-ordering experience.',
         desc='Academic concept: a street-food identity applied to packaging, a physical stand and a self-ordering interface.',
         lead='A playful street-food identity spanning packaging, spatial design and a self-ordering experience.',
         detail='Hebrew lettering, playful food icons and a bright palette carry one character from takeaway packaging to environmental graphics and a digital ordering interface.',
         meta=[('Project', 'Academic concept'), ('Scope', 'Identity · Packaging · Space · UI'), ('Subject', 'Street food'), ('Digital', 'Self-ordering flow')]),
]
BY = {p['slug']: p for p in PROJECTS}

# thumbnails for the "next project" card
NEXT_THUMB = {
    'campaign': ('#171719', 'campaign-04', 'Fine Rituals Tax Free campaign'),
    'marketplace': ('#E8E4DE', 'marketplace-09', 'Beauty product listing with benefit icons'),
    'hatachana': ('#ECBA40', 'hatachana-00', 'Hatachana identity and app overview'),
    'sambusak': ('#DDDADF', 'home-07-cut', 'Give Me Sambusak packaging'),
}

# ---------------------------------------------------------------- case-study body per project
def cover(bg, ar, inner, cls=''):
    return f'<div class="cover {cls}" style="--bg:{bg};--ar:{ar}">{inner}</div>'

def M(*items, cls=''):
    """12-column editorial grid. items are fig() strings."""
    return f'<div class="mx {cls}">' + ''.join(items) + '</div>'

def F(name, alt, cap, cols, row=None, pct=40, num=None, extra=''):
    st = f'grid-column:{cols};' + (f'grid-row:{row};' if row else '') + extra
    return fig(name, alt, cap, num, sizes=f'(max-width:700px) 92vw, {pct}vw', style=st)

def sec(num, label, heading, text, body='', mode='side', extra=''):
    """White editorial section: small heading + paragraph, images beside or below."""
    mode = mode if body else 'text'
    paras = ''.join(f'<p>{t}</p>' for t in ([text] if isinstance(text, str) else text) if t)
    t = (f'<div class="sx-t"><p class="lab"><b>{num}</b>{label}</p>{'<h2>'+heading+'</h2>' if heading else ''}{paras}{extra}</div>')
    bb = f'<div class="sx-b">{body}</div>' if body else ''
    return f'<section class="sx {mode}"><div class="sx-in">{t}{bb}</div></section>'

def steps(items, cls=''):
    li = ''.join(f'<li><b>{n:02d}</b><strong>{t}</strong>' + (f'<span>{d}</span>' if d else '') + '</li>' for n, (t, d) in enumerate(items, 1))
    return f'<ol class="steps {cls}">{li}</ol>'

def outs(items):
    li = ''.join(f'<li><strong>{t}</strong>' + (f'<span>{d}</span>' if d else '') + '</li>' for t, d in items)
    return f'<ul class="outs">{li}</ul>'

def sw(items, cls=''):
    li = ''.join(f'<li><i style="background:{h}"></i><b>{n}</b><span>{h}</span></li>' for n, h in items)
    return f'<ul class="sw {cls}">{li}</ul>'

def ph(label, ar='1.6', n=1):
    """Marked placeholder for an original image that has not been supplied yet."""
    return ''.join(f'<div class="ph" style="--ar:{ar}" role="img" aria-label="Image needed: {label}"><span><b>Image needed</b>{label}</span></div>' for _ in range(n))

def chips(items):
    return '<ul class="chips">' + ''.join(f'<li>{t}</li>' for t in items) + '</ul>'

def body_campaign():
    out = []
    out.append(cover('#fff', '2.05', '<div class="trio">'
               + img('campaign-04', 'Fine Rituals Tax Free campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-01', 'Beauty serum product campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-03', 'Fine Rituals Mystery Box campaign', '(max-width:700px) 40vw, 26vw', True)
               + '</div>'))
    out.append(sec('01', 'Context', 'Different brands, across digital channels.',
        ['Fine Rituals was OG Global Import’s Israeli online retail store, a boutique beauty and lifestyle retailer carrying several brands, each with its own products, audiences and visual identity. I designed digital campaigns, social media assets, newsletters and website visuals for this retail activity, promoting those products for launches, sales and brand-awareness moments.',
         'Each piece had to work on the website, social, paid media and email without losing its core visual idea. The brand identities of the featured products are not my work; the layouts, adaptations and campaign assets are.']))
    out.append(sec('02', 'My role', 'Design and adaptation.',
        'I worked on the visual design and production of campaign creative, adapting each idea for e-commerce, social, paid media and email. I worked alongside marketing, sales and operations, and prepared assets for Meta Ads, Google Ads and Flashy.'))
    out.append(sec('03', 'Campaign system', 'A flexible visual language.', 'Offers, launches and awareness posts share a simple structure: one product or portrait as the focus, a short message, and a clear offer. The layout flexes to fit each product and brand.',
        M(F('campaign-16', 'Cleansing mousse campaign — pink product composition', 'Cleansing mousse', '1/9', '1/3', 62),
          F('campaign-02', 'Plenaire skincare promotional design', 'Plenaire skincare', '9/13', '1/2', 31),
          F('campaign-20', 'Fine Rituals candle campaign — green composition', 'Candle campaign', '9/13', '2/3', 31))))
    out.append(sec('04', 'Formats', 'The same idea, different formats.', 'Product-in-use shots, hero visuals and bundle offers were adapted to different formats, including a Yom Ha’atzmaut post and a web and commerce piece. Holiday promotions were laid out as both square and vertical versions of the same design.',
        M(F('campaign-14', 'Skincare campaign — product in use', 'Product in use', '1/9', '1/3', 62),
          F('campaign-11', 'Beauty serum hero visual', 'Product-led hero', '9/13', '1/2', 31),
          F('campaign-23', 'Signature skincare bundle campaign', 'Product bundle', '9/13', '2/3', 31))
        + M(F('campaign-27', 'Three holiday promotions, each shown as a square and a vertical layout', 'Three holiday promotions, each as a square and a vertical layout', '3/11', None, 66), cls='again')))
    out.append(sec('05', 'Selected campaign', 'Flame Sale.', 'The Flame Sale was laid out as a website banner and a social post (and a newsletter, shown below). The same dark red look carries across all three.',
        M(F('campaign-08', 'Flame Sale website banner', 'Website banner', '1/9', None, 62),
          F('campaign-09', 'Flame Sale social campaign', 'Social', '9/13', None, 31))))
    out.append(sec('06', 'Selected campaign', 'The White Holiday.', 'A three-story series, each story with its own offer: up to 25% on selected collections, 20% on home products, and 15% on skincare and fragrance. A product group, a candle close-up and a portrait share one layout and one type treatment.',
        M(F('campaign-26', 'The White Holiday story series shown as three Instagram story ads', 'Story series as shown in Instagram', '1/13', None, 92)), 'top'))
    out.append(sec('07', 'Web & social', 'Social, web and paid.', 'Campaign creative sat inside the online store as homepage banners, promotional graphics and product pages, and in the social feed as posts and stories.',
        M(F('campaign-06', 'Website product page shown on a laptop', 'Website product page', '1/8', None, 56, extra='align-self:center'),
          F('campaign-35', 'Instagram profile grid and a promotional story shown on two phones', 'Social feed and campaign post', '8/13', None, 40, extra='align-self:center'))))
    out.append(sec('08', 'Story ads', 'Shown in the feed.', 'Story creative as it appears in Instagram, each with a Shop now button.',
        '<div class="gal n4 phones">'
        + fig('campaign-29', 'Flame Sale story ad in the Instagram interface', 'Flame Sale', sizes='(max-width:700px) 58vw, 22vw')
        + fig('campaign-38-2', 'Candle story ad with a Shop now button', 'Candle', sizes='(max-width:700px) 58vw, 22vw')
        + fig('campaign-42-2', 'Skincare jar story ad with a Shop now button', 'Skincare', sizes='(max-width:700px) 58vw, 22vw')
        + fig('campaign-36-2', 'Skincare gift story ad with a Shop now button', 'Skincare gift', sizes='(max-width:700px) 58vw, 22vw')
        + '</div>', 'top'))
    out.append(sec('09', 'Email & newsletter design', 'The campaign, in the inbox.',
        ['Newsletters carry the same campaign language into a direct channel for launches and promotions. The layouts are single-column: a header, a hero visual, then offer or product blocks with clear shop buttons. Some add customer reviews and an Instagram strip.',
         'Both newsletters shown use Hebrew copy set right to left.'],
        M(F('campaign-07', 'Flame Sale newsletter, full layout', 'Flame Sale newsletter', '1/5', None, 30),
          F('campaign-13', 'Skincare newsletter, full layout', 'Skincare newsletter', '6/9', None, 27, extra='max-width:377px'))))
    out.append(sec('10', 'Campaign operations', 'Beyond the layout.', 'I prepared campaign assets for Meta Ads, Google Ads and Flashy, and took part in newsletter scheduling and automation setup.',
        chips(['Meta Ads', 'Google Ads', 'Flashy']), 'top'))
    out.append(sec('', 'More from the collection', '', '',
        M(F('campaign-15', 'Skincare supporting campaign imagery', None, '1/5', None, 31),
          F('campaign-17', 'Beauty promotional campaign on red', None, '5/9', None, 31, extra='margin-top:clamp(32px,5vw,80px)'),
          F('campaign-21', 'Fine Rituals beauty promotion', None, '9/13', None, 31)), 'top'))
    out.append(sec('11', 'Delivered', 'What the work covered.', '',
        outs([('Social', 'Promotional posts and stories.'), ('Web', 'Banners and product-page graphics.'), ('Email', 'Newsletter layouts.'), ('Paid', 'Creative assets for ad platforms.')]), 'top'))
    return out

def body_marketplace():
    out = []
    out.append(cover('#fff', '2.05', '<div class="trio flat">'
               + img('marketplace-09', 'Beauty product listing with benefit icons', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-02', 'Lip product benefit listing', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-11', 'Razor product visual', '(max-width:700px) 40vw, 26vw', True)
               + '</div>'))
    out.append(sec('01', 'Context & objectives', 'Clear fast. Consistent everywhere.',
        ['This work was part of OG Global Import’s international e-commerce operations across Asian markets, where beauty and wellness brands were sold through several marketplaces. It is separate from Fine Rituals, OG Global Import’s Israeli online store. Each marketplace needed product visuals that explained the benefits quickly and clearly, often in limited space and with different image requirements.',
         'The challenge was a scalable visual system that adapts to different brands and product types while staying consistent, informative and on-brand. My work covers the listing visuals, not the brands’ own identities.']))
    out.append(sec('02', 'My role', 'Four parts of one system.', 'I designed the icons and the listing images, and prepared them for each platform.',
        steps([('Icon library', 'Product-benefit icons, each communicating a single claim in one visual language.'), ('Scalable system', 'The same icon style applied across product categories for coherence.'),
               ('Photography integration', 'Full listing images that combine icons with product photography.'), ('Platform delivery', 'Sized and formatted to each platform’s requirements across several Asian markets.')], 'again'), 'top'))
    out.append(sec('03', 'Icon system', 'One icon. One message.', 'Each icon is a thin line drawing in a circle and carries one claim, from hydrating and long-lasting to vegan and cruelty-free. The shared frame keeps them consistent across categories, and keeps listings easy to scan.',
        M(F('marketplace-01', 'Set of benefit icons with labels', None, '1/13', None, 92)), 'top'))
    out.append(sec('04', 'Visual system', 'Same logic. New product.', 'Each family follows the same order: ingredients explained first, then benefits, then the product in context. The structure stays fixed, while photography, colour and tone change with the product.',
        M(F('marketplace-03', 'Mascara ingredient benefit layout', 'Ingredients — mascara', '1/5', None, 31),
          F('marketplace-14', 'Eyeliner ingredient benefit layout', 'Ingredients — eyeliner', '5/9', None, 31),
          F('marketplace-16', 'Skincare active ingredient visual', 'Ingredients — skincare', '9/13', None, 31))
        + M(F('marketplace-02', 'Lipstick benefit listing', 'Benefits — lipstick', '1/5', None, 31),
            F('marketplace-09', 'Deodorant balm benefit listing', 'Benefits — deodorant', '5/9', None, 31),
            F('marketplace-19', 'Skincare benefits layout with portrait photography', 'Benefits — skincare', '9/13', None, 31), cls='again')
        + M(F('marketplace-05', 'Deodorant ingredient and benefit layout on stone', 'In context — ingredient story', '1/7', None, 46),
            F('marketplace-17', 'Deodorant held in warm light', 'In context — product photography', '7/13', None, 46), cls='again'), 'top'))
    out.append(sec('05', 'Listing system', 'Hero. Benefits. Usage.', 'A listing set opens with the product, explains what makes it different through icons and short claims, then shows it in use. The razor set shows the full sequence, with supporting visuals for detail and sustainability.',
        M(F('marketplace-06', 'Razor hero product image', 'Hero — the product first', '1/5', None, 31, num='01'),
          F('marketplace-12', 'Razor feature overview with icons', 'Benefits — features as icons', '5/9', None, 31, num='02'),
          F('marketplace-08', 'Razor usage demonstration', 'Usage — shown in use', '9/13', None, 31, num='03'))
        + M(F('marketplace-11', 'Razor handle detail', 'Hero — handle detail', '1/7', None, 46),
            F('marketplace-04', 'Razor refills with sustainability icons', 'Benefits — refills and sustainability', '7/13', None, 46), cls='again'), 'top'))
    out.append(sec('06', 'Platforms & markets', 'One system. Several platforms.', 'The visual language stays the same while sizes, hierarchy and the amount of information change to suit each platform’s requirements. Keeping the layouts modular makes them easier to localise and to reuse for new products.',
        M(F('marketplace-18', 'Eyeliner thin and flat applicator comparison', 'Another category, same layout logic', '1/13', None, 56, extra='max-width:min(100%,640px)')), 'side'))
    out.append(sec('07', 'Final applications', 'What the work covered.', '',
        outs([('Icon library', 'Benefit icons in one style.'), ('Listing image sets', 'Per product, combining icons and photography.'), ('Platform versions', 'Sized for each marketplace.')]), 'top'))
    return out

def body_hatachana():
    out = []
    out.append(cover('#fff', '2.165', '<div class="full">' + img('hatachana-00', 'Hatachana identity and app overview', '100vw', True) + '</div>', 'fullimg'))
    out.append(sec('01', 'Context & objectives', 'From curiosity to a guided visit.', ['Tel Aviv’s Central Bus Station has become an attraction for people interested in unusual and abandoned urban spaces. The challenge was to turn that curiosity into a guided experience that feels safe, accessible and easy to navigate.',
        'The brief called for a visual identity and a mobile app that lets users discover tours, view details and register for a guided visit.']))
    out.append(sec('02', 'Visual identity', 'Industrial, but approachable.',
        ['The identity balances the raw, urban character of the station with a clear, approachable digital system. Industrial neutrals set the atmosphere, while a strong yellow adds visibility, guidance and a sense of movement through the space.',
         '<b>Wordmark and icon.</b> A bold Hebrew wordmark paired with a compact icon, built to move between physical and digital applications.',
         '<b>Typography.</b> A Hebrew type scale with two heading sizes (24 and 20 px) and two text sizes (14 and 12 px).'],
        M(F('hatachana-wordmark', 'Hatachana wordmark and icon on black, with the tagline', 'Wordmark, icon and tagline', '1/8', None, 62))
        + M(F('hatachana-board-type', 'Hatachana typography scale and colour palette with hex values', 'Typography and colour', '1/10', None, 70), cls='again'), 'top'))
    out.append(sec('03', 'Illustration & design system', 'People first, then components.',
        ['Character illustrations make the experience feel more human against the station’s heavier urban character. The same explorers appear in the identity and inside the app.',
         'Line icons for bookmarks, time, date, price, home and profile sit with reusable buttons and form fields, so every screen draws on the same parts.'],
        '<div class="chars three" style="max-width:640px">' + img('hatachana-01', 'Female urban explorer illustration', '(max-width:700px) 30vw, 300px')
        + img('hatachana-02', 'Male urban explorer illustration', '(max-width:700px) 30vw, 300px') + '</div>'
        + M(F('hatachana-board-comp', 'Hatachana buttons, form fields and character illustrations', 'Components and illustrations', '1/13', None, 92), cls='again')
        + M(F('hatachana-icons', 'Hatachana line icon set: bookmark, clock, calendar, home, price tag, profile', 'Icon set', '1/6', None, 40, extra='max-width:454px'), cls='again'), 'top'))
    def ph(items, n, size):
        return f'<div class="gal n{n} phones">' + ''.join(fig(a, b, c, sizes=size) for a, b, c in items) + '</div>'
    out.append(sec('04', 'Digital experience', 'Discover. Choose. Book.', 'The core of the app is tour discovery and booking: a card list of tours, a detail page with duration, price, date, guide and group size, and a booking confirmation. Onboarding and account screens support it.',
        ph([('hatachana-s-list', 'Tour browsing screen with tour cards', 'Discover — tour list'),
            ('hatachana-s-details', 'Tour details screen', 'Choose — tour details'),
            ('hatachana-s-popup', 'Booking confirmation popup', 'Book — confirmation')], 3, '(max-width:700px) 46vw, 24vw')
        + '<p class="sublab" style="margin:clamp(36px,5vw,64px) 0 14px">Getting started</p>'
        + ph([('hatachana-s-splash1', 'Onboarding screen with the explorer holding a camera', 'Onboarding'),
              ('hatachana-s-splash2', 'Onboarding screen with the walking traveller', 'Onboarding'),
              ('hatachana-s-signup', 'Sign-up form', 'Sign-up'),
              ('hatachana-s-login', 'Sign-in screen with wordmark', 'Sign-in')], 4, '(max-width:700px) 46vw, 16vw'), 'top'))
    out.append(sec('05', 'Final applications', 'The identity in use.', 'The wordmark, illustration and palette carry from the app to a landing page, shown here on a laptop. Hatachana is an academic concept, not a client project.',
        M(F('hatachana-web', 'Hatachana landing page', 'Landing page', '1/7', None, 46),
          F('hatachana-laptop', 'Hatachana landing page on a laptop', 'Landing page on a laptop', '7/13', None, 46))
        + '<div style="margin-top:clamp(40px,6vw,88px)">' + outs([('Identity', 'Wordmark, icon and colour palette.'), ('Illustration', 'Explorer characters.'), ('Design system', 'Type scale, icons, buttons and form fields.'), ('Mobile app', 'Tour discovery, details, booking, onboarding and sign-in.'), ('Landing page', 'Web layout with app store badges.')]) + '</div>', 'top'))
    return out

def body_sambusak():
    out = []
    out.append(cover('#fff', '2.05', '<div class="one">' + img('home-07-cut', 'Give Me Sambusak paper bag, box, wrapping and cup packaging', '(max-width:700px) 90vw, 760px', True) + '</div>'))
    out.append(sec('01', 'Challenge', 'One dish. A whole brand.', ['The brief was to build a complete street-food brand around a single dish, from identity and packaging to a physical exhibition stand and a digital ordering experience.',
        'The challenge was to take sambusak, a familiar Middle Eastern pastry, and make it feel relevant, playful and desirable to a younger Tel Aviv audience.']))
    out.append(sec('02', 'Concept', 'Familiar food, younger language.', ['The concept puts a traditional food in a younger, more expressive visual language. Bold colour and playful graphics sit against deliberately rough cardboard, a contrast between the dish’s roots and a contemporary street-food feel.',
        'Customisation became part of the idea: the sambusak is something people build around their own taste.']))
    out.append(sec('03', 'Identity', 'Built to be seen from a distance.', 'An energetic palette of yellow, blue and pink, bold graphic symbols and an informal typographic style. The Hebrew wordmark leads, and a small set of illustrated symbols extends the brand beyond the logo into packaging, signage and interfaces.',
        '<div class="stack">' + fig('sambusak-02', 'Give Me Sambusak Hebrew wordmark', 'Logo', sizes='(max-width:700px) 92vw, 60vw')
        + fig('sambusak-01', 'Give Me Sambusak typography, palette and food icon system', 'Graphic language — typography, palette and icons', sizes='(max-width:700px) 92vw, 60vw').replace('<figure class="fg"', '<figure class="fg ondark"') + '</div>'))
    out.append(sec('04', 'Packaging', 'Cardboard as part of the brand.', 'The same system runs across takeaway bags, food containers and supporting materials. Plain cardboard surfaces are left visible as part of the brand, not hidden.',
        M(F('sambusak-03', 'Branded kraft paper bag on a café table', 'Paper bag', '1/8', None, 56),
          F('sambusak-04', 'Physical Give Me Sambusak packaging samples', 'Packaging samples', '6/13', '2/3', 50, extra='margin-top:calc(-1 * clamp(24px,5vw,80px));z-index:2'))
        + M(F('sambusak-05', 'Yellow and blue branded takeaway cups', 'Takeaway cups', '3/11', None, 66), cls='again'), 'top'))
    out.append(sec('05', 'The stand', 'A branded environment.', 'The stand is built from cardboard boxes, so the material itself becomes part of the identity. Graphics, packaging and physical form were designed together as one environment, not a neutral display.',
        M(F('sambusak-06', 'Branded street-food stand front', 'Stand — front', '1/4', None, 24, extra='align-self:end'),
          F('sambusak-07', 'Give Me Sambusak branded environmental panels', 'Environmental panels', '4/10', None, 46, extra='align-self:center'),
          F('sambusak-08', 'Street-food stand side with oversized graphics', 'Stand — side', '10/13', None, 24, extra='margin-top:clamp(40px,6vw,96px)')), 'top'))
    out.append(sec('06', 'Ordering experience', 'Build your own sambusak.', 'A self-ordering tablet carries the same personality into a working ordering flow. Users can pick a ready-made option or build their own by choosing size, dough, filling, toppings and dips.',
        M(F('sambusak-09', 'Give Me Sambusak self-ordering tablet interface', 'Self-ordering interface', '1/13', None, 92)), 'top'))
    out.append(sec('07', 'One identity, every touchpoint', 'What changes, and what stays.', 'The wordmark, palette and illustrated symbols stay fixed. What changes is the surface they sit on.', 
        outs([('Packaging', 'Pattern and symbols printed on cardboard, which stays visible.'), ('Stand', 'Large graphics on stacked boxes, readable from a distance.'), ('Digital', 'The same colours and symbols on the ordering screens, with build-your-own steps.')]), 'top'))
    return out

BODIES = dict(campaign=body_campaign, marketplace=body_marketplace, hatachana=body_hatachana, sambusak=body_sambusak)

def case_page(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % 4]
    prv = PROJECTS[(i - 1) % 4]
    meta = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p['meta'])
    badge_cls = 'real' if p['kind'] == 'real' else 'acad'
    note_txt = '' if p['kind'] == 'real' else '<span class="acad-note">Academic concept — not a client project</span>'
    nbg, nimg, nalt = NEXT_THUMB[nxt['slug']]
    nxt_img = img(nimg, nalt, '(max-width:700px) 80vw, 380px')
    html = head(f"{p['short'].replace('&amp;','&amp;')} — Tzadik Azaria", p['desc'], 'inner case' + (' ff2' if p['slug'] in ('marketplace', 'hatachana') else ''), og='og-' + p['slug'])
    html += header('section')
    html += f'''<main id="main">
<section class="ch wrap">
<div class="ch-top"><a class="back-link" href="index.html#work">← Selected work</a><span class="kind {badge_cls}">{p['kind_label']}</span></div>
<div class="ch-main"><h1 class="ct">{p['title']}</h1><div class="ci"><p class="cl">{p['lead']}</p>{note_txt}</div></div>
<dl class="cm">{meta}</dl>
</section>
'''
    html += '\n'.join(BODIES[p['slug']]())
    nfg = ''
    html += f'''
<section class="nxb{nfg}" style="--bg:{nbg}" aria-label="Next project"><div class="nxb-top wide"><span class="lab">Project {p['n']} of 04</span><a class="prev-link" href="{prv['slug']}.html">← {prv['short']}</a></div>
<a class="nxb-a wide" href="{nxt['slug']}.html"><div class="nxb-t"><span class="lab">Next project</span><span class="nx-h">{nxt['short']}</span><span class="kind {'real' if nxt['kind']=='real' else 'acad'}">{nxt['kind_label']}</span></div><span class="nxb-m">{nxt_img}<span class="go" aria-hidden="true">↗</span></span></a></section>
</main>
'''
    html += FOOTER
    open(f"{ROOT}/{p['slug']}.html", 'w').write(html)


# ---------------------------------------------------------------- draft pages (not linked from the homepage)
NOINDEX = '<meta name="robots" content="noindex,nofollow">'

def draft_page(slug, title, short, lead, desc, meta, body):
    html = head(f'{short} — Tzadik Azaria', desc, 'inner case', NOINDEX)
    html += header('section')
    mt = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in meta)
    html += f"""<main id="main">
<section class="ch wrap">
<div class="ch-top"><a class="back-link" href="index.html#work">← Selected work</a><span class="kind acad">Academic concept</span></div>
<div class="ch-main"><h1 class="ct">{title}</h1><div class="ci"><p class="cl">{lead}</p><span class="acad-note">Academic concept — not a client project</span><span class="acad-note draft-note">Draft page — original images still needed</span></div></div>
<dl class="cm">{mt}</dl>
</section>
"""
    html += '\n'.join(body)
    html += '\n</main>\n' + FOOTER
    open(f'{ROOT}/{slug}.html', 'w').write(html)

def body_tree():
    out = []
    out.append(cover('#fff', '2.05', ph('Hero: two phones showing the Tree Tower build screen and tower view', '2.05')))
    out.append(sec('01', 'Challenge', 'Simple idea, clear interface.', 'Turn a simple stacking-game idea into an interface that feels playful and easy to understand, while still supporting building choices, resources, upgrades and progression.'))
    out.append(sec('02', 'Goal', 'The world stays the hero.', 'Create a cohesive experience where the fantasy world remains the focus, while controls, stats and actions stay clear enough for quick mobile interaction.'))
    out.append(sec('03', 'Core flow', 'Four repeatable actions.', 'The main flow is organised around four actions: view the tower, choose a structure, review its attributes, and build or upgrade it.',
        steps([('Home', 'View the tower.'), ('Build', 'Choose a house.'), ('Preview', 'Check its stats.'), ('Build', 'Place it and grow.')]), 'top'))
    out.append(sec('04', 'Visual direction', 'Wood, forest and warmth.', 'The interface borrows its look from the game world: wooden controls, deep teal forest backgrounds, warm orange roofs, cream information cards and simple icons. This helps interface elements feel part of the environment, not layered on top of it.',
        sw([('Forest Teal', '#173F3D'), ('Warm Wood', '#A94F22'), ('Cream', '#F4EFE4'), ('Moss', '#72865B')]), 'top'))
    out.append(sec('05', 'Final UI', 'One system across the game.', 'The same buttons, resource counters and cards run through every screen, so navigation and information stay consistent.',
        '<div class="gal n4 phone-ph">' + ph('Title screen with Play button', '0.5') + ph('Build menu: house cards with costs', '0.5') + ph('Tower view with resource counters', '0.5') + ph('Preview card with stats and Build button', '0.5') + '</div>', 'top'))
    out.append(sec('06', 'Outcome', 'A clearer game concept.', 'The final direction turns Tree Tower into a more complete mobile-game concept, connecting the playful visual world with a clear interface for building, upgrading and tracking progress. Designing the system across several screens made it easier to keep navigation, buttons, resources and information consistent.'))
    out.append('<section class="sx text"><div class="sx-in"><div class="sx-t"><p class="lab">More</p><p><a class="text-link" href="index.html#work">Back to selected work <span aria-hidden="true">→</span></a></p></div></div></section>')
    return out

def body_cupid():
    out = []
    out.append(cover('#fff', '2.05', ph('Hero: phone mockup showing the home screen with date ideas', '2.05')))
    out.append(sec('01', 'Challenge', 'Planning a date is hard work.', 'Planning a perfect date is stressful and time-consuming. People often struggle to find activities both partners will enjoy. Cupid’s Helper offers a curated selection of date ideas shaped by the user’s preferences, so romantic planning feels simple and enjoyable.'))
    out.append(sec('02', 'Planning journey', 'One date, four steps.', 'In the scenario, Ronan wants a romantic date and opens the app to plan it. He signs in, searches, and gets several ideas from the app’s database: movies, restaurants, concerts and art galleries. He reads the details of each option, picks one, and shares it with Rona so they can coordinate and meet on time.',
        steps([('Sign in', 'Open the app and log in.'), ('Browse', 'Movies, restaurants, concerts and galleries.'), ('Compare', 'Read each option’s details.'), ('Share', 'Send the chosen date to a partner.')]), 'top'))
    out.append(sec('03', 'Key screens', 'Built around browsing.', 'The home screen puts category icons at the top and recommended venues below as image cards. A venue screen shows a large photo, rating and details. The interface is in Hebrew, set right to left.',
        '<div class="gal n3 phone-ph">' + ph('Home: category icons and recommendations', '0.5') + ph('Venue detail screen', '0.5') + ph('Share-with-partner screen', '0.5') + '</div>', 'top'))
    out.append(sec('04', 'Visual identity', 'Soft pinks and purples.', 'The visual design aims for an inviting, romantic look: a palette of soft pinks and purples, with considered typography and icons, to make the stressful job of planning a date feel easy and pleasant.',
        sw([('Blush Pink', '#F9EAF4'), ('Deep Orchid', '#9B4F8B'), ('Violet', '#683D9E'), ('Night', '#1A1A2E')]), 'top'))
    out.append(sec('05', 'Supporting screens', 'Beyond the main flow.', 'A splash screen with the logo, and two dark, social-style screens.',
        '<div class="gal n3 phone-ph">' + ph('Splash screen with logo', '0.5') + ph('Instagram-style promo screens', '0.5', 2) + '</div>', 'top'))
    out.append('<section class="sx text"><div class="sx-in"><div class="sx-t"><p class="lab">More</p><p><a class="text-link" href="index.html#work">Back to selected work <span aria-hidden="true">→</span></a></p></div></div></section>')
    return out

# ---------------------------------------------------------------- home
def home():
    feat = BY['campaign']
    def tile_media(slug):
        if slug == 'campaign':
            return ('<span class="pj-m feat-m" style="--bg:#171719"><span class="trio3">'
                    + img('campaign-04', 'Fine Rituals Tax Free campaign', '(max-width:700px) 40vw, 28vw', True)
                    + img('campaign-16', 'Cleansing mousse campaign', '(max-width:700px) 40vw, 28vw', True)
                    + img('campaign-09', 'Flame Sale social campaign', '(max-width:700px) 40vw, 28vw', True)
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        if slug == 'marketplace':
            return ('<span class="pj-m" style="--bg:#E8E4DE"><span class="mk">'
                    + img('marketplace-09', 'Beauty product listing with benefit icons', '(max-width:700px) 60vw, 24vw')
                    + img('marketplace-02', 'Lip product benefits and features', '(max-width:700px) 60vw, 24vw')
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        if slug == 'hatachana':
            return ('<span class="pj-m" style="--bg:#ECBA40"><span class="ht">'
                    + img('hatachana-01', 'Illustrated urban explorer', '(max-width:700px) 40vw, 14vw')
                    + img('home-05', 'Hatachana mobile tour experience', '(max-width:700px) 40vw, 16vw')
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        return ('<span class="pj-m" style="--bg:#DDDADF"><span class="sb">'
                + img('home-07-cut', 'Give Me Sambusak brand packaging', '(max-width:700px) 90vw, 32vw')
                + '</span><span class="go" aria-hidden="true">↗</span></span>')
    def tile(p, featured=False):
        cls = 'pj feat' if featured else 'pj'
        k = 'real' if p['kind'] == 'real' else 'acad'
        extra = '<span class="pj-star">Featured</span>' if featured else ''
        return (f'<a class="{cls} rv" href="{p["slug"]}.html">{tile_media(p["slug"])}'
                f'<span class="pj-c"><span class="pj-n">{p["n"]}</span><span class="pj-t"><h3>{p["short"]}</h3><p>{p["blurb"]}</p></span>'
                f'<span class="pj-k"><span class="kind {k}">{p["kind_label"]}</span><span class="pj-tags">{p["tag"]}</span><span class="pj-cta">View case study <i aria-hidden="true">→</i></span></span></span></a>')
    h = head('Tzadik Azaria — Digital &amp; Visual Designer', 'Portfolio of Tzadik Azaria, a digital and visual designer creating visual identities, digital campaigns and scalable visual systems across branding, e-commerce and marketing.', 'home', og='og-home', home=True)
    h += header('work')
    h += f'''<main id="main">
<section class="hero2" id="hero" aria-labelledby="hero-title">
<div class="hero2-in wide"><p class="eyebrow"><i aria-hidden="true"></i>Digital &amp; Visual Designer</p>
<h1 id="hero-title"><span>Design with clarity.</span><span class="l2">And a <b class="sel">point of view.<i class="hd tl"></i><i class="hd tr"></i><i class="hd bl"></i><i class="hd br"></i><em class="dim" aria-hidden="true">W 0 × H 0</em></b></span></h1>
<svg class="vec" role="group" aria-label="Interactive curve that reshapes the headline type"><path class="vp" d=""/><path class="vh" d=""/><g class="vpts"></g></svg>
<div class="hero-row"><p class="sub">I create visual identities, digital campaigns and scalable visual systems across branding, e&#8209;commerce and marketing.</p>
<div class="actions"><a class="cta" href="#work">Selected projects <span aria-hidden="true">↓</span></a><a class="ghost" href="about.html">About me <span aria-hidden="true">→</span></a></div></div>
<div class="hero-foot"><span>Tzadik Azaria</span><p class="hint">Drag the middle point of the curve, or focus it and use the arrow keys, to reshape the type.</p><span>Open to full-time roles</span></div></div></section>

<section class="work wrap" id="work" aria-labelledby="work-title"><div class="work-head"><p class="kicker" id="work-title">Selected Projects</p><h2 class="lede rv">Commercial campaign and e-commerce work, alongside two academic concepts. Each one is labelled.</h2><p class="work-key rv"><span class="kind real">Commercial work</span><span class="kind acad">Academic concept</span></p></div>
<div class="pj-grid">
{tile(PROJECTS[0], True)}
{tile(PROJECTS[1])}
{tile(PROJECTS[2])}
{tile(PROJECTS[3])}
</div></section>

<section class="about-strip wrap"><h2 class="rv">From product pages<br><em>to brand identities.</em></h2><p class="rv">I’m a digital and visual designer with in-house and freelance experience. I’ve created e-commerce content, campaign and social visuals, and promotional materials for beauty and wellness brands, and branding, signage and print for freelance clients. I care about typography, layout and consistency, and I like seeing a project through from brief to final delivery.</p><a class="text-link rv" href="about.html">More about me <span aria-hidden="true">→</span></a></section></main>
'''
    h += FOOTER
    open(f'{ROOT}/index.html', 'w').write(h)
    # legacy URL: keep old home.html working
    open(f'{ROOT}/home.html', 'w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="index.html"><title>Tzadik Azaria</title></head><body><a href="index.html">Continue to the portfolio</a></body></html>')

# ---------------------------------------------------------------- about
def about():
    h = head('About — Tzadik Azaria', 'Tzadik Azaria is a digital and visual designer with in-house and freelance experience in e-commerce content, digital campaigns, social media, web visuals and print.', 'inner about', og='og-home')
    h += header('about')
    exp = [
        ('OG Global Import', 'Designed digital and print assets for international beauty and wellness brands across e-commerce, social media, campaigns and retail. Created product visuals, banners, newsletters, marketplace content and promotional materials, working with marketing, sales, operations and external suppliers.'),
        ('Freelance', 'Designed branding, brochures, signage, presentations and digital marketing materials for clients across different industries. Developed visual solutions around each client’s needs and managed projects from the initial brief through feedback, revisions and final delivery.'),
        ('ORT Hermelin College', 'Designed posters, educational publications and marketing materials for college initiatives. Created digital and print assets and assisted students with design principles and creative software.'),
    ]
    xp = ''.join(f'<article class="xp"><span class="xn">0{i+1}</span><h2>{o}</h2><p>{d}</p></article>' for i, (o, d) in enumerate(exp))
    h += f'''<main id="main"><div class="about-page wrap">
<section class="about-hero"><div><p class="eyebrow">About Tzadik</p><h1>Thoughtful design.<br><em>From idea<br>to execution.</em></h1></div><p class="about-intro">I’m Tzadik Azaria, a digital and visual designer with in-house and freelance experience. I create e-commerce content, digital campaigns, social media assets, web visuals and print materials, with an eye for typography, layout and brand consistency.</p></section>
<section class="about-story"><p class="eyebrow">Background</p><div><p>I’ve worked in-house on e-commerce and campaign content for beauty and wellness brands, and as a freelancer on branding, signage, brochures and presentations for clients in different industries. I’m used to taking a project from the brief and concept through to final production, and I enjoy adapting one visual idea to different channels and markets while keeping it consistent.</p><p>I studied media design at ORT Hermelin College, and I’m looking for a full-time role in a design studio, agency or in-house creative team.</p><div class="about-actions"><a class="text-link" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV <span aria-hidden="true">↓</span></a><a class="text-link ghost-l" href="mailto:tzadikazaria@gmail.com">Get in touch <span aria-hidden="true">→</span></a></div></div></section>
<section class="experience-section"><p class="eyebrow">Experience</p><div class="experience-list">{xp}</div></section>
<section class="about-lists"><div><h2>Skills</h2><ul><li>Brand identity</li><li>Campaigns &amp; social visuals</li><li>E-commerce, product visuals &amp; marketplaces</li><li>Shopify &amp; email</li><li>Web design, landing pages &amp; responsive</li><li>Print, packaging &amp; production</li><li>Presentations &amp; video editing</li></ul></div><div><h2>Tools</h2><ul><li>Figma · Wix Studio</li><li>Adobe Photoshop · Illustrator</li><li>Adobe InDesign · Premiere Pro</li><li>Shopify · Blender</li></ul></div><div><h2>Education</h2><p>ORT Hermelin College<br>Practical Engineer Diploma<br>in Media Design</p><p class="education-note">Graduated with Distinction</p><h2 class="lang-h">Languages</h2><p>Hebrew — native<br>English — professional</p></div></section></div></main>
'''
    h += FOOTER
    open(f'{ROOT}/about.html', 'w').write(h)

home(); about()
for i in range(4):
    case_page(i)
draft_page('tree-tower', 'Tree Tower', 'Tree Tower', 'A cozy mobile building game concept where players grow a vertical village by stacking and upgrading tree houses.',
           'Academic concept: UI and visual direction for Tree Tower, a mobile tree-house building game.',
           [('Project', 'Academic concept'), ('Platform', 'Figma'), ('Scope', 'App design'), ('Year', '2023')], body_tree())
draft_page('cupids-helper', 'Cupid’s Helper', 'Cupid’s Helper', 'An app concept for planning a date: curated venue ideas, sharing the plan with a partner, and a soft romantic look.',
           'Academic concept: a date-planning app with curated ideas, partner coordination and a romantic visual identity.',
           [('Project', 'Academic concept'), ('Platform', 'Figma'), ('Scope', 'App design'), ('Year', '2023')], body_cupid())
print('built')
