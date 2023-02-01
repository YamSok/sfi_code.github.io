from PyPDF2 import PdfReader
import pandas as pd
import json
import re

def df_to_json(df, outfile):

    j = []
    for i in range(len(df)):
        j.append({"name": f"({df.iloc[i]['sfi_code']}) {df.iloc[i]['sfi_label']}"})

    outfile = open(outfile, "w")
    json.dump(j, outfile, indent=4)

def get_content():
    content = []

    # Open the pdf file
    with open("sfi_detail.pdf", "rb") as file:
        # Create a pdf reader object
        pdf_reader = PdfReader(file)

        # Get the number of pages in the pdf
        num_pages = len(pdf_reader.pages)

        # Iterate through each page
        for page_num in range(5, num_pages):
            # Get the page object
            page = pdf_reader.pages[page_num]

            # Extract the text from the page
            text = page.extract_text()

            # texte contenant un point (code supérieur à 3 digits)
            text = [x.strip() for x in text.split("\n") if (x != " ")]

            content.extend(text)

    # Split entre code et label
    d = [
        {"sfi_code": x.split(" ")[0], "sfi_label": " ".join(x.split(" ")[1:])}
        for x in content
    ]

    df = pd.DataFrame.from_records(d)
    df = df[df["sfi_label"].apply(lambda x: x != "")]
    
    # Enlever les espaces parasites à la fin
    df["sfi_label"] = df["sfi_label"].apply(lambda x: x.strip())
    
    return df


def main():
    df = get_content()

    for i in [1,2,3,7]:
        codes = df.copy(deep=True)
        codes = codes[codes["sfi_code"].apply(lambda x: len(x) == i)]
        df_to_json(codes, f'sfi_{i}.json')


main()
