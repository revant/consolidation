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

	parent_asset = get_data(filters.company, "Asset", "Debit", period_list, only_current_fiscal_year=False)
	parent_liability = get_data(filters.company, "Liability", "Credit", period_list, only_current_fiscal_year=False)
	parent_equity = get_data(filters.company, "Equity", "Credit", period_list, only_current_fiscal_year=False)
	parent_provisional_profit_loss = get_provisional_profit_loss(parent_asset, parent_liability, parent_equity, period_list, filters.company)

	company_doc = frappe.get_doc("Company", filters.company)
	no_of_children = len(company_doc.children)
	consolidated_asset, consolidated_liability, consolidated_equity, consolidated_provisional_profit_loss = [], [], [], []
	a, l, e, ppl = [], [], [], []

	for i in xrange(no_of_children):
		a = get_data(company_doc.children[i].company, "Asset", "Debit", period_list, only_current_fiscal_year=False)
		for p, c in zip(parent_asset, a):
			if p.get("account_name") == c.get("account_name"):
				# Add Accounts and add to consolidated_asset list
				for i, j in zip(p,c):
					if c[j]:
						p[i] = c[j]
				consolidated_asset.append(p)
			else:
				consolidated_asset.append(p)
				consolidated_asset.append(c)

		# l = get_data(company_doc.children[i], "Liability", "Credit", period_list, only_current_fiscal_year=False)
		# e = get_data(company_doc.children[i], "Equity", "Credit", period_list, only_current_fiscal_year=False)
		# ppl = get_provisional_profit_loss(a, l, e,
		# 	period_list, company_doc.children[i])

	asset = consolidated_asset if filters.consolidated else parent_asset
	liability = parent_liability
	equity = parent_equity
	provisional_profit_loss = parent_provisional_profit_loss

	data = []
	data.extend(asset or [])
	data.extend(liability or [])
	data.extend(equity or [])
	if provisional_profit_loss:
		data.append(provisional_profit_loss)

	columns = get_columns(filters.periodicity, period_list)

	return columns, data

def get_provisional_profit_loss(asset, liability, equity, period_list, company):
	if asset and (liability or equity):
		total=0
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

			total += flt(provisional_profit_loss[period.key])
			provisional_profit_loss["total"] = total

		if has_value:
			return provisional_profit_loss
