import markdown
import re
import os

def add_styling(html_content):
    """Add MathJax support with $ for inline and $$ for display math."""
    
    css_head = """
    <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
<style>
    body {
        margin: 0;
        padding: 20px;
        min-height: 100vh;
        line-height: 1.6;
        font-family: Consolas, "Liberation Mono", Monaco, "Courier New", monospace;
        background-color: #1a1412;
        color: #f4eee8;
        display: flex;
        justify-content: center;
    }

    .container {
        max-width: 800px;
        width: 100%;
        padding: 40px;
        background-color: #231815;
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }

    a {
        color: #e6d5a7;
        text-decoration: none;
    }

    a:hover {
        color: #f0e3c0;
        text-decoration: underline;
    }

    h1 {
        margin: 0.2em 0 0.1em 0;
    }

    h2, h3, h4, h5, h6 {
        color: #f0e3c0;
        margin: 0.1em 0 0.03em 0;  /* Very compact spacing */
        font-family: Consolas, monospace;
        letter-spacing: 0.5px;
    }

    ul {
        padding-left: 20px;
        margin-top: 0.5em;    /* Added to reduce space after headings when followed by lists */
        margin-bottom: 0.5em;
    }

    li {
        margin-bottom: 0.5em;
    }

    pre, code {
        font-family: Consolas, monospace;
        background-color: #2a1f1c;
        padding: 2px 5px;
        border-radius: 3px;
    }
</style>
     """
    
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

    html_content = f'<head>{css_head}{mathjax_head}</head>\n<div class="container">{html_content}</div>'
    
    #print(html_content)  # Print the final HTML content for debugging
    
    return html_content

def remove_unwanted_hashes(text):
    # Remove any #sometagname at the start of the string
    text = re.sub(r'^(#\S+ )+', '', text)
    # Remove only the # if it appears elsewhere in the string
    text = re.sub(r'#(\S+)', r'\1', text)
    return text


def md_to_html(path, output_path=None):
    with open(path, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    # Md processing
    text = remove_unwanted_hashes(text)

    # html processing
    html = markdown.markdown(text)
    html = add_styling(html)
    
    md_file_name = path.split(os.sep)[-1]
    if output_path is not None:
        output = f"{output_path}{os.sep}{md_file_name.split('.')[0]}.html"
        # save html file
        with open(output, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)
        return output

    output = f"{path.split(".")[0]}.html"
    # save html file
    with open(output, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)
    return output
