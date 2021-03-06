import datetime
from time import strftime
from create_folders import create_folders
from python_ifirma.core import iFirmaAPI, Client, Address, Position, VAT, NewInvoiceParams
from python_ifirma.config import IFIRMA_USER, IFIRMA_INVOICE_KEY, IFIRMA_USER_KEY, NET, POSITION_NAME, FILE_PATH \
    , CLIENT_NAME, CLIENT_TAX_ID, CLIENT_CITY, CLIENT_POSTALCODE, CLIENT_STREET, CLIENT_COUNTRY, DAY_OF_INVOICE, \
    PAYMENT_DAYS, FILE_NAME, INVOICE_MONTH


def main():
    ifirma_client = iFirmaAPI(IFIRMA_USER, IFIRMA_INVOICE_KEY, IFIRMA_USER_KEY)

    client = Client(
        CLIENT_NAME,  # company name
        CLIENT_TAX_ID,  # Tax ID
        Address(
            CLIENT_CITY,
            CLIENT_POSTALCODE,
            CLIENT_STREET,  # Street
            CLIENT_COUNTRY  # Country
        )

    )

    position = Position(
        VAT.VAT_23,  # VAT rate
        1,  # Quantity
        NET,  # Unit total price
        POSITION_NAME,  # Position name
        "szt"  # Position unit
    )
    # create folders to generate the file.
    path_altalog_documents = create_folders(folder='/altalog_documents', month=INVOICE_MONTH)
    print(path_altalog_documents)
    issue_year_month = strftime("%Y-%m",
                                datetime.date.today().timetuple())  # issue date can't be earlier than last invoice date
    issue_date = issue_year_month + '-' + str(DAY_OF_INVOICE)

    invoice = NewInvoiceParams(client, [position], issue_date, PAYMENT_DAYS)
    print(invoice)

    invoice_id, invoice_number = ifirma_client.generate_invoice(invoice)

    pdf_file_obj = ifirma_client.get_invoice_pdf(invoice_id)

    with open(path_altalog_documents + '/' + FILE_NAME + ' - ' + issue_year_month + ' - ' + 'faktura.pdf', 'wb') as f:
        f.write(pdf_file_obj.getvalue())
    pdf_file_obj.close()


if __name__ == "__main__":
    main()
