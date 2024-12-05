from pydantic import BaseModel

class CreatePropertyRequest(BaseModel):
    value: float
    zip_code: str
    number: int
    buyer: "CreateBuyerRequest"

class CreateBuyerRequest(BaseModel):
    name: str
    credit_score: float
    wage: float

class CreatePropertyResponse(BaseModel):
    id: int

class DealBuyerResponse(BaseModel):
    id: int
    nome: str
    credit_score: float
    wage: float

class DealPropertyResponse(BaseModel):
    id: int
    zip_code: str
    number: int
    value: float
    public_place: str

class DealResponse(BaseModel):
    id: int
    status: str
    buyer: DealBuyerResponse
    property: DealPropertyResponse