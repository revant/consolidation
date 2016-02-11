# Copyright (c) 2013, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)

def execute(filters=None):
	period_list = get_period_list(filters.fiscal_year, filters.periodicity, from_beginning=True)

	# TODO: Get company from consolidation
	# Get Asset, Liability and Equity Data for each company
	# Get Company Relations from consolidation
	# Make changes in Asset, Liability and Equity figures as per relations

	company_list = []
	consolidation = frappe.get_doc("Consolidation", filters.consolidation)
	for company in consolidation.organization:
		company_list.append(company.company)

	asset = get_data(company_list[0], "Asset", "Debit", period_list)
	liability = get_data(company_list[0], "Liability", "Credit", period_list)
	equity = get_data(company_list[0], "Equity", "Credit", period_list)
	provisional_profit_loss = get_provisional_profit_loss(asset, liability, equity,
		period_list, company_list[0])

	data = []
	data.extend(asset or [])
	data.extend(liability or [])
	data.extend(equity or [])
	if provisional_profit_loss:
		data.append(provisional_profit_loss)

	columns = get_columns(period_list)

	return columns, data

def get_provisional_profit_loss(asset, liability, equity, period_list, company):
	if asset and (liability or equity):
		provisional_profit_loss = {
			"account_name": "'" + _("Provisional Profit / Loss (Credit)") + "'",
			"account": None,
			"warn_if_negative": True,
			"currency": frappe.db.get_value("Company", company, "default_currency")
		}

		has_value = False

		for period in period_list:
			effective_liability = 0.0
			if liability:
				effective_liability += flt(liability[-2][period.key])
			if equity:
				effective_liability += flt(equity[-2][period.key])

			provisional_profit_loss[period.key] = flt(asset[-2][period.key]) - effective_liability

			if provisional_profit_loss[period.key]:
				has_value = True

		if has_value:
			return provisional_profit_loss
