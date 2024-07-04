from groq import Groq
from io import BytesIO
from markdown import markdown
from weasyprint import HTML, CSS
from flask import current_app

def generate_book_structure(prompt: str):
    groq_client = Groq(api_key=current_app.config['GROQ_API_KEY'])
    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Write in JSON format:\n\n{\"Title of section goes here\":\"Description of section goes here\",\n\"Title of section goes here\":{\"Title of section goes here\":\"Description of section goes here\",\"Title of section goes here\":\"Description of section goes here\",\"Title of section goes here\":\"Description of section goes here\"}}"},
            {"role": "user", "content": f"Write a comprehensive structure, omitting introduction and conclusion sections (forward, author's note, summary), for a long (>300 page) book on the following subject:\n\n<subject>{prompt}</subject>"}
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    usage = completion.usage
    statistics = GenerationStatistics(input_time=usage.prompt_time, output_time=usage.completion_time, input_tokens=usage.prompt_tokens, output_tokens=usage.completion_tokens, total_time=usage.total_time, model_name="llama3-70b-8192")

    return statistics, completion.choices[0].message.content

def generate_section(prompt: str):
    groq_client = Groq(api_key=current_app.config['GROQ_API_KEY'])
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert writer. Generate a long, comprehensive, structured chapter for the section provided."},
            {"role": "user", "content": f"Generate a long, comprehensive, structured chapter for the following section:\n\n<section_title>{prompt}</section_title>"}
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content

def create_markdown_file(content: str) -> BytesIO:
    markdown_file = BytesIO()
    markdown_file.write(content.encode('utf-8'))
    markdown_file.seek(0)
    return markdown_file

def create_pdf_file(content: str) -> BytesIO:
    html_content = markdown(content, extensions=['extra', 'codehilite'])
    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{ margin: 2cm; }}
            body {{ font-family: Arial, sans-serif; line-height: 1.6; font-size: 12pt; }}
            h1, h2, h3, h4, h5, h6 {{ color: #333366; margin-top: 1em; margin-bottom: 0.5em; }}
            p {{ margin-bottom: 0.5em; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}
            pre {{ background-color: #f4f4f4; padding: 1em; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }}
            blockquote {{ border-left: 4px solid #ccc; padding-left: 1em; margin-left: 0; font-style: italic; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    pdf_buffer = BytesIO()
    HTML(string=styled_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer
