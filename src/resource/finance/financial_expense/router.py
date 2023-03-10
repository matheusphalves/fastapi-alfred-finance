from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database.database import database_conector
from src.database.models import FinancialExpense, FinancialExpenseEntry
from src.resource.finance.financial_expense.repository import FinancialExpenseRepository
from src.resource.finance.financial_expense.schemas import FinancialExpenseResponse, FinancialExpenseRequest, \
    FinancialExpenseUpdateRequest
from src.resource.finance.financial_expense_entry.schemas import FinancialExpenseEntryResponse

financial_expenses_router = APIRouter(prefix="/api/financial-expenses", tags=["Financial Expenses"])

financial_expense_repository = FinancialExpenseRepository()


@financial_expenses_router.post(path="", response_model=FinancialExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create(request: FinancialExpenseRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_expense = financial_expense_repository.save(db, FinancialExpense(**request.dict()))
    if financial_expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialExpenseResponse.from_orm(financial_expense)


@financial_expenses_router.put(path="", response_model=FinancialExpenseResponse, status_code=status.HTTP_200_OK)
async def update(request: FinancialExpenseUpdateRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_expense = financial_expense_repository.update(db, FinancialExpense(**request.dict()))
    if financial_expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialExpenseResponse.from_orm(financial_expense)


@financial_expenses_router.get(path="", response_model=List[FinancialExpenseResponse])
async def find_all(db: Session = Depends(database_conector.get_database_session)):
    financial_expenses = financial_expense_repository.find_all(db)
    return [FinancialExpenseResponse.from_orm(financial_expense) for financial_expense in financial_expenses]


@financial_expenses_router.delete(path="/{financial_expense_id}")
async def delete(financial_expense_id: int, db: Session = Depends(database_conector.get_database_session)):
    financial_expense_repository.delete_by_id(db, financial_expense_id)


@financial_expenses_router.get(path="/{financial_expense_id}/financial-expense-entries")
async def get_financial_expense_entries_by_financial_expense(financial_expense_id: int,
                                         db: Session = Depends(database_conector.get_database_session)):
    financial_expense_entries = financial_expense_repository.get_related_entries(db, financial_expense_id,
                                                                                 FinancialExpenseEntry,
                                                                                 "financial_expense_id")
    return [FinancialExpenseEntryResponse.from_orm(financial_expense_entry) for financial_expense_entry in
            financial_expense_entries]
