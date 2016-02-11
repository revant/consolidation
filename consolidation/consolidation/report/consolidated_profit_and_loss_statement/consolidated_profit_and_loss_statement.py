# Copyright (c) 2013, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)

def execute(filters=None):
	period_list = get_period_list(filters.fiscal_year, filters.periodicity)

	# TODO: Get company from consolidation
	# Get Asset, Liability and Equity Data for each company
	# Get Company Relations from consolidation
	# Make changes in Asset, Liability and Equity figures as per relations

	company_list = []
	consolidation = frappe.get_doc("Consolidation", filters.consolidation)
	for company in consolidation.organization:
		company_list.append(company.company)

	income = get_data(company_list[0], "Income", "Credit", period_list, ignore_closing_entries=True)
	expense = get_data(company_list[0], "Expense", "Debit", period_list, ignore_closing_entries=True)
	net_profit_loss = get_net_profit_loss(income, expense, period_list, company_list[0])

	data = []
	data.extend(income or [])
	data.extend(expense or [])
	if net_profit_loss:
		data.append(net_profit_loss)

	columns = get_columns(filters.periodicity, period_list, company=company_list[0])

	return columns, data

def get_net_profit_loss(income, expense, period_list, company):
	if income and expense:
		net_profit_loss = {
			"account_name": "'" + _("Net Profit / Loss") + "'",
			"account": None,
			"warn_if_negative": True,
			"currency": frappe.db.get_value("Company", company, "default_currency")
		}

		for period in period_list:
			net_profit_loss[period.key] = flt(income[-2][period.key] - expense[-2][period.key], 3)

		return net_profit_loss
