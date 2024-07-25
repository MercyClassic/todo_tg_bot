import enum

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PriorityEnum(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class ToDo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(nullable=True)
    priority: Mapped[PriorityEnum] = mapped_column(
        ENUM(PriorityEnum, name='priorityenum', create_type=False),
        default=PriorityEnum.low.value,
    )
    is_active: Mapped[bool] = mapped_column(default=True)
