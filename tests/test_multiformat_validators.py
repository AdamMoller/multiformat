import pytest
from context import Document


class TestValidators:
    def new_document(self):
        return Document("A4", "portrait")

    @pytest.mark.parametrize("x", [
        ("100"),
        (200),
    ])
    def test_validate_x_var(self, x):
        document = self.new_document()
        assert document._validate_x_var(x) == int(x)

    @pytest.mark.parametrize("y", [
        ("100"),
        (200),
    ])
    def test_validate_y_var(self, y):
        document = self.new_document()
        assert document._validate_y_var(y) == int(y)

    @pytest.mark.parametrize("x,w", [
        ("100", "400"),
        (200, 400),
    ])
    def test_validate_w_var(self, x, w):
        document = self.new_document()
        assert document._validate_w_var(x, w) == int(w)

    @pytest.mark.parametrize("y,h", [
        ("100", "400"),
        (200, 400),
    ])
    def test_validate_h_var(self, y, h):
        document = self.new_document()
        assert document._validate_h_var(y, h) == int(h)

    @pytest.mark.parametrize("param, return_value", [
        ("left", "left"),
        ("right", "right"),
        ("middle", "middle"),
        ("Left", "left"),
        ("Right", "right"),
        ("Middle", "middle"),
        ("LEFT", "left"),
        ("RIGHT", "right"),
        ("MIDDLE", "middle"),
    ])
    def test_validate_alignment(self, param, return_value):
        document = self.new_document()
        assert document._validate_alignment(param) == return_value

    @pytest.mark.parametrize("font,return_font", [
        ("OpenSans-Regular", "OpenSans-Regular"),
        ("OpenSans-Bold", "OpenSans-Bold"),
        ("opensans-regular", "OpenSans-Regular"),
        ("opensans-bold", "OpenSans-Bold"),
        ("OPENSANS-REGULAR", "OpenSans-Regular"),
        ("OPENSANS-BOLD", "OpenSans-Bold"),
    ])
    def test_validate_font(self, font, return_font):
        document = self.new_document()
        assert document._validate_font(font) == return_font

    @pytest.mark.parametrize("font", [
        ("Unknown-Font"),
        (-1),
        (None),
    ])
    def test_validate_font_error(self, font):
        document = self.new_document()
        with pytest.raises(RuntimeError):
            document._validate_font(font)

    @pytest.mark.parametrize("size", [
        ("10"),
        (20),
    ])
    def test_validate_size(self, size):
        document = self.new_document()
        assert document._validate_size(size) == int(size)

    @pytest.mark.parametrize("string", [("test string"), ])
    def test_validate_string(self, string):
        document = self.new_document()
        assert document._validate_string(string) == string

    @pytest.mark.parametrize("color,output", [
        ((10, 10, 10), (10, 10, 10)),
        (("100", "100", "100"), (100, 100, 100)),
        ("000", (0, 0, 0)),
        ("#000", (0, 0, 0)),
        ("000000", (0, 0, 0)),
        ("#000000", (0, 0, 0)),
        ("FFF", (255, 255, 255)),
        ("#FFF", (255, 255, 255)),
        ("FFFFFF", (255, 255, 255)),
        ("#FFFFFF", (255, 255, 255)),
        ("87CEFA", (135, 206, 250)),
        ("8B4513", (139, 69, 19)),
        ("708090", (112, 128, 144)),
    ])
    def test_validate_color(self, color, output):
        document = self.new_document()
        assert document._validate_color(color) == output

    @pytest.mark.parametrize("color,error", [
        (("a", 10, 10), RuntimeError),
        (("100", "b", "100"), RuntimeError),
        (("100", None, "100"), RuntimeError),
        (("100", "100", -1), RuntimeError),
        (("100", "300", "-1"), RuntimeError),
        ("F", ValueError),
        ("#F", ValueError),
        ("FF", ValueError),
        ("#FF", ValueError),
        ("FFFF", ValueError),
        ("#FFFF", ValueError),
        ("FFFFF", ValueError),
        ("#FFFFF", ValueError),
        ("FFFFFFF", ValueError),
        ("#FFFFFFF", ValueError),
    ])
    def test_validate_color_error(self, color, error):
        document = self.new_document()
        with pytest.raises(error):
            document._validate_color(color)
