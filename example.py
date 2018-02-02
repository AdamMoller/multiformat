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
# Generate the document as a PDF
document.generate_pdf(file_name="example")
# Generate the document as a PNG no larger than 1000,1000
document.generate_image(
    file_name="example", image_format="PNG", size=(1000, 1000))
