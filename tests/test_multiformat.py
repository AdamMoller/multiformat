import pytest

from multiformat.multiformat import Document


def test_dimensions():
    with pytest.raises(KeyError):
        document = Document("a44", "landscape")


def test_dimensions():
    with pytest.raises(KeyError):
        document = Document("letter", "L")


@pytest.mark.parametrize("doc_size,doc_layout,w,h", [
    ("a4", "Portrait", 2100, 2970),
    ("A4", "landscape", 2970, 2100),
    ("letter", "portrait", 2159, 2794),
    ("Letter", "Landscape", 2794, 2159),
])
def test_dimensions(doc_size, doc_layout, w, h):
    document = Document(doc_size, doc_layout)
    assert document.w == w
    assert document.h == h


def test_draw_string_success():
    document = Document("letter", "portrait")
    document.draw_string("Test", 0, 100, "left", "OpenSans-Regular", 12,
                         (0, 0, 0))
    assert document._document[-1] == {
        "type": "string",
        "string": "Test",
        "x": 0,
        "y": 100,
        "alignment": "left",
        "font": "OpenSans-Regular",
        "size": 12,
        "color": (0, 0, 0)
    }


@pytest.mark.parametrize(
    "string, x, y, alignment, font, size, color",
    [
        # string
        # x
        ("Test", -1, 0, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 10000, 0, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", "a", 0, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", None, 0, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", "", 0, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        # y
        ("Test", 0, -1, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, 10000, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, "a", "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, None, "left", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, "", "left", "OpenSans-Regular", 12, (0, 0, 0)),
        # alignment
        ("Test", 0, 0, "top", "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, 0, -1, "OpenSans-Regular", 12, (0, 0, 0)),
        ("Test", 0, 0, None, "OpenSans-Regular", 12, (0, 0, 0)),
        # font
        ("Test", 0, 0, "left", "Verdana", 12, (0, 0, 0)),
        ("Test", 0, 0, "left", -1, 12, (0, 0, 0)),
        ("Test", 0, 0, "left", None, 12, (0, 0, 0)),
        # size
        ("Test", 0, 0, "left", "OpenSans-Regular", "a", (0, 0, 0)),
        ("Test", 0, 0, "left", "OpenSans-Regular", -1, (0, 0, 0)),
        # color
        ("Test", 0, 0, "left", "OpenSans-Regular", 12, ("r", "g", "b")),
        ("Test", 0, 0, "left", "OpenSans-Regular", 12, (-1, -1, -1)),
        ("Test", 0, 0, "left", "OpenSans-Regular", 12, (256, 256, 256)),
    ])
def test_draw_string_error(string, x, y, alignment, font, size, color):
    document = Document("a4", "portrait")
    with pytest.raises(RuntimeError):
        document.draw_string(string, x, y, alignment, font, size, color)


def test_draw_rectangle_success():
    document = Document("letter", "portrait")
    document.draw_rectangle(0, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1)
    assert document._document[-1] == {
        "type": "rectangle",
        "x": 0,
        "y": 0,
        "w": 200,
        "h": 200,
        "fill_color": (0, 0, 0),
        "border_color": (0, 0, 0),
        "border_width": 1
    }


@pytest.mark.parametrize(
    "x,y,w,h,fill_color,border_color,border_width",
    [
        # x
        (-1, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (5000, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        ("a", 0, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (None, 0, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        ("", 0, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        # y
        (0, -1, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, 5000, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, "a", 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, None, 200, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, "", 200, 200, (0, 0, 0), (0, 0, 0), 1),
        # w
        (0, 0, -1, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, 5000, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, "a", 200, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, None, 200, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, "", 200, (0, 0, 0), (0, 0, 0), 1),
        # h
        (0, 0, 200, -1, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, 200, 5000, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, 200, "a", (0, 0, 0), (0, 0, 0), 1),
        (0, 0, 200, None, (0, 0, 0), (0, 0, 0), 1),
        (0, 0, 200, "", (0, 0, 0), (0, 0, 0), 1),
        # fill_color
        (0, 0, 200, 200, (-1, -1, -1), (0, 0, 0), 1),
        (0, 0, 200, 200, (256, 256, 256), (0, 0, 0), 1),
        (0, 0, 200, 200, ("a", "b", "c"), (0, 0, 0), 1),
        # border_color
        (0, 0, 200, 200, (0, 0, 0), (-1, -1, -1), 1),
        (0, 0, 200, 200, (0, 0, 0), (256, 256, 256), 1),
        (0, 0, 200, 200, (0, 0, 0), ("a", "b", "c"), 1),
        # border_width
        (0, 0, 200, 200, (0, 0, 0), (0, 0, 0), -1),
        (0, 0, 200, 200, (0, 0, 0), (0, 0, 0), "a"),
    ])
def test_draw_rectangle_error(x, y, w, h, fill_color, border_color,
                              border_width):
    document = Document("a4", "portrait")
    with pytest.raises(RuntimeError):
        document.draw_rectangle(x, y, w, h, fill_color, border_color,
                                border_width)


def test_draw_line_success():
    document = Document("letter", "portrait")
    document.draw_line(0, 0, 100, 100, 2, (0, 0, 0))
    assert document._document[-1] == {
        "type": "line",
        "x": 0,
        "y": 0,
        "x1": 100,
        "y1": 100,
        "width": 2,
        "color": (0, 0, 0)
    }


@pytest.mark.parametrize(
    "x,y,x1,y1,width,color",
    [
        # x
        (-1, 0, 100, 100, 2, (0, 0, 0)),
        (10000, 0, 100, 100, 2, (0, 0, 0)),
        ("a", 0, 100, 100, 2, (0, 0, 0)),
        (None, 0, 100, 100, 2, (0, 0, 0)),
        ("", 0, 100, 100, 2, (0, 0, 0)),
        # y
        (0, -1, 100, 100, 2, (0, 0, 0)),
        (0, 10000, 100, 100, 2, (0, 0, 0)),
        (0, "a", 100, 100, 2, (0, 0, 0)),
        (0, None, 100, 100, 2, (0, 0, 0)),
        (0, "", 100, 100, 2, (0, 0, 0)),
        # x1
        (0, 0, -1, 100, 2, (0, 0, 0)),
        (0, 0, 10000, 100, 2, (0, 0, 0)),
        (0, 0, "a", 100, 2, (0, 0, 0)),
        (0, 0, None, 100, 2, (0, 0, 0)),
        (0, 0, "", 100, 2, (0, 0, 0)),
        # y1
        (0, 0, 100, -1, 2, (0, 0, 0)),
        (0, 0, 100, 10000, 2, (0, 0, 0)),
        (0, 0, 100, "a", 2, (0, 0, 0)),
        (0, 0, 100, None, 2, (0, 0, 0)),
        (0, 0, 100, "", 2, (0, 0, 0)),
        # width
        (0, 0, 100, 100, "a", (0, 0, 0)),
        (0, 0, 100, 100, -1, (0, 0, 0)),
        # color
        (0, 0, 100, 100, 2, ("r", "g", "b")),
        (0, 0, 100, 100, 2, (-1, -1, -1)),
        (0, 0, 100, 100, 2, (256, 256, 256)),
    ])
def test_draw_line_error(x, y, x1, y1, width, color):
    document = Document("a4", "portrait")
    with pytest.raises(RuntimeError):
        document.draw_line(x, y, x1, y1, width, color)


def test_generate_unsupported_image():
    document = Document("letter", "portrait")
    with pytest.raises(RuntimeError):
        document.generate_image("test_image", "tiff", size=(500, 500))


@pytest.mark.parametrize("x", [
    ("100"),
    (200),
])
def test_validate_x_var(x):
    document = Document("letter", "portrait")
    assert document._validate_x_var(x) == int(x)


@pytest.mark.parametrize("y", [
    ("100"),
    (200),
])
def test_validate_y_var(y):
    document = Document("letter", "portrait")
    assert document._validate_y_var(y) == int(y)


@pytest.mark.parametrize("x,w", [
    ("100", "400"),
    (200, 400),
])
def test_validate_w_var(x, w):
    document = Document("letter", "portrait")
    assert document._validate_w_var(x, w) == int(w)


@pytest.mark.parametrize("y,h", [
    ("100", "400"),
    (200, 400),
])
def test_validate_h_var(y, h):
    document = Document("letter", "portrait")
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
def test_validate_alignment(param, return_value):
    document = Document("letter", "portrait")
    assert document._validate_alignment(param) == return_value


@pytest.mark.parametrize("font,return_font", [
    ("OpenSans-Regular", "OpenSans-Regular"),
    ("OpenSans-Bold", "OpenSans-Bold"),
    ("opensans-regular", "OpenSans-Regular"),
    ("opensans-bold", "OpenSans-Bold"),
    ("OPENSANS-REGULAR", "OpenSans-Regular"),
    ("OPENSANS-BOLD", "OpenSans-Bold"),
])
def test_validate_font(font, return_font):
    document = Document("letter", "portrait")
    assert document._validate_font(font) == return_font


@pytest.mark.parametrize("size", [
    ("10"),
    (20),
])
def test_validate_size(size):
    document = Document("letter", "portrait")
    assert document._validate_size(size) == int(size)


@pytest.mark.parametrize("string", [
    ("test string"),
])
def test_validate_string(string):
    document = Document("letter", "portrait")
    assert document._validate_string(string) == string


@pytest.mark.parametrize("color", [
    ((10, 10, 10)),
    (("100", "100", "100")),
])
def test_validate_color(color):
    document = Document("letter", "portrait")
    assert document._validate_color(color) == (int(color[0]), int(color[1]),
                                               int(color[2]))


@pytest.mark.parametrize("color", [
    ((10, 10, "a")),
    (("100", "100", "b")),
    (("100", "100", None)),
    (("100", "100", -1)),
    (("100", "100", "-1")),
])
def test_validate_color_error(color):
    document = Document("letter", "portrait")
    with pytest.raises(RuntimeError):
        document._validate_color(color)
