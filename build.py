#!/usr/bin/env python3
"""Build script: applies CMS content data to HTML pages."""
import os
import re
import shutil
import glob
import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))


def load_content():
    content_path = os.path.join(ROOT, "content", "content.yml")
    with open(content_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def apply_content_to_index(content):
    """Replace text content in index.html using content.yml data."""
    index_path = os.path.join(ROOT, "pages", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Site meta
    site = content["site"]
    html = re.sub(
        r'(<title>).*?(</title>)',
        rf'\g<1>{site["title"]}\g<2>', html)
    html = re.sub(
        r'(<meta name="description" content=").*?(")',
        rf'\g<1>{site["description"]}\2', html)

    # Hero section
    hero = content["hero"]
    # Badge
    html = html.replace(
        '지금 배틀 진행 중!',
        hero["badge"])
    # Title
    html = re.sub(
        r'(<h1 class="hero-title">\s*)살 빼고,(<br><span class="highlight">)돈 벌자!',
        rf'\g<1>{hero["title_line1"]}\g<2>{hero["title_highlight"]}',
        html)
    # Subtitle
    html = re.sub(
        r'(<p class="hero-subtitle">\s*)다이어트에 게임의 재미와 금전 보상을 더했습니다\.(<br>\s*)AI가 당신의 변화를 시뮬레이션하고,(<br>\s*)목표 달성 시 참가비를 나눠 가져요!',
        rf'\g<1>{hero["subtitle_line1"]}\g<2>{hero["subtitle_line2"]}\g<3>{hero["subtitle_line3"]}',
        html)
    # Hero stats
    for i, stat in enumerate(hero.get("stats", [])):
        if i == 0:
            html = re.sub(
                r'(<div class="hero-stat-num">)4주(</div>\s*<div class="hero-stat-label">)배틀 기간',
                rf'\g<1>{stat["number"]}\g<2>{stat["label"]}', html)
        elif i == 1:
            html = re.sub(
                r'(<div class="hero-stat-num">)25만원(</div>\s*<div class="hero-stat-label">)1등 예상 상금',
                rf'\g<1>{stat["number"]}\g<2>{stat["label"]}', html)

    # Floating cards
    for i, card in enumerate(hero.get("floating_cards", [])):
        if i == 0:
            html = html.replace('1등 달성!', card["title"])
            html = html.replace('상금 250,000원 획득', card["description"])
        elif i == 1:
            html = html.replace('-5.2kg 감량', card["title"])
            html = html.replace('4주 배틀 완료', card["description"])

    # Problem section
    prob = content["problem"]
    html = html.replace(
        '>왜 다이어트배틀인가?<',
        f'>{prob["label"]}<')
    html = re.sub(
        r'다이어트, 왜 항상 <span class="highlight">실패</span>할까\?',
        prob["title"].replace("실패", '<span class="highlight">실패</span>'),
        html)

    for i, card in enumerate(prob.get("cards", [])):
        if i == 0:
            html = html.replace('>80%</div>', f'>{card["stat"]}</div>', 1)
            html = html.replace('<h3>높은 실패율</h3>', f'<h3>{card["title"]}</h3>', 1)
        elif i == 1:
            html = html.replace('>20%</div>', f'>{card["stat"]}</div>', 1)
            html = html.replace('<h3>낮은 유지율</h3>', f'<h3>{card["title"]}</h3>', 1)
        elif i == 2:
            html = re.sub(r'>0</div>(\s*<h3>)보상 부재',
                          f'>{card["stat"]}</div>\\1{card["title"]}', html, count=1)

    # Solution section
    sol = content["solution"]
    html = html.replace('>우리의 솔루션<', f'>{sol["label"]}<')

    # How it works
    how = content["how"]
    html = html.replace('>이용방법<', f'>{how["label"]}<')

    # Rewards
    rew = content["rewards"]
    html = html.replace('>보상 시스템<', f'>{rew["label"]}<')

    # Testimonials
    test = content["testimonials"]
    html = html.replace('>베타 테스터 후기<', f'>{test["label"]}<')

    # CTA
    cta = content["cta"]
    html = re.sub(
        r'(<section class="cta" id="download">\s*<div class="container">\s*<h2 class="section-title">)지금 시작하면,(<br>)다음 배틀의 주인공은 당신입니다',
        rf'\g<1>{cta["title_line1"]}\g<2>{cta["title_line2"]}',
        html)
    html = re.sub(
        r'(class="section-desc">)무료 다운로드하고 첫 배틀에 참가해보세요\.(<br>)당신의 변화가 시작됩니다!',
        rf'\g<1>{cta["description_line1"]}\g<2>{cta["description_line2"]}',
        html)

    # Footer copyright
    footer = content["footer"]
    html = re.sub(
        r'(&copy; ).*?(</div>)',
        rf'\g<1>{footer["copyright"]}\g<2>',
        html, count=1)

    return html


def build():
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)

    # 1. Load content and apply to index.html
    content = load_content()
    index_html = apply_content_to_index(content)
    with open(os.path.join(dist, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  - index.html ({len(index_html):,} bytes) [CMS-enabled]")

    # 2. Copy other static HTML pages
    pages_dir = os.path.join(ROOT, "pages")
    if os.path.exists(pages_dir):
        for html_file in glob.glob(os.path.join(pages_dir, "*.html")):
            filename = os.path.basename(html_file)
            if filename != "index.html":  # index is rendered from CMS
                shutil.copy2(html_file, os.path.join(dist, filename))
                print(f"  - {filename} ({os.path.getsize(html_file):,} bytes)")

    # 3. Copy admin directory
    admin_src = os.path.join(ROOT, "admin")
    admin_dst = os.path.join(dist, "admin")
    if os.path.exists(admin_dst):
        shutil.rmtree(admin_dst)
    if os.path.exists(admin_src):
        shutil.copytree(admin_src, admin_dst)
        print("  - admin/ copied")

    # 4. Copy static assets
    static_src = os.path.join(ROOT, "static")
    static_dst = os.path.join(dist, "static")
    if os.path.exists(static_src) and os.listdir(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)

    print(f"\nBuild complete -> {dist}/")


if __name__ == "__main__":
    build()
