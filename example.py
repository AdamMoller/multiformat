from multiformat.multiformat import Document

# Create a new document.
document = Document(document_size='A4', layout='portrait')
# Add titles
document.draw_string(
    string="Multiformat",
    x=100,
    y=250,
    alignment="left",
    font="OpenSans-Bold",
    size=150,
    color=(44, 62, 80))

# Circles
document.draw_string(
    string="Circles",
    x=100,
    y=450,
    alignment="left",
    font="OpenSans-Bold",
    size=100,
    color=(44, 62, 80))
document.draw_circle(
    x=250,
    y=650,
    radius=150,
    fill_color=None,
    border_color=(142, 68, 173),
    border_width=10)
document.draw_circle(
    x=650,
    y=650,
    radius=150,
    fill_color=(41, 128, 185),
    border_color=(142, 68, 173),
    border_width=10)
document.draw_circle(
    x=1050,
    y=650,
    radius=150,
    fill_color=(41, 128, 185),
    border_color=(142, 68, 173),
    border_width=0)

# Lines
document.draw_string(
    string="Lines",
    x=100,
    y=1050,
    alignment="left",
    font="OpenSans-Bold",
    size=100,
    color=(44, 62, 80))
document.draw_line(
    x=100, y=1100, x1=document.w - 100, y1=1100, width=10, color=(231, 76, 60))
document.draw_line(
    x=100,
    y=1250,
    x1=document.w - 100,
    y1=1250,
    width=40,
    color=(230, 126, 34))

# Rectangles
document.draw_string(
    string="Rectangles",
    x=100,
    y=1650,
    alignment="left",
    font="OpenSans-Bold",
    size=100,
    color=(44, 62, 80))
document.draw_rectangle(
    x=100,
    y=1700,
    w=300,
    h=300,
    fill_color=None,
    border_color=(41, 128, 185),
    border_width=10)
document.draw_rectangle(
    x=500,
    y=1700,
    w=300,
    h=300,
    fill_color=(39, 174, 96),
    border_color=(41, 128, 185),
    border_width=10)
document.draw_rectangle(
    x=900,
    y=1700,
    w=300,
    h=300,
    fill_color=(39, 174, 96),
    border_color=(41, 128, 185),
    border_width=0)

# Strings
document.draw_string(
    string="Strings",
    x=100,
    y=2250,
    alignment="left",
    font="OpenSans-Bold",
    size=100,
    color=(44, 62, 80))
document.draw_string(
    string="Right Align",
    x=document.w / 2,
    y=2375,
    alignment="right",
    font="OpenSans-Regular",
    size=75,
    color=(142, 68, 173))
document.draw_string(
    string="Middle Align",
    x=document.w / 2,
    y=2475,
    alignment="middle",
    font="OpenSans-Regular",
    size=75,
    color=(41, 128, 185))
document.draw_string(
    string="Left Align",
    x=document.w / 2,
    y=2575,
    alignment="left",
    font="OpenSans-Regular",
    size=75,
    color=(39, 174, 96))

# Add line break.
document.insert_page_break()

# Add title.
document.draw_string(
    string="Page 2",
    x=100,
    y=250,
    alignment="left",
    font="OpenSans-Bold",
    size=150,
    color=(44, 62, 80))

# Generate the document as a PDF.
document.generate_pdf(file_name="example")
# Generate page 1 of the document as a PNG no larger than 1000,1000.
document.generate_image(
    file_name="example", image_format="PNG", size=(1000, 1000), page=1)
