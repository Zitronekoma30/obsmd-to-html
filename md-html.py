import markdown 
from sys import argv
import re

def add_mathjax_support(html_content):
    """Add MathJax support with $ for inline and $$ for display math."""
    
    mathjax_head = """
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [ ['$','$'] ],
                displayMath: [['$$', '$$']],
                processEscapes: true, 
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js"></script>
    """
    
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{mathjax_head}</head>')
    elif '<html>' in html_content:
        html_content = html_content.replace('<html>', f'<html><head>{mathjax_head}</head>')
    else:
        html_content = f'<head>{mathjax_head}</head>\n{html_content}'
    
    print(html_content)  # Print the final HTML content for debugging
    
    return html_content

def remove_unwanted_hashes(text):
    # Remove any #sometagname at the start of the string
    text = re.sub(r'^(#\S+ )+', '', text)
    # Remove only the # if it appears elsewhere in the string
    text = re.sub(r'#(\S+)', r'\1', text)
    return text

md = argv[1]

with open(md, "r", encoding="utf-8") as input_file:
    text = input_file.read()

# Md processing
text = remove_unwanted_hashes(text)


# html processing
html = markdown.markdown(text)
html = add_mathjax_support(html)

# save html file
with open(f"{md.split(".")[0]}.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(html)