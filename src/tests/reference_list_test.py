"""Tests for reference list functionality."""
from os import remove, path
from init import app, db, Reference
from services import Service


class TestReferenceList:
    """Tests for reference list functionality."""
    def setup_method(self):
        """Pytest setup method"""
        self.services = Service(db) # pylint: disable=attribute-defined-outside-init

    def test_db_write_and_read(self):
        """Test adding a reference to the database and reading references."""
        with app.app_context():
            self.services.save_reference("Very Real", "Test Data", "2022")
            assert self.services.get_all_references() == [
                Reference(
                    id=1,
                    author='Very Real',
                    title='Test Data',
                    year=2022,
                    type_id=1
                )
            ]

    def test_db_remove_entry(self):
        """Test removing a reference from the database."""
        with app.app_context():
            assert len(self.services.get_all_references()) == 1
            self.services.delete_reference(1)
            references = self.services.get_all_references()
            assert references == []

    def test_create_file(self):
        """Test bibtex-file is created and is correct"""
        with app.app_context():
            self.services.save_reference("Very Real", "Test Data", "2022")
            self.services.create_bibtex_file()
            assert path.isfile('references.bib')

            with open('references.bib', 'r', encoding='utf-8') as file:
                bibtex_file = file.read().strip()
                should_be = (
                    '@InCollection{1Real2022,author={Very Real},'
                    'title={Test Data},'
                    'booktitle={},year={2022},pages={}}'
                ).strip()

                assert bibtex_file == should_be

    def test_db_edit_reference(self):
        """Test editing reference already in the database"""
        with app.app_context():
            self.services.edit_reference(1, "Edited Data", "This Too", "9001")
            assert self.services.get_all_references() == [
                Reference(
                    id=1,
                    author='Edited Data',
                    title='This Too',
                    year=9001,
                    type_id=1
                )
            ]
    
    def test_db_save_reference_book(self):
        with app.app_context():
            self.services.delete_reference(1)
            self.services.save_reference_book("Au Thor", "Tit Le", "1732", "Book Title", "39")
            assert self.services.get_all_references() == [
                Reference(
                    id=1,
                    author="Au Thor",
                    title="Tit Le",
                    booktitle="Book Title",
                    year=1732,
                    pages=39,
                    type_id=2
                )
            ]
    
    def test_db_edit_reference_book(self):
        with app.app_context():
            self.services.edit_reference_book(1, "Edited Data", "This Too", "3000", "Edited book title", "45")
            assert self.services.get_all_references() == [
                Reference(
                    id=1,
                    author='Edited Data',
                    title='This Too',
                    year=3000,
                    booktitle="Edited book title",
                    pages=45,
                    type_id=2
                )
            ]


def teardown_module():
    """Pytest test suite teardown."""
    remove('src/instance/test.db')
