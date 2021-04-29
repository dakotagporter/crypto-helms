# Std Library Imports
from typing import List

# Third-party Imports
from fastapi import APIRouter

#Instantiate router
router = APIRouter()

## Possible sources of data:
# https://min-api.cryptocompare.com/
# https://futures-docs.poloniex.com/#general
# https://bravenewcoin.com/developers

## Refer to GitHub project board for discussion topics.

@router.get("/")
async def dummy_data() -> List[dict]:
    employees = [
        {"id": 1, "name": "John", "employee_id": 12345},
        {"id": 2, "name": "June", "employee_id": 67890}
    ]

    return employees
