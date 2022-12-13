"""Module for all different routes of the app."""
from flask import render_template, request, redirect, send_file
from init import app, db
from services import Service

service = Service(db)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page for viewing all references."""
    if request.method == 'GET':
        references = service.get_all_references()
        return render_template(
            'check_references.html',
            count=len(references),
            references=references
        )
    else:
        ref_id = int(request.form["id"])
        service.delete_reference(ref_id)
        return redirect('/')

@app.route('/type', methods=['GET', 'POST'])
def choose_reference_type():
    """Page for choosing reference type."""
    if request.method == 'GET':
        return render_template('choose_reference_type.html')
    else:
        ref_type = request.form['type']
        return redirect(f'/edit/{ref_type}')

@app.route('/edit/<ref_type>', methods=['GET', 'POST'])
def send_reference(ref_type: str):
    """New reference page."""
    if request.method == 'GET':
        return render_template('send_reference.html', ref_type=ref_type)
    else:
        ref_type = request.form['ref_type']
        author = request.form['author']
        title = request.form['title']
        year = request.form['year']
        if ref_type == "InCollection":
            service.save_reference(author, title, year)
        if ref_type == "Book":
            booktitle = request.form['booktitle']
            pages = request.form['pages']
            service.save_reference_book(
                author,
                title,
                year,
                booktitle,
                pages
            )
    return redirect('/')

@app.route('/edit_reference/<ref_id>', methods=['GET', 'POST'])
def edit_reference(ref_id: int):
    """Pre-filled form for editing a reference"""
    ref_id = request.form['id']
    ref = service.get_reference_by_id(ref_id)
    return render_template('edit_reference.html', ref_id=ref_id,
                                                    ref_type=ref.type.name,
                                                    author=ref.author,
                                                    title=ref.title,
                                                    year=ref.year,
                                                    booktitle=ref.booktitle,
                                                    pages=ref.pages)

@app.route('/edited', methods=['GET', 'POST'])
def edited_ref_to_database():
    """Updates edited reference to the database"""
    ref_id = request.form['id']
    ref_type = request.form['ref_type']
    author = request.form['author']
    title = request.form['title']
    year = request.form['year']
    if ref_type == "InCollection":
        service.edit_reference(ref_id, author, title, year)
    if ref_type == "Book":
        booktitle = request.form['booktitle']
        pages = request.form['pages']
        service.edit_reference_book(
            ref_id,
            author,
            title,
            year,
            booktitle,
            pages
        )
    return redirect('/')

@app.route('/download', methods=['POST'])
def download_references():
    """Download all references."""
    service.create_bibtex_file()
    return send_file('references.bib', as_attachment=True)

@app.route('/doi2bib', methods=['GET', 'POST'])
def doi2bib():
    """Get reference info from Doi-number"""
    if request.method == 'GET':
        return render_template('doi.html')
    else:
        doi_number = request.form['doinumber']
        reference = service.get_bibtex_from_doi(doi_number)
        print(reference)
        #Do something with reference
        return redirect('/')
