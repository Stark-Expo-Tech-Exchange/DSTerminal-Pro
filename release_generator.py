import argparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime


class DSTerminalReleaseGenerator:
    def __init__(self, html_content: str):
        self.html_content = html_content

    def clean_html(self):
        """Remove unwanted style-heavy HTML artifacts"""
        soup = BeautifulSoup(self.html_content, "lxml")

        # Remove all inline styles
        for tag in soup.find_all(True):
            if "style" in tag.attrs:
                del tag.attrs["style"]

        return str(soup)

    def to_markdown(self):
        """Convert cleaned HTML to Markdown"""
        cleaned_html = self.clean_html()

        markdown = md(
            cleaned_html,
            heading_style="ATX",
            bullets="-",
            strip=["span", "div"]
        )

        return self.post_process(markdown)

    def post_process(self, text: str):
        """Fix GitHub-specific formatting issues"""
        lines = text.splitlines()
        fixed = []

        for line in lines:
            # Fix broken table lines like "Command | Description -- | --"
            if "-- | --" in line:
                continue

            # Normalize multiple spaces
            line = " ".join(line.split())

            fixed.append(line)

        return "\n".join(fixed).strip()

    def build_release_template(self, markdown_body: str, version: str):
        """Wrap markdown into GitHub Release format"""

        date = datetime.utcnow().strftime("%Y-%m-%d")

        return f"""# 🚀 DSTerminal Release {version}

**Tag:** `{version}`  
**Release Date:** {date}

---

{markdown_body}

---

### 🔗 Links
- Issue Tracker
- Full Changelog
- Compare Versions

© Stark Expo Tech Exchange
"""

    def generate(self, version: str):
        markdown = self.to_markdown()
        return self.build_release_template(markdown, version)


def main():
    parser = argparse.ArgumentParser(description="DSTerminal Release Generator")
    parser.add_argument("--file", help="Input HTML file", required=True)
    parser.add_argument("--version", help="Release version", required=True)
    parser.add_argument("--output", help="Output markdown file", default="RELEASE.md")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        html_content = f.read()

    generator = DSTerminalReleaseGenerator(html_content)
    release_md = generator.generate(args.version)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(release_md)

    print(f"✅ Release generated: {args.output}")


if __name__ == "__main__":
    main()