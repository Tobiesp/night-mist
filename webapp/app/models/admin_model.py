import json
from app import ADMIN_KEY
from app.models import BASE
from app.models.base_db_model import BaseDBModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from cryptography.fernet import Fernet
import base64


class Admin(BaseDBModel, BASE):
    __tablename__ = 'admin'
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    store_value: Mapped[str] = mapped_column(nullable=True)
    salt: Mapped[str] = mapped_column(String(100), nullable=True)
    value_type: Mapped[str] = mapped_column(String(100), nullable=True)

    def __repr__(self):
        return '<Admin %r>' % self.key
    
    def _get_secret_key(self):
        bytes = base64.urlsafe_b64decode(ADMIN_KEY)
        diff = 32 - len(bytes)
        if diff > 0:
            if self.salt is None:
                self.salt = Fernet.generate_key()
            else:
                self.salt = base64.urlsafe_b64decode(self.salt)
            bytes += self.salt[:diff]
        return bytes
    
    @property
    def value(self) -> str:
        if self.value_type == 'dict':
            return json.loads(self.store_value)
        if self.value_type == 'list':
            return json.loads(self.store_value)
        if self.value_type == 'bool':
            return json.loads(self.store_value)
        if self.value_type == 'int':
            return json.loads(self.store_value)
        if self.value_type == 'secret':
            return self.secret
        return self.store_value
    
    @value.setter
    def value(self, value: str | bool | int | dict | list) -> None:
        if isinstance(value, dict):
            self.store_value = json.dumps(value)
            self.value_type = 'dict'
        elif isinstance(value, list):
            self.store_value = json.dumps(value)
            self.value_type = 'list'
        elif isinstance(value, bool):
            self.store_value = json.dumps(value)
            self.value_type = 'bool'
        elif isinstance(value, int):
            self.store_value = json.dumps(value)
            self.value_type = 'int'
        else:
            self.store_value = value
            self.value_type = 'string'
    
    @property
    def secret(self) -> str:
        cipher_suite = Fernet(self._get_secret_key())
        bytes = base64.b64decode(self.value)
        return cipher_suite.decrypt(bytes).decode()
    
    @property.setter
    def secret(self, value: str) -> None:  # noqa: F811
        cipher_suite = Fernet(self._get_secret_key())
        bytes = cipher_suite.encrypt(value.encode())
        self.value = base64.b64encode(bytes).decode()
        self.value_type = 'secret'