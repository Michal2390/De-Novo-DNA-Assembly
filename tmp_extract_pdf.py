import pdfplumber

with pdfplumber.open(r'C:\Users\Michał\OneDrive\Desktop\Studia magisterskie EITI\MBI\lab2\input\MBI___lab_2-wzorzec.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
