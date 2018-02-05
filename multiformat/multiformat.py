# Copyright 2018 Adam Moller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from .generate_pdf import _PDF
from .generate_image import _Image


class Document:
    """Entry point for creating documents

    This object includes methods for adding elements to a document and
    generating the document as a pdf or image.

    Attributes:
        document_size: A string defining the page size (a4, letter).
        layout: A string defining the page orientation (portrait, landscape).
    """

    def __init__(self, document_size="a4", layout="portrait"):
        """Inits the document with page size, layout, and dimensions.

        Also looks for available fonts in the fonts directory,
        defines metadata variables, and a list to store the document contents.
        """
        self.document_size = document_size.lower()
        if self.document_size not in ["a4", "letter"]:
            _error("Invalid document size: '{}'".format(document_size),
                   "KeyError")
        self.layout = layout.lower()
        if self.layout not in ["landscape", "portrait"]:
            _error("Invalid document layout: '{}'".format(layout), "KeyError")
        page_dimensions = {
            'a4': {
                'landscape': {
                    'w': 2970,
                    'h': 2100
                },
                'portrait': {
                    'w': 2100,
                    'h': 2970
                },
            },
            'letter': {
                'landscape': {
                    'w': 2794,
                    'h': 2159
                },
                'portrait': {
                    'w': 2159,
                    'h': 2794
                },
            }
        }
        # Create list of TrueType fonts in fonts directory.
        self.supported_fonts = []
        for file in os.listdir(
                os.path.join(os.path.dirname(__file__), 'fonts')):
            if file.endswith(".ttf"):
                self.supported_fonts.append(os.path.splitext(file)[0])
        # Define document width and height based on page size and layout
        self.w = page_dimensions[self.document_size][self.layout]["w"]
        self.h = page_dimensions[self.document_size][self.layout]["h"]
        self.author = None
        self.title = None
        self.subject = None
        self._document = []

    def draw_string(self, string, x, y, alignment, font, size, color):
        """Add a string to the document.

        Adds a text string to the document that will be printed after all
        previous additions to the document.

        Args:
            string: String that will be drawn on the document
            x: x-axis alignment point of the text. (Integer)
            y: y-axis bottom of the text (Integer)
            alignment: "left", "right", "middle" (String)
            font: TTF file name without extension (String)
            size: Font size in hundredths of a centimeter (Integer)
            color: RGB color code (Tuple)

        Returns:
            None
        """
        self._document.append({
            "type":
            "string",
            "string":
            self._validate_string(string),
            "x":
            self._validate_x_var(x),
            "y":
            self._validate_y_var(y),
            "alignment":
            self._validate_alignment(alignment),
            "font":
            self._validate_font(font),
            "size":
            self._validate_size(size),
            "color":
            self._validate_color(color),
        })

    def draw_line(self, x, y, x1, y1, width, color):
        """Add a line to the document.

        Adds a line to the document defined by a start and end point.

        Args:
            x: x-axis start of the line. (Integer)
            y: y-axis start of the line. (Integer)
            x1: x-axis end of the line. (Integer)
            y1: y-axis end of the line (Integer)
            width: Width of the line. (Integer)
            color: RGB color of the line. (Tuple)

        Returns:
            None
        """
        self._document.append({
            "type": "line",
            "x": self._validate_x_var(x),
            "y": self._validate_y_var(y),
            "x1": self._validate_x_var(x1),
            "y1": self._validate_y_var(y1),
            "width": self._validate_size(width),
            "color": self._validate_color(color),
        })

    def draw_rectangle(self,
                       x,
                       y,
                       w,
                       h,
                       fill_color=(0, 0, 0),
                       border_color=(0, 0, 0),
                       border_width=0):
        """Add a rectangle to the document.

        Add a rectangle to the document with fill and optional border.

        Args:
            x: x-axis top of the rectangle. (Integer)
            y: y-axis left of the rectangle (Integer)
            w: Width of the rectangle. (Integer)
            h: Height of the rectangle. (Integer)
            fill_color: RGB color of the interior (Tuple)
            border_color: RGB color of the border (Tuple)
            w: Width of the border. Set at 0 for no border (Integer)

        Returns:
            None
        """
        valid_border_width = self._validate_size(border_width)
        if fill_color is None and (valid_border_width <= 0
                                   or border_color is None):
            _error("Rectangle requires border or fill")
        valid_border_color = None
        if valid_border_width > 0:
            valid_border_color = self._validate_color(border_color)

        self._document.append({
            "type":
            "rectangle",
            "x":
            self._validate_x_var(x),
            "y":
            self._validate_y_var(y),
            "w":
            self._validate_w_var(x, w),
            "h":
            self._validate_h_var(y, h),
            "fill_color":
            self._validate_color(fill_color, required=False),
            "border_color":
            valid_border_color,
            "border_width":
            valid_border_width,
        })

    def insert_page_break(self):
        """Insert page break

        Add a page break to the document. When the document is generated as an
        image each page becomes a new image.

        Args:
            None

        Returns:
            None
        """
        self._document.append({
            "type": "page_break",
        })

    def generate_pdf(self, file_name, file_object=None):
        """Generate the document as a PDF.

        Generate the document as a PDF based on the elements defined with other
        methods.

        PDF will be saved to the current directory if a file-like object is
        not assigned to the file_object parameter.

        Args:
            file_name: name of the pdf file, without extension. (String)
            file_object: optional file-like object to write to
        Returns:
            None
        """
        pdf = _PDF(
            file_name,
            self.document_size,
            self.layout,
            file_object=file_object)
        pdf.set_metadata(
            author=self.author, title=self.title, subject=self.subject)
        for item in self._document:
            if item["type"] == "string":
                pdf.draw_string(item["string"], item["x"], item["y"],
                                item["alignment"], item["font"], item["size"],
                                item["color"])
            elif item["type"] == "line":
                pdf.draw_line(item["x"], item["y"], item["x1"], item["y1"],
                              item["width"], item["color"])
            elif item["type"] == "rectangle":
                pdf.draw_rectangle(item["x"], item["y"], item["w"], item["h"],
                                   item["fill_color"], item["border_color"],
                                   item["border_width"])
            elif item["type"] == "page_break":
                pdf.new_page()
        pdf.save()

    def generate_image(self,
                       file_name,
                       image_format,
                       size=None,
                       file_object=None):
        """Generate the document as an image.

        Generate the document as an image based on the elements defined with
        other methods. Will create PNG, GIF, or JPEG images.

        Image will be saved to the current directory if a file-like object is
        not assigned to the file_object parameter.

        Args:
            file_name: name of the image file, without extension. (String)
            image_format: GIF, JPEG, PNG (String)
            size: Width and height of image in pixels (Integer, Integer)
            file_object: optional file-like object to write to

        Returns:
            None
        """
        image_count = 0
        if image_format.lower() == "png":
            image_format = "png"
        elif image_format.lower() == "gif":
            image_format = "gif"
        elif image_format.lower() == "jpeg":
            image_format = "jpeg"
        else:
            _error(
                "Image format not valid: Supported types are PNG, GIF, JPEG")
        if size:
            image = _Image(file_name, image_format, (self.w, self.h), size)
        else:
            image = _Image(file_name, image_format, (self.w, self.h))
        for item in self._document:
            if item["type"] == "string":
                image.draw_string(item["string"], item["x"], item["y"],
                                  item["alignment"], item["font"],
                                  item["size"], item["color"])
            elif item["type"] == "line":
                image.draw_line(item["x"], item["y"], item["x1"], item["y1"],
                                item["width"], item["color"])
            elif item["type"] == "rectangle":
                image.draw_rectangle(item["x"], item["y"], item["w"],
                                     item["h"], item["fill_color"],
                                     item["border_color"],
                                     item["border_width"])
            elif item["type"] == "page_break":
                # break if assigning to single file object
                if file_object:
                    break
                image.save()
                image_count = image_count + 1
                image = _Image("file_name_{}".format(image_count),
                               image_format, (self.w, self.h), size)
        image.save(file_object)

    def _validate_x_var(self, x):
        # Confirm x-coordinate is an integer and within document plane.
        try:
            x = int(x)
        except:
            _error("Invalid x variable: {}, Should be integer.".format(x))
        if x >= 0 and x <= self.w:
            return x
        else:
            _error("X variable not within document boundaries: {}".format(x))

    def _validate_y_var(self, y):
        # Confirm y-coordinate is an integer and within document plane.
        try:
            y = int(y)
        except:
            _error("Invalid y variable: {}, Should be integer.".format(y))
        if y >= 0 and y <= self.h:
            return y
        else:
            _error("Y variable not within document boundaries: {}".format(y))

    def _validate_w_var(self, x, w):
        # Confirm width is an integer and element doesn't extend outside
        # document plane.
        try:
            w = int(w)
            x2 = w + int(x)
        except:
            _error("Invalid width: {}, Width should be integer.".format(w))
        if x2 >= 0 and x2 <= self.w:
            return w
        else:
            _error(
                "Width variable not within document boundaries: {}".format(w))

    def _validate_h_var(self, y, h):
        # Confirm height is an integer and element doesn't extend outside
        # document plane.
        try:
            h = int(h)
            y2 = h + int(y)
        except:
            _error("Invalid width: {}, Width should be integer.".format(h))
        if y2 >= 0 and y2 <= self.h:
            return h
        else:
            _error(
                "Width variable not within document boundaries: {}".format(h))

    def _validate_alignment(self, alignment):
        # Confirm alignement is string and left, right, or middle.
        valid_alignments = ["left", "right", "middle"]
        alignment = str(alignment).lower()
        if alignment in valid_alignments:
            return alignment.lower()
        else:
            _error("Invalid alignment.")

    def _validate_font(self, font):
        # Confirm font name is valid.
        font = str(font)
        try:
            index = [x.lower() for x in self.supported_fonts].index(
                font.lower())
            return self.supported_fonts[index]
        except:
            _error(
                "Font named ({}) not valid. Custom fonts need to be loaded.".
                format(font))

    def _validate_size(self, size):
        # Confirm size is an integer >= 0.
        try:
            size = int(size)
        except:
            _error("Invalid size. Size should be integer.")
        if size >= 0:
            return size
        else:
            _error("Invalid size. Size should be >= 0.")

    def _validate_string(self, string):
        # Confirm strings are strings.
        return str(string)

    def _validate_color(self, color, required=True):
        # Confirm RGB colors are tuples of 3 integers 0 to 255.
        if not color and required is False:
            return None
        try:
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
        except:
            _error("Invalid RGB color code: {}".format(color))
        if r < 0 or r > 255:
            _error("Invalid RGB color code red value: {}".format(r))
        if g < 0 or g > 255:
            _error("Invalid RGB color code green value: {}".format(g))
        if b < 0 or b > 255:
            _error("Invalid RGB color code blue value: {}".format(b))
        return (r, g, b)


def _error(statement, error_type=""):
    # Used to trigger exceptions with customized statements
    if error_type == "KeyError":
        raise KeyError(statement)
    else:
        raise RuntimeError(statement)
