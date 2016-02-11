# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Consolidation(Document):
	def validate(self):
		self.set_title()

	def set_title(self):
		for item in self.organization:
			if item.is_parent:
				self.consolidation_name = item.company
