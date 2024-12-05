from pydantic import BaseModel, Field

class CreatePropertyRequest(BaseModel):
    value: float = Field(ge=0)
    buyer: "CreateBuyerRequest"

class CreateBuyerRequest(BaseModel):
    credit_score: float = Field(alias="creditScore", ge=0, le=1000)
    estimated_income: float = Field(alias="estimatedIncome", ge=0)

class CreatePropertyResponse(BaseModel):
    id: int

class DealBuyerResponse(BaseModel):
    id: int
    credit_score: float = Field(serialization_alias="creditScore")
    estimated_income: float = Field(serialization_alias="estimatedIncome")

class DealPropertyResponse(BaseModel):
    id: int
    value: float

class DealResponse(BaseModel):
    id: int
    status: str
    buyer: DealBuyerResponse
    property: DealPropertyResponse