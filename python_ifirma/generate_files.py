from python_ifirma.core import iFirmaAPI,Client,Address,Position,VAT,NewInvoiceParams
from python_ifirma.config import IFIRMA_USER ,IFIRMA_INVOICE_KEY ,IFIRMA_USER_KEY,GROSS ,POSITION_NAME,INVOICE_LINK,CLIENT_NAME,CLIENT_TAX_ID,CLIENT_CITY,CLIENT_POSTALCODE,CLIENT_STREET,CLIENT_COUNTRY



def main():
    ifirma_client = iFirmaAPI(IFIRMA_USER, IFIRMA_INVOICE_KEY, IFIRMA_USER_KEY)
    client = Client(
        CLIENT_NAME,  # company name
        CLIENT_TAX_ID,  # Tax ID
        Address(
            CLIENT_CITY,
            CLIENT_POSTALCODE,
            CLIENT_STREET , # Street
            CLIENT_COUNTRY  # Country
        )

    )

    position = Position(
        VAT.VAT_23,  # VAT rate
        1,  # Quantity
        GROSS,  # Unit total price
        POSITION_NAME,  # Position name
        "szt"  # Position unit
    )

    invoice = NewInvoiceParams(client, [position])

    invoice_id,invoice_number = ifirma_client.generate_invoice(invoice)

    pdf_file_obj = ifirma_client.get_invoice_pdf(invoice_id)


    with open(INVOICE_LINK +'fakturka.pdf', 'wb') as f:
        f.write(pdf_file_obj.getvalue())
    pdf_file_obj.close()


if __name__ == "__main__":
    main()