from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, BigInteger, Boolean
from db import Base


class UserItem(Base):
    __tablename__ = "user_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    appid: Mapped[int] = mapped_column(Integer)
    market_hash_name: Mapped[str] = mapped_column(String(255))
    target_price: Mapped[float] = mapped_column(Float)  # цена, при которой уведомляем
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
