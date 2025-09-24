from sqlalchemy import Column, Uuid
import uuid


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
