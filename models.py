from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import yadisk


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
    def show_groups(cls):
        return session.query(cls).all()

    @classmethod
    def del_group_by_id(cls, group_id):
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
    year = Column(String)
    raiting_kp = Column(Integer)
    raiting_imdb = Column(Integer)
    kinopoisk_id = Column(Integer)
    genres = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    groups = relationship('Groups', back_populates='series')

    def __str__(self):
        return self.name

    @classmethod
    def show_series_by_id(cls, group_id):
        return session.query(cls).filter_by(group_id=group_id).all()

    @classmethod
    def add_series(cls, series_name, group_name, kinopoisk_id_, year_, raiting_imdb_, raiting_kp_, genres_):
        if group_name == 0:
            if cls.check_serial(series_name, year_) == 0:
                group = session.query(Groups).filter_by(id=1)[0]
                series = cls(name=series_name,
                             groups=group,
                             kinopoisk_id=kinopoisk_id_,
                             year=year_,
                             raiting_imdb=raiting_imdb_,
                             raiting_kp=raiting_kp_,
                             genres=genres_)
                session.add(series)
                session.commit()
                return series
        else:
            group = session.query(Groups).filter(Groups.name.like(f'{group_name}'))
            series = cls(name=series_name, groups=group[0])
            session.add(series)
            session.commit()
            return series

    @classmethod
    def del_series_by_id(cls, series_id):
        series = session.query(cls).filter_by(id=series_id).first()
        if series:
            session.delete(series)
            session.commit()
            return True
        return False

    @classmethod
    def check_serial(cls, series_name, year):
        return len(session.query(cls).filter_by(name=series_name, year=year).all())


class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)

Base.metadata.create_all(engine)