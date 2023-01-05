import sys
import re

header = """---
title: Converted {{ORIG}}
subtitle: Subtitle {{ORIG}}
layout: default
date: 2023-01-01
keywords: quantum computing, magic, entanglement
published: true
draft: true
---"""

if __name__ == "__main__":
    tex = sys.argv[1]
    md = tex.replace("latex_drafts", "_drafts").replace(".tex", ".md")
    print(f"Converting {tex} to {md}...")

    with open(tex) as input:
        with open(md, "w") as output:
            content = input.read()
            content = header + content
            content = content.replace("ORIG", tex)
            content = re.sub(
                r"\\abstract\{(.*?)\}",
                r"""# Abstract
\1""",
                content,
            )
            content = re.sub(r"\\label\{.*?\}", "", content)
            content = re.sub(
                r"\\section\{(.*?)\}",
                r"# \1",
                content,
            )
            content = re.sub(
                r"\\subsection\{(.*?)\}",
                r"## \1",
                content,
            )
            content = re.sub(
                r"\\textit\{(.*?)\}",
                r"<em>\1</em>",
                content,
            )
            content = re.sub(
                r"\\%",
                r"%",
                content,
            )
            content = re.sub(
                r"\\cite\{(.*?)\}",
                r"{% cite \1 %}",
                content,
            )
            for i in range(10):
                content = re.sub(
                    r"\$(.*?)([^\\])\_(.*?)\$",
                    r"$\1\2\_\3$",
                    content,
                )
            # for i in range(10):
            #     content = re.sub(
            #         r"\$(.*?) (.*?)\$",
            #         r"$\1{}\2$",
            #         content,
            #     )

            content = re.sub(
                r"\\begin\{align.?\}",
                r"""{% katexmm %}
$$""",
                content,
            )
            content = re.sub(
                r"\\end{align.?\}",
                r"""$$
{% endkatexmm %}""",
                content,
            )
            output.write(content)
    print("Done.")
