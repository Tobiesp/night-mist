import uuid
from sqlalchemy import UUID, func

from app import SQL_DB

class BaseTable(SQL_DB.Model):
    id = SQL_DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = SQL_DB.Column(SQL_DB.DateTime(timezone=True), server_default=func.now())
    updated_at = SQL_DB.Column(SQL_DB.DateTime(timezone=True), onupdate=func.now())