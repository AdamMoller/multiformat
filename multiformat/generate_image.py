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
from PIL import Image as ImagePIL
from PIL import ImageFont, ImageDraw


class _Image:
    # Generate the document as image(s)
    def __init__(self, file_name, image_format, document_wh, image_wh=None):
        self.scale = 1
        self.file_name = file_name
        self.image_format = image_format
        self.output_dimensions = None
        if image_wh:
            scaleW = image_wh[0] / document_wh[0]
            scaleH = image_wh[1] / document_wh[1]
            if scaleW < scaleH:
                if scaleW > 1:
                    output_w = image_wh[0]
                    output_h = int(document_wh[1] * scaleW)
                    self.scale = scaleW
                else:
                    output_w = image_wh[0]
                    output_h = int(document_wh[1] * scaleW)
                    self.output_dimensions = (image_wh[0],
                                              int(document_wh[1] * scaleW))
                    output_w = document_wh[0]
                    output_h = document_wh[1]
            else:
                if scaleH > 1:
                    output_w = int(document_wh[0] * scaleH)
                    output_h = image_wh[1]
                    self.scale = scaleH
                else:
                    self.output_dimensions = (int(document_wh[0] * scaleH),
                                              image_wh[1])
                    output_w = document_wh[0]
                    output_h = document_wh[1]
        else:
            output_w = document_wh[0]
            output_h = document_wh[1]
        self.image = ImagePIL.new("RGB", (output_w, output_h), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def draw_string(self, string, x, y, alignment, font, size, color):
        # Add a string to the image at the defined coordinates.
        font_file = os.path.join(
            os.path.dirname(__file__), 'fonts', '{}.ttf'.format(font))
        font = ImageFont.truetype(font_file, size)
        w, h = self.draw.textsize(str(string), font)
        y = y - h
        if alignment.lower() == "middle":
            x = x - w / 2
        elif alignment.lower() == "right":
            x = x - w
        self.draw.text((x, y), str(string), fill=color, font=font)

    def draw_line(self, x, y, x1, y1, width, color):
        # Add a line to the image between (x,y) and (x1,y1).
        self.draw.line(
            [(int(x * self.scale), int(y * self.scale)),
             (int(x1 * self.scale), int(y1 * self.scale))],
            fill=color,
            width=int(width * self.scale))

    def draw_rectangle(self, x, y, w, h, fill_color, border_color,
                       border_width):
        # Draw a rectangle on the image with the upper left corner at (x,y).
        x = int(x * self.scale)
        y = int(y * self.scale)
        w = int(w * self.scale)
        h = int(h * self.scale)
        border_width = int(border_width * self.scale)
        x1 = x + w
        y1 = y
        x2 = x + w
        y2 = y + h
        x3 = x
        y3 = y + h
        self.draw.polygon(
            [(x, y), (x1, y1), (x2, y2), (x3, y3)], fill=fill_color)
        half_border_width = border_width * 0.5
        x1a = x - half_border_width
        y1a = y
        x1b = x1 + half_border_width
        y1b = y1
        x3a = x2 + half_border_width
        x3b = x3 - half_border_width
        self.draw.line(
            [(x1a, y), (x1b, y1)], fill=border_color, width=border_width)
        self.draw.line(
            [(x1, y1), (x2, y2)], fill=border_color, width=border_width)
        self.draw.line(
            [(x3a, y2), (x3b, y3)], fill=border_color, width=border_width)
        self.draw.line(
            [(x3, y3), (x, y)], fill=border_color, width=border_width)

    def save(self):
        # Save the image to a file
        if self.output_dimensions:
            self.image = self.image.resize(
                self.output_dimensions, resample=ImagePIL.ANTIALIAS)
        self.image.save("{}.{}".format(self.file_name, self.image_format),
                        self.image_format)
