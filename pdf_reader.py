from PyPDF2 import PdfReader




def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


extract_information("pdf.pdf")

with open("pdf.pdf", 'rb') as f:
    pdf = PdfReader(f)
    information = pdf.metadata
    number_of_pages = len(pdf.pages)
    print(pdf.pages(1))