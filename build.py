#!/usr/bin/env python3
"""Build script: copies static pages and renders CMS-enabled index."""
import os
import shutil
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))


def build():
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)

    # 1. Copy all static HTML pages from pages/ to dist/
    pages_dir = os.path.join(ROOT, "pages")
    if os.path.exists(pages_dir):
        for html_file in glob.glob(os.path.join(pages_dir, "*.html")):
            filename = os.path.basename(html_file)
            shutil.copy2(html_file, os.path.join(dist, filename))
            print(f"  - {filename} ({os.path.getsize(html_file):,} bytes)")

    # 2. Copy admin directory to dist/admin/
    admin_src = os.path.join(ROOT, "admin")
    admin_dst = os.path.join(dist, "admin")
    if os.path.exists(admin_dst):
        shutil.rmtree(admin_dst)
    if os.path.exists(admin_src):
        shutil.copytree(admin_src, admin_dst)
        print("  - admin/ copied")

    # 3. Copy static assets if they exist
    static_src = os.path.join(ROOT, "static")
    static_dst = os.path.join(dist, "static")
    if os.path.exists(static_src) and os.listdir(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)
        print("  - static/ copied")

    print(f"\nBuild complete -> {dist}/")


if __name__ == "__main__":
    build()
