#!/usr/bin/env python3
"""Build script: renders Jinja2 template with YAML content data."""
import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))


def build():
    # 1. Load content data
    content_path = os.path.join(ROOT, "content", "content.yml")
    with open(content_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    # 2. Set up Jinja2 (autoescape OFF to allow SVG icons)
    env = Environment(
        loader=FileSystemLoader(os.path.join(ROOT, "templates")),
        autoescape=False,
    )
    template = env.get_template("index.html")

    # 3. Render template with content data
    html = template.render(**content)

    # 4. Write output to dist/
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)

    with open(os.path.join(dist, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # 5. Copy admin directory to dist/admin/
    admin_src = os.path.join(ROOT, "admin")
    admin_dst = os.path.join(dist, "admin")
    if os.path.exists(admin_dst):
        shutil.rmtree(admin_dst)
    if os.path.exists(admin_src):
        shutil.copytree(admin_src, admin_dst)

    # 6. Copy static assets if they exist
    static_src = os.path.join(ROOT, "static")
    static_dst = os.path.join(dist, "static")
    if os.path.exists(static_src) and os.listdir(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)

    print(f"Build complete -> {dist}/")
    print(f"  - index.html ({os.path.getsize(os.path.join(dist, 'index.html')):,} bytes)")
    if os.path.exists(admin_dst):
        print(f"  - admin/ copied")


if __name__ == "__main__":
    build()
