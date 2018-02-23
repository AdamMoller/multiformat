import pytest
from io import BytesIO
from filecmp import cmp
from context import Document


class TestGenerators:
    def new_populated_document(self, size="letter"):
        document = Document(size, "portrait")
        document.draw_rectangle(100, 100, 400, 400, None, (50, 99, 154), 40)
        document.draw_rectangle(700, 100, 200, 400, "#181c1f", None, 0)
        document.draw_circle(160, 800, 150, None, (138, 41, 0), 20)
        document.draw_circle(160, 1200, 150, (172, 108, 19), None, 0)
        document.draw_circle(160, 1600, 150, "#0d754b", (150, 153, 155), 20)
        document.draw_line(document.w / 2, 0, document.w / 2, document.h, 30,
                           (224, 224, 224))
        document.draw_string("Left Align", document.w / 2, 800, "left",
                             "OpenSans-Bold", 100, (0, 0, 0))

        document.draw_string("Center Align", document.w / 2, 1000, "middle",
                             "OpenSans-Bold", 100, (0, 0, 0))

        document.draw_string("Right Align", document.w / 2, 1200, "right",
                             "OpenSans-Bold", 100, (0, 0, 0))
        document.draw_string("Page 1", document.w - 50, document.h - 50,
                             "right", "OpenSans-Regular", 100, "#000")
        document.insert_page_break()
        document.draw_rectangle(100, 100, 400, 400, None, (50, 99, 154), 40)
        document.draw_rectangle(700, 100, 200, 400, (24, 28, 31), None, 0)
        document.draw_line(document.w / 2, 0, document.w / 2, document.h, 30,
                           "#e0e0e0")
        document.draw_string("Left Align", document.w / 2, 800, "left",
                             "OpenSans-Bold", 100, (0, 0, 0))

        document.draw_string("Center Align", document.w / 2, 1000, "middle",
                             "OpenSans-Bold", 100, (0, 0, 0))

        document.draw_string("Right Align", document.w / 2, 1200, "right",
                             "OpenSans-Bold", 100, (0, 0, 0))
        document.draw_string("Page 2", document.w - 50, document.h - 50,
                             "right", "OpenSans-Regular", 100, (0, 0, 0))
        return document

    def test_generate_image_unsupported(self):
        document = self.new_populated_document()
        with pytest.raises(RuntimeError):
            document.generate_image("image_test", "tiff", size=(500, 500))

    @pytest.mark.parametrize("page", [
        ("A"),
        (10),
    ])
    def test_generate_image_invalid_page(self, page):
        document = self.new_populated_document()
        with pytest.raises(RuntimeError):
            document.generate_image(
                "image_test", "png", size=(500, 500), page=page)

    @pytest.mark.parametrize("image_format,size,page", [
        ("PNG", None, None),
        ("JPEG", None, 1),
        ("GIF", None, 1),
        ("PNG", (100, 2000), 1),
        ("JPEG", (2000, 100), 2),
        ("GIF", (2160, 3000), 2),
        ("PNG", (3000, 2999), 2),
    ])
    def test_generate_image_supported(self, image_format, size, page):
        document = self.new_populated_document()
        f = BytesIO()
        document.generate_image(
            "image_test", image_format, size=size, page=page, file_object=f)

    def test_generate_pdf(self):
        document = self.new_populated_document()
        document.author = "Person Name"
        document.title = "The Title"
        document.subject = "The Subject"
        f = BytesIO()
        document.generate_pdf("pdf_test", file_object=f)
        document = self.new_populated_document("a4")
        f = BytesIO()
        document.generate_pdf("pdf_test", file_object=f)

    def test_generated_image_files(self, tmpdir):
        document = self.new_populated_document()
        image_path = tmpdir.join("image_generation_test")
        image_path_1 = tmpdir.join("image_generation_test.png")
        image_path_2 = tmpdir.join("image_generation_test_2.png")
        document.generate_image(image_path, "PNG", size=(1000, 1000))
        assert cmp("tests/image_generation_test_control.png", image_path_1)
        assert cmp("tests/image_generation_test_control_2.png", image_path_2)

    def test_generated_pdf_file(self, tmpdir):
        document = self.new_populated_document()
        pdf_path = tmpdir.join("pdf_generation_test")
        document.generate_pdf(pdf_path)
