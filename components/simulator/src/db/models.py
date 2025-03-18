from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for all SQLAlchemy models
Base = declarative_base()

# Define the StartRecord model
class StartRecord(Base):
    __tablename__ = "start_record" # Specify the table name

    # Define the columns of the table
    id = Column(
        BigInteger,
        primary_key=True
    )
    connection_id = Column(
        String(255),
        nullable=False,
    )
    timestamp = Column(
        BigInteger,
        nullable=False,
    )
    response_time = Column(
        BigInteger,
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return a string representation of the StartRecord object"""
        return f"StartRecord(id={self.id}, start_time={self.consume_time})"


if __name__ == "__main__":
    from database import engine
    Base.metadata.create_all(engine) # Create the table in the database
