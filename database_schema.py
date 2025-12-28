from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


# where all table definitions are registered
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customers'
    
    customer_id = Column(Integer, primary_key=True)
    organisation_or_person = Column(String)
    organisation_name = Column(String)
    gender = Column(String)
    first_name = Column(String)
    middle_initial = Column(String)
    last_name = Column(String)
    email_address = Column(String)
    login_name = Column(String)
    login_password = Column(String)
    phone_number = Column(String)
    address_line_1 = Column(String)
    address_line_2 = Column(String)
    address_line_3 = Column(String)
    address_line_4 = Column(String)
    town_city = Column(String)
    county = Column(String)
    country = Column(String)
    
    orders = relationship("Order", back_populates="customer")
    payment_methods = relationship("CustomerPaymentMethod", back_populates="customer")

class CustomerPaymentMethod(Base):
    __tablename__ = 'Customer_Payment_Methods'
    
    customer_payment_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.customer_id'))
    payment_method_code = Column(String, ForeignKey('Ref_Payment_Methods.payment_method_code'))
    credit_card_number = Column(String)
    payment_method_details = Column(String)
    
    customer = relationship("Customer", back_populates="payment_methods")
    method_details = relationship("RefPaymentMethod")

class Product(Base):
    __tablename__ = 'Products'
    
    product_id = Column(Integer, primary_key=True)
    product_type_code = Column(String, ForeignKey('Ref_Product_Types.product_type_code'))
    return_merchandise_authorization_nr = Column(String)
    product_name = Column(String)
    product_price = Column(Float)
    product_color = Column(String)
    product_size = Column(String)
    product_description = Column(String)
    other_product_details = Column(String)
    
    product_type = relationship("RefProductType")

# ----------------------------
# Order Processing Domain
# ----------------------------

class Order(Base):
    __tablename__ = 'Orders'
    
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.customer_id'))
    order_status_code = Column(String, ForeignKey('Ref_Order_Status_Codes.order_status_code'))
    date_order_placed = Column(DateTime)
    order_details = Column(String)
    
    customer = relationship("Customer", back_populates="orders")
    status = relationship("RefOrderStatusCode")
    order_items = relationship("OrderItem", back_populates="order")
    invoices = relationship("Invoice", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'Order_Items'
    
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Products.product_id'))
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    order_item_status_code = Column(String, ForeignKey('Ref_Order_Item_Status_Codes.order_item_status_code'))
    order_item_quantity = Column(Integer)
    order_item_price = Column(Float)
    rma_number = Column(String)
    rma_issued_by = Column(String)
    rma_issued_date = Column(DateTime)
    other_order_item_details = Column(String)
    
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")
    status = relationship("RefOrderItemStatusCode")

# ----------------------------
# Billing & Shipping Domain
# ----------------------------

class Invoice(Base):
    __tablename__ = 'Invoices'
    
    invoice_number = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    invoice_status_code = Column(String, ForeignKey('Ref_Invoice_Status_Codes.invoice_status_code'))
    invoice_date = Column(DateTime)
    invoice_details = Column(String)
    
    order = relationship("Order", back_populates="invoices")
    status = relationship("RefInvoiceStatusCode")
    payments = relationship("Payment", back_populates="invoice")
    shipments = relationship("Shipment", back_populates="invoice")

class Payment(Base):
    __tablename__ = 'Payments'
    
    payment_id = Column(Integer, primary_key=True)
    invoice_number = Column(Integer, ForeignKey('Invoices.invoice_number'))
    payment_date = Column(DateTime)
    payment_amount = Column(Float)
    
    invoice = relationship("Invoice", back_populates="payments")

class Shipment(Base):
    __tablename__ = 'Shipments'
    
    shipment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    invoice_number = Column(Integer, ForeignKey('Invoices.invoice_number'))
    shipment_tracking_number = Column(String)
    shipment_date = Column(DateTime)
    other_shipment_details = Column(String)
    
    order = relationship("Order", back_populates="shipments")
    invoice = relationship("Invoice", back_populates="shipments")
    shipment_items = relationship("ShipmentItem", back_populates="shipment")

class ShipmentItem(Base):
    __tablename__ = 'Shipment_Items'
    
    # Composite Primary Key
    shipment_id = Column(Integer, ForeignKey('Shipments.shipment_id'), primary_key=True)
    order_item_id = Column(Integer, ForeignKey('Order_Items.order_item_id'), primary_key=True)
    
    shipment = relationship("Shipment", back_populates="shipment_items")
    order_item = relationship("OrderItem")