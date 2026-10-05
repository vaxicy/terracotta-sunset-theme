"""Render English layout references using headless Chromium, for final project assets."""
from pathlib import Path
import json
import base64
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'store-assets'/'references'
OUT.mkdir(parents=True,exist_ok=True)
C=json.loads((ROOT/'manifest.json').read_text('utf-8-sig'))['theme']['colors']
LOGO_HEX='#FFA759'  # Calibrated against user installed Chrome screenshot
def color(k): return '#%02X%02X%02X'%tuple(C[k])
css=f''':root{{--milk:{color('ntp_background')};--oat:{color('toolbar')};--sand:{color('frame')};--ink:{color('ntp_text')};--taupe:{color('frame_inactive')};}}'''+'''
*{box-sizing:border-box}body{margin:0;color:var(--ink);font-family:Arial,sans-serif;background:var(--milk)}
.browser{width:1280px;height:800px;background:var(--milk);position:relative;overflow:hidden}
.tabs{height:44px;background:var(--sand);display:flex;align-items:end;padding:6px 12px;gap:10px;padding-bottom:0}
.tab{height:37px;width:235px;padding:12px 18px;font-size:13px;border-radius:12px 12px 0 0}.active{background:var(--oat)}.close{float:right}
.tools{height:56px;background:var(--oat);display:flex;align-items:center;padding:0 20px;gap:24px;font-size:20px}.omni{height:36px;border-radius:22px;background:var(--milk);flex:1;font-size:13px;padding:11px 18px}.bookmarks{height:32px;background:var(--oat);font-size:12px;display:flex;gap:30px;padding:6px 22px}
.content{text-align:center;padding-top:118px}.google{font-size:80px;letter-spacing:-4px;color:var(--sand);margin-bottom:26px}.search{width:560px;height:54px;border-radius:30px;background:white;margin:auto;border:1px solid var(--taupe);text-align:left;padding:18px 24px;font-size:14px}.shortcuts{display:flex;justify-content:center;gap:44px;margin-top:35px}.shortcut{font-size:12px;width:66px}.circle{border-radius:50%;width:48px;height:48px;background:var(--oat);font-size:20px;padding-top:12px;margin:0 auto 12px}.label{position:absolute;bottom:22px;left:24px;font-size:12px}.brand{position:absolute;bottom:22px;right:24px;font-size:13px}
.promo{position:relative;overflow:hidden;background:var(--oat)}.promo h1{font-family:Georgia,serif;margin:0;font-weight:normal}.promo .swatches{display:flex;gap:16px}.swatch{width:46px;height:46px;border-radius:50%;border:1px solid var(--taupe)}
.large{width:1400px;height:560px}.large .copy{position:absolute;left:64px;top:62px}.large h1{font-size:60px;margin:44px 0 8px}.large p{font-size:20px;margin:34px 0}.large .right{position:absolute;left:765px;top:0;width:635px;height:560px;background:var(--sand)}.large .mini{position:absolute;left:725px;top:110px;transform:scale(.49);transform-origin:top left;border-radius:18px;overflow:hidden}.small{width:440px;height:280px}.small .copy{padding:35px 29px}.small h1{font-size:35px}.small p{font-size:16px;margin:16px 0 35px}.small .swatch{width:35px;height:35px}.kicker{font-size:12px;letter-spacing:2px}
'''

css += f'''
:root{{--evergreen:{'#FBE6D5'};}}
.tabs{{color:{color('tab_background_text')};}}
.tab.active{{color:var(--ink);}}
.omni{{background:{color('omnibox_background')};}}
.google{{color:{LOGO_HEX};}}
.circle{{background:{color('frame_inactive')};}}
.large .copy{{width:650px;}}
'''

def browser(bookmarks=False):
    bm='<div class="bookmarks"><span>▱ Bookmarks</span><span>▱ Reading</span><span>▱ Design</span><span>▱ Inspiration</span></div>' if bookmarks else ''
    shortcuts=('<div class="shortcuts">'
        '<div class="shortcut"><div class="circle"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z" fill="#FF0033"/></svg></div>Videos</div>'
        '<div class="shortcut"><div class="circle"><svg width="19" height="19" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="#DA6556" stroke-width="2"/><path d="M4 12h16M12 4c2.6 3.4 2.6 12.6 0 16M12 4c-2.6 3.4-2.6 12.6 0 16" fill="none" stroke="#DA6556" stroke-width="2"/></svg></div>Web</div>'
        '<div class="shortcut add"><div class="circle"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14" stroke="#5F6C7B" stroke-width="2.4" stroke-linecap="round"/></svg></div>Add shortcut</div>'
        '</div>')
    customize='<div class="customize"><svg width="13" height="13" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l4-1 10-10-3-3L5 16z" fill="none" stroke="#FFF5EC" stroke-width="2"/></svg>Customize Chrome</div>'
    return '<div class="browser"><div class="tabs"><div class="tab active">New Tab <span class="close">×</span></div><div class="tab">Reading list <span class="close">×</span></div><span style="padding:10px">+</span><span style="margin-left:auto;padding:10px 12px;letter-spacing:22px;color:#FFFCF8">− □ ×</span></div><div class="tools"><span>←</span><span>→</span><span>↻</span><div class="omni">Search or type a URL</div><span>☆</span><span>⋮</span></div>'+bm+'<div class="content"><div class="google">Google</div><div class="search">Search Google or type a URL</div>'+'</div>'+customize+'</div>'

def swatches():return '<div class="swatches">'+''.join(f'<div class="swatch" style="background:var(--{c})"></div>' for c in ('sand','milk','taupe','evergreen'))+'</div>'
def page(body):
    body=body.replace('<div class="search">Search Google or type a URL</div>', '<div class="search"><span class="plus">+</span><span class="prompt">Ask Google</span><span class="search-actions"><svg width="16" height="20" viewBox="0 0 24 28"><rect x="9" y="2" width="6" height="14" rx="3" fill="#202124"/><path d="M5 12v2a7 7 0 0 0 14 0v-2M12 21v5" fill="none" stroke="#202124" stroke-width="3"/></svg><svg width="18" height="18" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="4" fill="none" stroke="#202124" stroke-width="2.5"/><circle cx="12" cy="12" r="3" fill="#202124"/></svg></span><span class="ai-mode">✧ AI Mode</span></div><div class="ai-cards"><div><b>✧ &nbsp; Try AI Mode</b><span>Create, summarize, plan</span></div><div><b>✦ &nbsp; Create images</b><span>Imagine, edit, draw</span></div></div>')
    return '<!doctype html><html lang="en"><meta charset="utf-8"><style>'+css+'</style><body>'+body+'</body></html>'
logo='data:image/png;base64,'+base64.b64encode((ROOT/'logo/logo128.png').read_bytes()).decode()
css += """
.content{padding-top:96px}
.google{font-size:80px;line-height:1.18;margin-bottom:44px;font-weight:500}
.search{width:630px;height:48px;padding:0 20px;display:flex;align-items:center;gap:16px;border:0;border-radius:28px;box-shadow:0 1px 7px #00000029;color:#62676D;font-size:16px}
.bookmarks{border-bottom:1px solid #D6CFBF}
.tea{position:relative;overflow:hidden}
.tea h1{font-family:Georgia,serif;font-weight:normal;margin:0}
.tea.small{width:440px;height:280px;background:var(--sand);text-align:center;color:var(--milk);padding-top:16px}
.tea.small img{width:76px;height:76px;display:block;margin:0 auto 6px}
.tea.small h1{font-size:42px;line-height:1.1}
.tea.small .sub{font-size:15px;letter-spacing:4px;margin-top:8px}
.tea.small p{font-size:13px;margin-top:18px;color:#FFF5EC}
.tea.small:after{content:'';position:absolute;left:0;right:0;bottom:0;height:14px;background:#FBE6D5}
.tea.wide{width:1400px;height:560px;background:#FBE6D5;color:#542F2B}
.tea.wide .copy{position:absolute;left:58px;top:70px;width:440px}
.tea.wide .eyebrow{font-size:12px;letter-spacing:3px;margin-bottom:40px}
.tea.wide h1{font-size:62px;line-height:1.06}
.tea.wide .sub{font-size:22px;margin-top:14px;letter-spacing:2px}
.tea.wide p{font-size:18px;line-height:1.6;margin:28px 0}
.tea.wide .dots{display:flex;gap:16px}
.tea.wide .dot{width:32px;height:32px;border-radius:50%;border:1px solid #B0B79E}
.tea .window{position:absolute;left:550px;top:83px;transform:scale(.62);transform-origin:top left;border:2px solid #DA6556;border-radius:14px;overflow:hidden;color:var(--ink)}
.tea .window .browser{height:634px}
.tea .window .content{padding-top:80px}
"""
css += """
.tabs{height:37px}
.tab{height:32px;padding:9px 18px}
.tools{height:42px;gap:20px;padding:0 16px}
.omni{height:34px;padding:8px 16px;border:2px solid #677894}
.bookmarks{height:34px;padding:9px 20px;border-bottom-color:#BCB0A6}
.content{padding-top:109px}
.google{margin-bottom:20px}
.search{height:42px}
.tea .window .content{padding-top:85px}
"""

css += """
.poster{width:1400px;height:560px;background:#FFFAF6;position:relative;overflow:hidden;text-align:center;border-top:8px solid #DA6556}
.poster h1{font:48px Georgia,serif;margin:23px 0 7px}
.poster p{font-size:17px;margin:0}
.poster .preview{position:absolute;left:284px;top:145px;transform:scale(.65);transform-origin:top left;border:2px solid #DA6556;border-radius:16px;overflow:hidden;text-align:left}
.poster .browser{height:610px}.poster .content{padding-top:55px}
.shortcuts{display:flex;justify-content:center;gap:40px;margin-top:34px}
.shortcut{width:86px;font-size:12px;text-align:center}
.shortcut .circle{width:48px;height:48px;border-radius:50%;margin:0 auto 10px;padding:0;display:flex;align-items:center;justify-content:center;line-height:0;background:#FFFFFF;box-shadow:0 1px 4px #00000012}
.shortcut.add .circle{background:#E7E7DC;box-shadow:none}
.customize{position:absolute;right:22px;bottom:16px;background:#202124;color:#FFF5EC;font-size:12px;border-radius:16px;padding:8px 14px;display:flex;align-items:center;gap:6px}
.tea.small h1{font-size:36px}.tea.small p{color:var(--milk)}
.intro{width:1280px;height:800px;padding:65px 72px;background:#F4F3F1}
.intro h1{font:54px Georgia,serif;margin:20px 0}.intro p{font-size:21px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:35px}
.card{height:190px;border-radius:18px;padding:30px;display:flex;flex-direction:column;justify-content:end}.card strong{font-size:28px}.card span{font-size:17px;margin-top:12px}
"""
css += """
.google{color:#FFA759;font-size:80px;margin-bottom:40px}
.search{height:48px;gap:14px;color:#202124}
.plus{font-size:28px;line-height:1}.prompt{color:#B0B0B0}.search-actions{margin-left:auto;display:flex;align-items:center;gap:18px}
.ai-mode{background:#F3F5F6;border-radius:24px;padding:9px 12px;font-size:13px}
.ai-cards{display:flex;justify-content:center;gap:12px;margin-top:14px;text-align:left}
.ai-cards>div{background:#3C4043;color:#FFFAF6;border-radius:15px;padding:12px 18px;width:202px}
.ai-cards b{font-size:13px;font-weight:normal;display:block}.ai-cards span{display:block;font-size:11px;margin:4px 0 0 25px}
.bookmarks{border-bottom-color:#D8BCA5}
"""
css += """
.sunpromo{position:relative;overflow:hidden;background:#F4F3F1;color:#542F2B}
.sunpromo:before{content:'';position:absolute;width:480px;height:480px;border-radius:50%;background:#FDB773;right:-110px;bottom:-210px}
.sunpromo .copy{position:relative;z-index:2}.sunpromo h1{font-family:Georgia,serif;font-weight:normal}
.sunpromo.small{width:440px;height:280px;padding:0;background:#FFF5EC;text-align:center}.sunpromo.small:before{display:none}.sunpromo.small{display:flex;align-items:center;justify-content:center}.sunpromo.small .copy{transform:translateY(-14px)}.sunpromo.small img{width:72px;height:72px;display:block;margin:0 auto 12px}.sunpromo.small h1{font-size:31px;margin:8px 0 12px}.sunpromo.small p{font-size:13px;margin:0 0 24px}
.sunpromo.wide{width:1400px;height:560px}.sunpromo.wide .copy{position:absolute;left:65px;top:85px;width:400px}.sunpromo.wide h1{font-size:60px;line-height:1.08;margin:25px 0}.sunpromo.wide p{font-size:20px;line-height:1.6}
.sunpromo.wide:before{width:820px;height:820px;right:-100px;bottom:-370px}
.sunpromo .preview{position:absolute;left:550px;top:80px;transform:scale(.60);transform-origin:top left;border-radius:16px;overflow:hidden;border:1px solid #A14646;box-shadow:0 12px 40px #542F2B25}
.sunpromo .browser{height:660px}.sunpromo .content{padding-top:80px}
"""
small='<div class="sunpromo small"><div class="copy"><img src="'+logo+'"><h1>Terracotta Sunset</h1><p>A little sunset, every day.</p><div class="kicker">CHROME THEME</div></div></div>'
wide='<div class="sunpromo wide"><div class="copy"><div class="kicker">CHROME THEME</div><h1>Terracotta<br>Sunset</h1><p>Warm tones.<br>A calmer everyday browser.</p></div><div class="preview">'+browser(True)+'</div></div>'
colors=[('Terracotta Red','#A14646','Window frame','#FFF5EC'),('Sunset Coral','#DA6556','Links & accents','#542F2B'),('Warm Orange','#EB895B','Palette accent','#542F2B'),('Soft Apricot','#FDB773','Palette accent','#542F2B')]
cards=''.join(f'<div class="card" style="background:{k};color:{fg};border:1px solid #CED8D7"><strong>{name}</strong><span>{k} · {role}</span></div>' for name,k,role,fg in colors)
intro='<div class="intro"><div class="kicker">WARM DAYS AHEAD</div><h1>Terracotta Sunset Theme</h1><p>Four warm tones. One peaceful space.</p><div class="cards">'+cards+'</div><p style="font-size:16px;margin-top:30px">Solid colors · Minimal design · No wallpaper · No permissions required</p></div>'
jobs=[('screenshot-1-browser',1280,800,browser(True)),('screenshot-2-introduction',1280,800,intro),('promo-440x280',440,280,small),('promo-1400x560',1400,560,wide)]
with sync_playwright() as p:
    browser_engine=p.chromium.launch(headless=True)
    tab=browser_engine.new_page(device_scale_factor=1)
    for name,w,h,body in jobs:
        html=page(body);(OUT/f'{name}.html').write_text(html,'utf-8')
        tab.set_viewport_size({'width':w,'height':h});tab.set_content(html);tab.screenshot(path=str(OUT/f'{name}.png'))
        destination=ROOT/'store-assets'/('promo' if name.startswith('promo-') else 'screenshots/en')/(name.removeprefix('promo-')+'.png')
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=destination.with_suffix('.new.png')
        with Image.open(OUT/f'{name}.png') as img: img.convert('RGB').save(temp)
        temp.replace(destination)
        print(f'Rendered {name} {w}x{h}')
    browser_engine.close()


