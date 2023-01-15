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
    md = tex.replace("latex_drafts", "_drafts").replace(".tex", "_gen.md")
    print(f"Converting {tex} to {md}...")

    with open(tex) as input:
        with open(md, "w") as output:
            content = input.read()
            content = header + content
            content = content.replace("ORIG", tex)
            content = re.sub(
                r">",
                r"\\gt",
                content,
            )
            content = re.sub(
                r"&=",
                r"=",
                content,
            )
            content = re.sub(
                r"\\abstract\{(.*?)\}",
                r"""## Abstract
\1""",
                content,
            )
            content = re.sub(r"\\label\{.*?\}", "", content)
            content = re.sub(
                r"\\section\{(.*?)\}",
                r"## \1",
                content,
            )
            content = re.sub(
                r"\\subsection\{(.*?)\}",
                r"### \1",
                content,
            )
            # can't handle embedded curlys just yet
            content = re.sub(
                r"\\textit\{([^\{]*?)\}",
                r"<em>\1</em>",
                content,
            )
            content = re.sub(
                r"\\textbf\{([^\{]*?)\}",
                r"<strong>\1</strong>",
                content,
            )

            content = re.sub(
                r"\\begin\{itemize\}",
                r"<ul>",
                content,
            )
            content = re.sub(
                r"\\begin\{enumerate\}",
                r"<ol>",
                content,
            )
            content = re.sub(
                r"\\item (.*)",
                r"<li>\1</li>",
                content,
            )

            content = re.sub(
                r"\\end\{itemize\}",
                r"</ul>",
                content,
            )
            content = re.sub(
                r"\\end\{enumerate\}",
                r"</ol>",
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

            content = re.sub(
                r"\\ketbra\{(.*?)\}",
                r"\\ket{\1}\\bra{\1}",
                content,
            )
            content = re.sub(
                r"\\braket\{(.*?)\}",
                r"\\bra{\1}\\ket{\1}",
                content,
            )

            content = re.sub(
                r"\\Tr",
                r"\\text{Tr}",
                content,
            )

            content = re.sub(
                r"\|",
                r"\\lvert ",
                content,
            )
            content = re.sub(
                r"\\begin\{figure\}.*",
                r"",
                content,
            )
            content = re.sub(
                r"\\end\{figure\}.*",
                r"",
                content,
            )
            content = re.sub(
                r"\\center",
                r"",
                content,
            )
            content = re.sub(
                r"\\caption\{(.*)\}",
                r"<center><small>\1</small></center>",
                content,
            )

            content = re.sub(
                r"\\includegraphics(\[.*\])*\{(.*)\}",
                r"<center><img src='/assets/images/\2' width='100%'/></center>",
                content,
            )

            content = re.sub(
                r"([^\\])\\([\}|\{])",
                r"\1\\\\\2",
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
                r"\\begin\{definition\}",
                r"""<strong>Definition</strong>""",
                content,
            )
            content = re.sub(
                r"\\end\{definition\}",
                r"""""",
                content,
            )
            content = re.sub(
                r"\\end{align.?\}",
                r"""$$
{% endkatexmm %}""",
                content,
            )

            # try again, maybe there's less embedded curlys
            content = re.sub(
                r"\\textit\{([^\{]*?)\}",
                r"<em>\1</em>",
                content,
            )
            content = re.sub(
                r"\\textbf\{([^\{]*?)\}",
                r"<strong>\1</strong>",
                content,
            )

            output.write(content)
    print("Done.")
