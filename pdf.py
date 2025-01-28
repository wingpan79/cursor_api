from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from datetime import datetime, date
from reportlab.pdfgen import canvas

import os


class DeliveryInvoice:
    def __init__(self, invoice_number, customer_name, customer_address, items, total_amount, barcode_data):
        self.invoice_number = invoice_number
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.items = items
        self.total_amount = total_amount
        self.invoice_date = date.today()
        self.barcode_data = barcode_data

    def generate_barcode(self, data, width=2*inch, height=0.5*inch):
        """
        Generate a barcode using ReportLab's built-in functionality
        
        :param data: String to encode in barcode
        :param width: Width of barcode (default: 2 inches)
        :param height: Height of barcode (default: 0.5 inches)
        :return: Drawing object containing the barcode
        """
        try:
            # Create Code128 barcode
            barcode = code128.Code128(data)
            barcode.barWidth = 1.2
            barcode.barHeight = height
            
            # Calculate barcode width based on data
            barcode_width = barcode.width
            x_offset = (width - barcode_width) / 2  # Center the barcode
            
            # Create drawing of the right size
            drawing = Drawing(width, height)
           
            # Add barcode to the drawing, centered
            barcode.drawOn(canvas.Canvas(drawing), x_offset, 0)
            
            return barcode
            
        except Exception as e:
            print(f"Error generating barcode: {e}")
            return None

    def generate_pdf(self, filename='delivery_invoice.pdf'):
        """
        Generate PDF invoice
        
        :param filename: Output PDF filename
        :return: Path to generated PDF
        """
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        # Create story elements
        story = []
        
        # Company header
        styles = getSampleStyleSheet()
        story.append(Paragraph("ACME Delivery Services", styles['Title']))
        story.append(Paragraph("123 Delivery Street, Logistics City", styles['Normal']))
        story.append(Paragraph("Phone: (555) 123-4567", styles['Normal']))
        story.append(Paragraph(" ", styles['Normal']))

        # Generate barcode
        barcode_drawing = self.generate_barcode(self.barcode_data)

        # Invoice details
        details = [
            ["Invoice Number", self.invoice_number],
            ["Invoice Date", self.invoice_date.strftime("%B %d, %Y")],
            ["Customer", self.customer_name],
            ["Delivery Address", self.customer_address],
        ]
        
        # Add barcode if generation was successful
        if barcode_drawing:
            details.append(["Barcode", barcode_drawing])

        details_table = Table(details, colWidths=[3*inch, 4*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),  # Vertical alignment
            ('ALIGN', (0,0), (1,-1), 'CENTER')  # Center align the barcode
        ]))
        story.append(details_table)
        story.append(Paragraph(" ", styles['Normal']))

        # Items table
        headers = ["Item", "Quantity", "Unit Price", "Total"]
        table_data = [headers]
        for item in self.items:
            table_data.append([
                item['name'], 
                item['quantity'], 
                f"${item['unit_price']:.2f}", 
                f"${item['quantity'] * item['unit_price']:.2f}"
            ])
        
        # Add total row
        table_data.append(["", "", "Total:", f"${self.total_amount:.2f}"])
        
        items_table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ]))
        story.append(items_table)

        # Footer
        story.append(Paragraph(" ", styles['Normal']))
        story.append(Paragraph("Thank you for your business!", styles['Normal']))

        # Build PDF
        doc.build(story)
        return os.path.abspath(filename)

# Example usage
def main():
    print("Generating invoice...")
   
    items = [
        {"name": "Laptop Delivery", "quantity": 2, "unit_price": 50.00},
        {"name": "Express Shipping", "quantity": 1, "unit_price": 25.00}
    ]
    
    invoice = DeliveryInvoice(
        invoice_number="INV-2024-001",
        customer_name="John Doe",
        customer_address="456 Main Street, Anytown, USA",
        items=items,
        total_amount=125.00,
        barcode_data="INV2024001"  # Simplified barcode data
    )
    
    pdf_path = invoice.generate_pdf()
    print(f"Invoice generated: {pdf_path}")

if __name__ == "__main__":
    main()