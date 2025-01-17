from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
</head>
<body>
    {% for item in report_content %}
    <h2>{{ item.file }}</h2>
    <pre>{{ item.content }}</pre>
    {% endfor %}
</body>
</html>
"""

def generate_html_report(report_content: list, output_file: str) -> None:
    """Generates an HTML report from the given report content."""
    template = Template(HTML_TEMPLATE)
    html_content = template.render(report_content=report_content)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)
