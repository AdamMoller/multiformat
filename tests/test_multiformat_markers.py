import pytest
from multiformat.multiformat import Document


class TestMarkers:
    def new_document(self):
        return Document("letter", "portrait")

    def test_insert_page_break(self):
        document = self.new_document()
        document.draw_rectangle(0, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1)
        document.insert_page_break()
        assert document._document[-1] == {
            "type": "page_break",
        }
