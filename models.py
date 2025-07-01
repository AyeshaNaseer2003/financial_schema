from typing import Optional, List
from pydantic import BaseModel


class IncomeStatement(BaseModel):
    revenue: Optional[float]
    cost_of_goods_sold: Optional[float]
    gross_profit: Optional[float]
    research_and_development_expenses: Optional[float]
    sg_and_a_expenses: Optional[float]
    other_operating_income_or_expenses: Optional[float]
    operating_expenses: Optional[float]
    operating_income: Optional[float]
    total_non_operating_income_expense: Optional[float]
    pre_tax_income: Optional[float]
    income_taxes: Optional[float]
    income_after_taxes: Optional[float]
    income_from_continuous_operations: Optional[float]
    net_income: Optional[float]
    ebitda: Optional[float]
    ebit: Optional[float]
    basic_shares_outstanding: Optional[float]
    shares_outstanding: Optional[float]
    basic_eps: Optional[float]
    eps_earnings_per_share: Optional[float]


class BalanceSheet(BaseModel):
    cash_on_hand: Optional[float]
    receivables: Optional[float]
    pre_paid_expenses: Optional[float]
    total_current_assets: Optional[float]
    property_plant_and_equipment: Optional[float]
    goodwill_and_intangible_assets: Optional[float]
    other_long_term_assets: Optional[float]
    total_long_term_assets: Optional[float]
    total_assets: Optional[float]
    total_current_liabilities: Optional[float]
    long_term_debt: Optional[float]
    other_non_current_liabilities: Optional[float]
    total_long_term_liabilities: Optional[float]
    total_liabilities: Optional[float]
    retained_earnings_accumulated_deficit: Optional[float]
    comprehensive_income: Optional[float]
    share_holder_equity: Optional[float]
    total_liabilities_and_share_holders_equity: Optional[float]


class CashFlow(BaseModel):
    net_income_loss: Optional[float]
    total_depreciation_and_amortization_cash_flow: Optional[float]
    other_non_cash_items: Optional[float]
    total_non_cash_items: Optional[float]
    change_in_accounts_receivable: Optional[float]
    change_in_accounts_payable: Optional[float]
    change_in_assets_liabilities: Optional[float]
    total_change_in_assets_liabilities: Optional[float]
    cash_flow_from_operating_activities: Optional[float]
    net_change_in_property_plant_and_equipment: Optional[float]
    net_acquisitions_divestitures: Optional[float]
    net_change_in_short_term_investments: Optional[float]
    net_change_in_long_term_investments: Optional[float]
    net_change_in_investments_total: Optional[float]
    investing_activities_other: Optional[float]
    cash_flow_from_investing_activities: Optional[float]
    net_long_term_debt: Optional[float]
    net_current_debt: Optional[float]
    debt_issuance_retirement_net_total: Optional[float]
    net_common_equity_issued_repurchased: Optional[float]
    net_total_equity_issued_repurchased: Optional[float]
    financial_activities_other: Optional[float]
    cash_flow_from_financial_activities: Optional[float]
    net_cash_flow: Optional[float]
    stock_based_compensation: Optional[float]


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
