from docx import Document

client_data = [
            {'name': 'solar_panel : ' + 'invoice.solar_panel.name', 'quantity': 'invoice.solar_panel_quantity', 'price': 'invoice.solar_panel_price'},
            {'name': 'inverter : ' + 'invoice.inverter.name', 'quantity': 'invoice.inverter_quantity', 'price': 'invoice.inverter_price'},
            {'name': 'structure : ' + 'invoice.structure.name', 'quantity': 'invoice.structure_quantity', 'price': 'invoice.structure_price'},
            {'name': 'cabling : ' + 'invoice.cabling.name', 'quantity': 'invoice.cabling_quantity', 'price': 'invoice.cabling_price'},
            {'name': 'net_metering : ' + 'invoice.net_metering.name', 'quantity':' invoice.net_metering_quantity', 'price': 'invoice.net_metering_price'},
            ]
def handle_table3(table,invoice):
    total = 0
    row_index = 1  # Assuming the first row is the header row
    total = 1000  # Dummy total value, replace with actual calculation if available

    # List of data to insert into the table
    data = [
        ("Subtotal", total),
        ("Discount", invoice.discount),
        ("Discounted Amount", total - int(invoice.discount)),
        ("Partially Paid", invoice.amount_paid),
        ("Shipping", invoice.shipping_charges),
        ("Total", total - int(invoice.discount) + int(invoice.shipping_charges) - int(invoice.amount_paid))
    ]

    # Starting row index (assuming the first row is the header)
    start_row_index = 6  # Adjust this based on where you want to start

    for index, (label, value) in enumerate(data):
        row = table.add_row()
        row = table.rows[row_index].cells
        row[3].text = label  # Label column (adjust column index if needed)
        row[4].text = str(value)  # Value column (adjust column index if needed)
        row_index += 1

# Usage
docx_file_path = r'C:\Users\DELL\Downloads\template.docx'
doc = Document(docx_file_path)
class DummyInvoice:
    discount = 50
    amount_paid = 200
    shipping_charges = 30
invoice = DummyInvoice()
table = doc.tables[3]
handle_table3(table,invoice)
doc.save('new.docx')