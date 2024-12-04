import glob
import os
import smtplib
import ssl
from email.message import EmailMessage
from fpdf import FPDF
import pandas

# Read the
df = pandas.read_csv("hotels.csv", dtype={"id":str})

def clean_file():
    file_pdf = glob.glob("reservation.pdf")
    for pdf_files in  file_pdf:
        os.remove(pdf_files)
    print("pdf file removed")

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index = False)

    def available(self):
        """ Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your  reservation!
        Here are your booking data:
        Name:-{self.customer_name}.
        Hotel Name:-{self.hotel.name}, {self.hotel.city}
        """
        return content


class Email:
    def send(self, message, subject, filename):
        host = "smtp.gmail.com"
        port = 465

        username = "p.nikul6403@gmail.com"
        password = "gwhr ayyg xjyh eozy"

        receiver = "p.nikul1603@gmail.com"
        context = ssl.create_default_context()

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = receiver
        msg.set_content(message)

        # Attach PDF file
        with open(filename, 'rb') as file:
            file_data = file.read()
            file_name = file.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
        print("Email was sent!")

class PDF:
    def __init__(self, customer_name, hotel_name, hotel_city):
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.hotel_city = hotel_city

    def pdf_generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Arial", size=18, style="BIU")
        pdf.cell(w=0, h=10, txt="Thank you for your reservation!", ln=2)

        pdf.set_font(family="Arial", size=16, style="B")
        pdf.cell(w=0, h=10, txt="Here are your booking data:", ln=True)

        pdf.set_font(family="Arial", size=16, style="B")
        pdf.cell(w=0, h=10, txt=f"Name: {self.customer_name}.", ln=True)

        pdf.set_font(family="Arial", size=16, style="B")
        pdf.cell(w=0, h=10, txt=f"Hotel Name: {self.hotel_name}, {self.hotel_city}", ln=True)

        pdf_file = "reservation.pdf"
        pdf.output(pdf_file )
        print("pdf generate!")
        return pdf_file

print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_ticket = ReservationTicket(customer_name=name,  hotel_object=hotel)
    print(reservation_ticket.generate())

    pdf = PDF(customer_name=name, hotel_name=hotel.name, hotel_city=hotel.city)
    pdf_filename = pdf.pdf_generate()

    email = Email()
    email.send(subject="Hotel Reservation Confirmation", message=reservation_ticket.generate(), filename=pdf_filename)

    clean_file()

else:
    print("Hotel is not free!")