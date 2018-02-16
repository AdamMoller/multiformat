import pytest
from multiformat.multiformat import Document


class TestInit:
    @pytest.mark.parametrize("doc_size,doc_layout,match", [
        ("a44", "landscape", "Invalid document size: 'a44'"),
        ("A4", "L", "Invalid document layout: 'L'"),
    ])
    def test_invalid_parameters(self, doc_size, doc_layout, match):
        with pytest.raises(KeyError, match=match):
            document = Document(doc_size, doc_layout)

    @pytest.mark.parametrize("doc_size,doc_layout,w,h", [
        ("a4", "Portrait", 2100, 2970),
        ("A4", "landscape", 2970, 2100),
        ("letter", "portrait", 2159, 2794),
        ("Letter", "Landscape", 2794, 2159),
    ])
    def test_dimensions(self, doc_size, doc_layout, w, h):
        document = Document(doc_size, doc_layout)
        assert document.w == w
        assert document.h == h
