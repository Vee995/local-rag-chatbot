import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ingestion.document_loader as doc_loader  # adjust import path if needed


@pytest.fixture
def temp_data_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_load_documents_loads_pdf_and_txt(temp_data_dir):
    # Setup dummy files
    pdf_path = os.path.join(temp_data_dir, "file1.pdf")
    txt_path = os.path.join(temp_data_dir, "file2.txt")
    unsupported_path = os.path.join(temp_data_dir, "file3.xyz")
    for f in [pdf_path, txt_path, unsupported_path]:
        with open(f, "w") as file:
            file.write("dummy content")

    config = {
        "ingestion": {
            "data_dir": temp_data_dir,
            "supported_filetypes": [".pdf", ".txt"],
        }
    }
    config_dir = ""  # data_dir is absolute already

    # Mock loaders to avoid real file processing
    with patch("ingestion.document_loader.PyMuPDFLoader") as mock_pdf_loader, patch(
        "ingestion.document_loader.TextLoader"
    ) as mock_txt_loader:

        mock_pdf_loader.return_value.load.return_value = ["pdf_doc"]
        mock_txt_loader.return_value.load.return_value = ["txt_doc"]

        docs = doc_loader.load_documents(config, config_dir)

        # Check loaders called correctly
        mock_pdf_loader.assert_called_once_with(pdf_path)
        mock_txt_loader.assert_called_once_with(txt_path)

        # Confirm combined docs returned
        assert "pdf_doc" in docs
        assert "txt_doc" in docs


def test_load_documents_skips_unsupported_file(temp_data_dir):
    # Create only unsupported file
    unsupported_path = os.path.join(temp_data_dir, "file.xyz")
    with open(unsupported_path, "w") as f:
        f.write("dummy content")

    config = {
        "ingestion": {
            "data_dir": temp_data_dir,
            "supported_filetypes": [".pdf", ".txt"],
        }
    }
    config_dir = ""

    with patch("ingestion.document_loader.PyMuPDFLoader") as mock_pdf_loader, patch(
        "ingestion.document_loader.TextLoader"
    ) as mock_txt_loader:

        docs = doc_loader.load_documents(config, config_dir)

        # Loaders should NOT be called
        mock_pdf_loader.assert_not_called()
        mock_txt_loader.assert_not_called()

        # docs should be empty
        assert docs == []
