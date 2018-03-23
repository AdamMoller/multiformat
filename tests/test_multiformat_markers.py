import pytest
from context import Document


class TestMarkers:
    def setup_method(self, method):
        self.document = Document("letter", "portrait")

    def test_insert_page_break(self):
        self.document.draw_rectangle(0, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1)
        self.document.insert_page_break()
        assert self.document._document[-1] == {"type": "page_break", }
