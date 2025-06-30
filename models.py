from typing import Optional, List
from pydantic import BaseModel


class IncomeStatement(BaseModel):
    Revenue: Optional[float]
    Cost_Of_Goods_Sold: Optional[float]
    Gross_Profit: Optional[float]
    Research_And_Development_Expenses: Optional[float]
    SG_and_A_Expenses: Optional[float]
    Other_Operating_Income_Or_Expenses: Optional[float]
    Operating_Expenses: Optional[float]
    Operating_Income: Optional[float]
    Total_Non_Operating_Income_Expense: Optional[float]
    Pre_Tax_Income: Optional[float]
    Income_Taxes: Optional[float]
    Income_After_Taxes: Optional[float]
    Income_From_Continuous_Operations: Optional[float]
    Net_Income: Optional[float]
    EBITDA: Optional[float]
    EBIT: Optional[float]
    Basic_Shares_Outstanding: Optional[float]
    Shares_Outstanding: Optional[float]
    Basic_EPS: Optional[float]
    EPS_Earnings_Per_Share: Optional[float]


class BalanceSheet(BaseModel):
    Cash_On_Hand: Optional[float]
    Receivables: Optional[float]
    Pre_Paid_Expenses: Optional[float]
    Total_Current_Assets: Optional[float]
    Property_Plant_And_Equipment: Optional[float]
    Goodwill_And_Intangible_Assets: Optional[float]
    Other_Long_Term_Assets: Optional[float]
    Total_Long_Term_Assets: Optional[float]
    Total_Assets: Optional[float]
    Total_Current_Liabilities: Optional[float]
    Long_Term_Debt: Optional[float]
    Other_Non_Current_Liabilities: Optional[float]
    Total_Long_Term_Liabilities: Optional[float]
    Total_Liabilities: Optional[float]
    Retained_Earnings_Accumulated_Deficit: Optional[float]
    Comprehensive_Income: Optional[float]
    Share_Holder_Equity: Optional[float]
    Total_Liabilities_And_Share_Holders_Equity: Optional[float]


class CashFlow(BaseModel):
    Net_Income_Loss: Optional[float]
    Total_Depreciation_And_Amortization_Cash_Flow: Optional[float]
    Other_Non_Cash_Items: Optional[float]
    Total_Non_Cash_Items: Optional[float]
    Change_In_Accounts_Receivable: Optional[float]
    Change_In_Accounts_Payable: Optional[float]
    Change_In_Assets_Liabilities: Optional[float]
    Total_Change_In_Assets_Liabilities: Optional[float]
    Cash_Flow_From_Operating_Activities: Optional[float]
    Net_Change_In_Property_Plant_And_Equipment: Optional[float]
    Net_Acquisitions_Divestitures: Optional[float]
    Net_Change_In_Short_term_Investments: Optional[float]
    Net_Change_In_Long_Term_Investments: Optional[float]
    Net_Change_In_Investments_Total: Optional[float]
    Investing_Activities_Other: Optional[float]
    Cash_Flow_From_Investing_Activities: Optional[float]
    Net_Long_Term_Debt: Optional[float]
    Net_Current_Debt: Optional[float]
    Debt_Issuance_Retirement_Net_Total: Optional[float]
    Net_Common_Equity_Issued_Repurchased: Optional[float]
    Net_Total_Equity_Issued_Repurchased: Optional[float]
    Financial_Activities_Other: Optional[float]
    Cash_Flow_From_Financial_Activities: Optional[float]
    Net_Cash_Flow: Optional[float]
    Stock_Based_Compensation: Optional[float]


class FinancialYear(BaseModel):
    year: int
    income_statement: IncomeStatement
    balance_sheet: BalanceSheet
    cash_flow: CashFlow


class Company(BaseModel):
    name: str
    financials: List[FinancialYear]


class FinancialReport(BaseModel):
    title: str
    company: Company
