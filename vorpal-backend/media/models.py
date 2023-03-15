from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class MediaFile(Base):
    __tablename__ = 'media_files'
    unique_id = Column(String, default=lambda: str(uuid.uuid4()), unique=True)
    file_path = Column(String, primary_key=True)
    file_size = Column(Integer)
    hash = Column(String)
    duration = Column(Float)
    bit_rate = Column(Integer)
    sample_rate = Column(Integer)
    channels = Column(Integer)
    format_name = Column(String)
    format_long_name = Column(String)
    scan_date = Column(DateTime)
    media_metadata = Column(JSON)  # Change the attribute name to media_metadata

    def to_dict(self):
        return {
            "unique_id": self.unique_id,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "hash": self.hash,
            "duration": self.duration,
            "bit_rate": self.bit_rate,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "format_name": self.format_name,
            "format_long_name": self.format_long_name,
            "scan_date": self.scan_date.isoformat() if self.scan_date else None,
            "media_metadata": self.media_metadata  # Update the dictionary key to media_metadata
        }

