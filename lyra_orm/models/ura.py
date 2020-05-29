from lyra_orm.config import session
from lyra_orm.config import Base
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Text,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.dialects.mysql import BOOLEAN
from sqlalchemy.orm import relationship, backref

ura_transcription = Table(
    "ura_transcription",
    Base.metadata,
    Column("ura_id", Integer, ForeignKey("ura.id")),
    Column("transcription_id", Integer, ForeignKey("transcription.id")),
)


class Ura(Base):
    __tablename__ = "ura"
    id = Column(Integer, primary_key=True)
    number = Column(String(20))
    label = Column(String(50), unique=True)
    description = Column(String(200))
    active = Column(BOOLEAN, default=True)
    alarm = relationship("UraAlarm", backref="ura", uselist=False)
    last_alarm_time = Column(DateTime())
    alarmed_times = Column(Integer())
    transcriptions = relationship(
        "Transcription",
        secondary=ura_transcription,
        backref=backref("uras", lazy="dynamic"),
    )

    def __str__(self):
        return self.label

    @classmethod
    def find_all(cls, actives=True):
        if not actives:
            return session.query(cls).all()

        return session.query(cls).filter_by(active=True).all()

    @classmethod
    def find_by_number(cls, number):
        return session.query(cls).filter_by(number=number).first()

    @classmethod
    def get_uras_numbers(cls, actives=True):
        return [u.number for u in Ura.find_all(actives=actives)]

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()


class Transcription(Base):
    __tablename__ = "transcription"
    id = Column(Integer, primary_key=True)
    label = Column(String(30), unique=True)
    description = Column(String(200))
    transcription = Column(String(255))

    def __str__(self):
        return self.label

    @classmethod
    def find_by_label(cls, label):
        return session.query(cls).filter_by(label=label).first()

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()


class UraAlarm(Base):
    __tablename__ = "ura_alarm"
    id = Column(Integer, primary_key=True)
    label = Column(String(30), unique=True)
    description = Column(String(200))
    minimum_failures = Column(Integer())
    hours_between_alarms = Column(Integer())  # hours
    ura_id = Column(Integer(), ForeignKey("ura.id"))

    def __str__(self):
        return self.label

    @classmethod
    def find_by_label(cls, label):
        return session.query(cls).filter_by(label=label).first()

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
        session.close()
