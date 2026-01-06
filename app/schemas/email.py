from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str
