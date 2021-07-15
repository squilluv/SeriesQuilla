from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///SquillSeries.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    predefiend = Column(Boolean, nullable=False, default=False)
    series = relationship('Series', cascade='all,delete', back_populates='groups')

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, group_name):
        group = cls(name=group_name)
        session.add(group)
        session.commit()
        return group

    @classmethod
    def find_by_group_name(cls, group_name):
        return session.query(cls).filter(cls.name.ilike(f'%{group_name}%'))

    @classmethod
    def find_by_series_name(cls, series_name):
        return session.query(cls).join(Series).filter(Series.name.ilike(f'%{series_name}%'))

    @classmethod
    def show_all(cls):
        return session.query(cls).join(Series).all()
    @classmethod
    def del_by_id(cls, group_id):
        group = session.query(cls).filter_by(id=group_id).first()
        if group:
            session.delete(group)
            session.commit()
            return True
        return False


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rate = Column(Integer, default=0)
    group_id = Column(Integer, ForeignKey('groups.id'))
    groups = relationship('Groups', back_populates='series')

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, series_name, group):
        series = cls(name=series_name, groups=group)
        session.add(series)
        session.commit()
        return series


Base.metadata.create_all(engine)