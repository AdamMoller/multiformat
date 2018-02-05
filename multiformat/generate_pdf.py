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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class _PDF:
    # Generate a PDF with the reportlab open source toolkit.
    def __init__(self, file_name, document_size, orientation,
                 file_object=None):
        if document_size == "letter":
            standard_doc_size = letter
        elif document_size == "a4":
            standard_doc_size = A4
        if file_object:
            self.pdf = canvas.Canvas(
                file_object, pagesize=standard_doc_size, bottomup=0)
        else:
            self.pdf = canvas.Canvas(
                "{}.pdf".format(file_name),
                pagesize=standard_doc_size,
                bottomup=0)
        self.loaded_fonts = [
            "Courier",
            "Courier-Bold",
            "Courier-BoldOblique",
            "Courier-Oblique",
            "Helvetica",
            "Helvetica-Bold",
            "Helvetica-BoldOblique",
            "Helvetica-Oblique",
            "Times-Bold",
            "Times-BoldItalic",
            "Times-Italic",
            "Times-Roman",
        ]

    def set_metadata(self, author, title, subject):
        # Set metadata for a document.
        if author:
            self.pdf.setAuthor(author)
        if title:
            self.pdf.setTitle(title)
        if subject:
            self.pdf.setSubject(subject)

    def draw_string(self, string, x, y, alignment, font, size, color):
        # Add a string to a document at the defined coordinates.
        size = (size / 100) * cm
        x = (x / 100) * cm
        y = (y / 100) * cm
        self.use_font(font, size)
        self.pdf.setFillColorRGB(color[0] / 255, color[1] / 255,
                                 color[2] / 255)
        if alignment.lower() == "right":
            self.pdf.drawRightString(x, y, str(string))
        elif alignment.lower() == "middle":
            self.pdf.drawCentredString(x, y, str(string))
        else:
            self.pdf.drawString(x, y, str(string))

    def draw_line(self, x, y, x1, y1, width, color):
        # Add a line to the document between (x,y) and (x1,y1).
        x = (x / 100) * cm
        y = (y / 100) * cm
        x1 = (x1 / 100) * cm
        y1 = (y1 / 100) * cm
        self.pdf.setLineWidth((width / 100) * cm)
        self.pdf.setStrokeColorRGB(color[0] / 255, color[1] / 255,
                                   color[2] / 255)
        self.pdf.line(x, y, x1, y1)

    def draw_rectangle(self, x, y, w, h, fill_color, border_color,
                       border_width):
        # Draw a rectangle with the upper left corner at (x,y).
        x = (x / 100) * cm
        y = (y / 100) * cm
        w = (w / 100) * cm
        h = (h / 100) * cm
        self.pdf.setFillColorRGB(fill_color[0] / 255, fill_color[1] / 255,
                                 fill_color[2] / 255)
        if border_width > 0:
            self.pdf.setStrokeColorRGB(border_color[0] / 255,
                                       border_color[1] / 255,
                                       border_color[2] / 255)
            self.pdf.setLineWidth((border_width / 100) * cm)
        else:
            self.pdf.setStrokeColorRGB(
                fill_color[0] / 255, fill_color[1] / 255, fill_color[2] / 255)
            self.pdf.setLineWidth(0)
        if fill_color is None:
            self.pdf.rect(x, y, w, h, fill=0)
        else:
            self.pdf.rect(x, y, w, h, fill=1)

    def save(self):
        # Save the document to a file.
        self.pdf.save()

    def new_page(self):
        # Start a new page in the document
        self.pdf.showPage()

    def use_font(self, font, size):
        # Register a font if it is not registered
        if font not in self.loaded_fonts:
            font_file = os.path.join(
                os.path.dirname(__file__), 'fonts', '{}.ttf'.format(font))
            pdfmetrics.registerFont(TTFont(font, font_file))
            self.loaded_fonts.append(font)
            self.pdf.setFont(font, size)
        else:
            self.pdf.setFont(font, size)
