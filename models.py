from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Base 설정
Base = declarative_base(metadata=MetaData())

# Restaurant 테이블 모델
class Restaurant(Base):
    __tablename__ = "Restaurant"
    __table_args__ = {"extend_existing": True}

    res_id = Column(String(10), primary_key=True)
    name = Column(String(50))
    address_si = Column(String(50))
    address_gu = Column(String(50))
    address_dong = Column(String(50))
    address_detail = Column(String(50))
    phone = Column(String(10))

# DeliveryAble 테이블 모델
class DeliveryAble(Base):
    __tablename__ = "DeliveryAble"
    __table_args__ = {"extend_existing": True}

    able_add = Column(String(10), primary_key=True)
    res_id = Column(String(10), ForeignKey("Restaurant.res_id"))
    address_si = Column(String(50))
    address_gu = Column(String(50))
    address_dong = Column(String(50))

# Menu 테이블 모델
class Menu(Base):
    __tablename__ = "Menu"
    __table_args__ = {"extend_existing": True}

    menu_id = Column(String(10), primary_key=True)
    res_id = Column(String(10), ForeignKey("Restaurant.res_id"))
    detail = Column(String(200))
    menu_name = Column(String(50))
    photo = Column(String(100))
    price = Column(Integer)

# Customer 테이블 모델
class Customer(Base):
    __tablename__ = "Customer"
    __table_args__ = {"extend_existing": True}

    cus_id = Column(String(10), primary_key=True)
    cus_name = Column(String(50))
    address_si = Column(String(50))
    address_gu = Column(String(50))
    address_dong = Column(String(50))
    address_detail = Column(String(50))

# Review 테이블 모델
class Review(Base):
    __tablename__ = "Review"
    __table_args__ = {"extend_existing": True}

    review_id = Column(String(10), primary_key=True)
    rec_id = Column(String(10), ForeignKey("Receipt.rec_id"))
    content = Column(String(200))
    photo = Column(String(100))
    star_rating = Column(Float)

# OrderList 테이블 모델
class OrderList(Base):
    __tablename__ = "OrderList"
    __table_args__ = {"extend_existing": True}

    order_id = Column(String(10), primary_key=True)
    menu_id = Column(String(10), ForeignKey("Menu.menu_id"))
    rec_id = Column(String(10), ForeignKey("Receipt.rec_id"))
    cus_id = Column(String(10), ForeignKey("Customer.cus_id"))

# Receipt 테이블 모델
class Receipt(Base):
    __tablename__ = "Receipt"
    __table_args__ = {"extend_existing": True}

    rec_id = Column(String(10), primary_key=True)
    cus_id = Column(String(10), ForeignKey("Customer.cus_id"))
    res_id = Column(String(10), ForeignKey("Restaurant.res_id"))
    order_date = Column(Date)
    amount = Column(Integer)
    pay_info = Column(String(20))
    dlv_id = Column(String(10), ForeignKey("DeliveryMan.dlv_id"))

# DeliveryMan 테이블 모델
class DeliveryMan(Base):
    __tablename__ = "DeliveryMan"
    __table_args__ = {"extend_existing": True}

    dlv_id = Column(String(10), primary_key=True)
    phone = Column(String(12))
    dlv_name = Column(String(20))
    vehicle = Column(String(20))
    dlv_address_si = Column(String(50))
