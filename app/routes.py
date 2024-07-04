from flask import Blueprint, render_template, request, jsonify, send_file
from app.models import Book
from app.utils import generate_book_structure, generate_section, create_markdown_file, create_pdf_file
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate_book():
    topic = request.form.get('topic')
    if len(topic) < 10:
        return jsonify({'error': 'Book topic must be at least 10 characters long'}), 400

    structure_stats, book_structure = generate_book_structure(topic)
    
    try:
        book_structure_json = json.loads(book_structure)
        book = Book(book_structure_json)
        
        return jsonify({
            'structure': book_structure_json,
            'stats': str(structure_stats)
        })
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to decode the book structure. Please try again.'}), 500

@main.route('/generate_section', methods=['POST'])
def generate_section_content():
    title = request.form.get('title')
    description = request.form.get('description')
    content = generate_section(f"{title}: {description}")
    return jsonify({'content': content})

@main.route('/download/<filetype>')
def download_book(filetype):
    book_content = request.args.get('content', '')
    
    if filetype == 'txt':
        file = create_markdown_file(book_content)
        return send_file(file, as_attachment=True, download_name='generated_book.txt', mimetype='text/plain')
    elif filetype == 'pdf':
        file = create_pdf_file(book_content)
        return send_file(file, as_attachment=True, download_name='generated_book.pdf', mimetype='application/pdf')
    else:
        return jsonify({'error': 'Invalid file type'}), 400
