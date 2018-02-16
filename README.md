# Multiformat
[![codecov](https://codecov.io/gh/AdamMoller/multiformat/branch/master/graph/badge.svg)](https://codecov.io/gh/AdamMoller/multiformat)
[![Build Status](https://travis-ci.org/AdamMoller/multiformat.svg?branch=master)](https://travis-ci.org/AdamMoller/multiformat)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

Generate documents in multiple formats using a single class.

## About
When dynamically generating PDF documents, thumbnail or preview images are sometimes required. With this package documents are designed using a single "Document" class that can generate documents in PDF, PNG, GIF, or JPEG format. The [ReportLab open-source PDF Toolkit](https://bitbucket.org/rptlab/reportlab) and [Pillow](https://github.com/python-pillow/Pillow) are utilized for PDF and image generation.

## Currently Supports
- Strings
- Lines
- Rectangles
- Circles
- TrueType fonts
- PDF metadata
- PNG, GIF, JPEG image format
- US Letter or A4 document size

## Usage

### Example
``` python
from multiformat.multiformat import Document

# Create a new document
document = Document(document_size='A4', layout='portrait')
# Add a green background
document.draw_rectangle(
    x=0,
    y=0,
    w=document.w,
    h=document.h,
    fill_color=(29, 179, 97),
    border_color=(0, 0, 0),
    border_width=0)
# Add "Hello World" to the bottom left.
document.draw_string(
    string="Hello World",
    x=100,
    y=document.h - 100,
    alignment="left",
    font="OpenSans-Bold",
    size=100,
    color=(255, 255, 255))
# Add an orange line from the top-left to the bottom-right
document.draw_line(
    x=0, y=0, x1=document.w, y1=document.h, width=50, color=(251, 176, 64))
# Insert page break
document.insert_page_break()
# Add an orange line from the top-right to the bottom-left
document.draw_line(
    x=document.w, y=0, x1=0, y1=document.h, width=50, color=(251, 176, 64))
# Generate the document as a PDF
document.generate_pdf(file_name="example")
# Generate page 1 of the document as a PNG no larger than 1000,1000
document.generate_image(
    file_name="example", image_format="PNG", size=(1000, 1000), page=1)
```
### New Document
``` python
document = Document(document_size, layout)
```
Inits the document with page size and layout.
- document_size: A string defining the page size (a4, letter).
- layout: A string defining the page orientation (portrait, landscape).

### Methods

#### Line
``` python
draw_line(x, y, x1, y1, width, color)
```
Adds a line to the document defined by a start and end point.
- x: x-axis start of the line. (Integer)
- y: y-axis start of the line. (Integer)
- x1: x-axis end of the line. (Integer)
- y1: y-axis end of the line (Integer)
- width: Width of the line. (Integer)
- color: RGB color of the line. (Tuple)

#### Rectangle
``` python
draw_rectangle(x, y, w, h, fill_color=(0, 0, 0), border_color=(0, 0, 0), border_width=0)
```
Add a rectangle to the document with fill and optional border.
- x: x-axis top of the rectangle. (Integer)
- y: y-axis left of the rectangle (Integer)
- w: Width of the rectangle. (Integer)
- h: Height of the rectangle. (Integer)
- fill_color: RGB color of the interior (Tuple)
- border_color: RGB color of the border (Tuple)
- border_width: Width of the border. Set at 0 for no border (Integer)

#### Circle
``` python
draw_circle(x, y, radius, fill_color=(0, 0, 0), border_color=(0, 0, 0), border_width=0)
```
Add a circle to the document with fill and optional border.
- x: x-axis center of the circle. (Integer)
- y: y-axis center of the circle. (Integer)
- radius: Radius of the circle. (Integer)
- fill_color: RGB color of the interior (Tuple)
- border_color: RGB color of the border (Tuple)
- border_width: Width of the border. Set at 0 for no border (Integer)


#### String
``` python
draw_string(string, x, y, alignment, font, size, color)
```
Adds a text string to the document that will be printed after all previous additions to the document.
- string: String that will be drawn on the document
- x: x-axis alignment point of the text. (Integer)
- y: y-axis bottom of the text (Integer)
- alignment: "left", "right", "middle" (String)
- font: TTF file name without extension (String)
- size: Font size in hundredths of a centimeter (Integer)
- color: RGB color code (Tuple)

#### New Page
``` python
insert_page_break()
```
Add a page break to the document. When the document is generated as an image each page becomes a new image.

#### Generate Image
``` python
generate_image(file_name, image_format, size=None, page=None, file_object=None)
```
Generate the document as an image based on the elements defined with other methods. Will create PNG, GIF, or JPEG images.

Image will be saved to the current directory if a file-like object is not assigned to the file_object parameter.
- file_name: name of the image file, without extension. (String)
- image_format: GIF, JPEG, PNG (String)
- size: Width and height of image in pixels (Integer, Integer)
- page: Page to generate on multiple page documents
- file_object: optional file-like object to write to

#### Generate PDF
``` python
generate_pdf(file_name, file_object=None)
```
Generate the document as a PDF based on the elements defined with other methods.

PDF will be saved to the current directory if a file-like object is not assigned to the file_object parameter.
- file_name: name of the pdf file, without extension. (String)
- file_object: optional file-like object to write to

## Colors
Page element methods currently support decimal RGB colors as a 3-Tuple and hexadecimal colors as strings.

Here are some examples of acceptable color formats for the color white:
- "FFF"
- "#FFF"
- "FFFFFF"
- "#FFFFFF"
- (255,255,255)

## Fonts
Multiformat supports TrueType fonts (TTF). The following open source fonts are included in the package:
- OpenSans-Bold
- OpenSans-Regular

Additional fonts can be added by placing the font's TTF file in the "fonts" directory of the Multiformat package. The 14 standard PDF fonts will only work for creating PDF files. These fonts will need to be licensed and added to the fonts directory before creating images. The 14 fonts are:
- Courier
- Courier-Bold
- Courier-BoldOblique
- Courier-Oblique
- Helvetica
- Helvetica-Bold
- Helvetica-BoldOblique
- Helvetica-Oblique
- Times-Bold
- Times-BoldItalic
- Times-Italic
- Times-Roman
