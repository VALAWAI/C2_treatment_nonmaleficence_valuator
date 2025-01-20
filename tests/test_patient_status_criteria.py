#
# This file is part of the C2_treatment_nonmaleficence_valuator distribution
# (https://github.com/VALAWAI/C2_treatment_nonmaleficence_valuator).
# Copyright (c) 2022-2026 VALAWAI (https://valawai.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.

import math
import unittest

from c2_treatment_nonmaleficence_valuator.patient_status_criteria import (
	AgeRangeOption,
	BarthelIndex,
	ClinicalRiskGroupOption,
	CognitiveImpairmentLevel,
	DiscomfortDegree,
	PatientStatusCriteria,
	SPICT_Scale,
	SurvivalOptions,
)


class TestPatientStatusCriteria(unittest.TestCase):
	"""Class to test the patient status criteria."""

	def setUp(self):
		"""Create the criteria for the test."""

		self.criteria = PatientStatusCriteria()

	def test_normalized_age_range(self):
		"""Check that is calculated the normalized age range."""

		self.criteria.age_range = None
		expected = 0.0
		normalized = self.criteria.normalized_age_range()
		assert normalized == expected

		for value in AgeRangeOption:

			self.criteria.age_range = value
			expected += 0.1
			normalized = self.criteria.normalized_age_range()
			assert math.isclose(normalized, expected), f"Unexpected normlaized for {value.name}"


	def test_normalized_ccd(self):
		"""Check that is calculated the normalized ccd."""

		self.criteria.ccd = None
		expected = 0.0
		normalized = self.criteria.normalized_ccd()
		assert normalized == expected

		self.criteria.ccd = True
		normalized = self.criteria.normalized_ccd()
		assert normalized == expected

		expected = 1.0
		self.criteria.ccd = False
		normalized = self.criteria.normalized_ccd()
		assert normalized == expected

	def test_normalized_maca(self):
		"""Check that is calculated the normalized maca."""

		self.criteria.maca = None
		expected = 0.0
		normalized = self.criteria.normalized_maca()
		assert normalized == expected

		self.criteria.maca = True
		normalized = self.criteria.normalized_maca()
		assert normalized == expected

		expected = 1.0
		self.criteria.maca = False
		normalized = self.criteria.normalized_maca()
		assert normalized == expected

	def test_normalized_expected_survival(self):
		"""Check that is calculated the normalized expected_survival."""

		self.criteria.expected_survival = None
		expected = 0.0
		normalized = self.criteria.normalized_expected_survival()
		assert normalized == expected

		for value in SurvivalOptions:

			self.criteria.expected_survival = value
			expected = 0.0 if value != SurvivalOptions.MORE_THAN_12_MONTHS else 1.0
			normalized = self.criteria.normalized_expected_survival()
			assert normalized == expected

	def test_normalized_frail_vig(self):
		"""Check that is calculated the normalized frail VIG."""

		self.criteria.frail_VIG = None
		expected = 0.0
		normalized = self.criteria.normalized_frail_vig()
		assert normalized == expected

		expected = 1.0
		for value in SPICT_Scale:

			self.criteria.frail_VIG = value
			normalized = self.criteria.normalized_frail_vig()
			assert math.isclose(normalized, expected), f"Unexpected normlaized for {value.name}"
			expected = max(0,expected-0.5)

	def test_normalized_clinical_risk_group(self):
		"""Check that is calculated the normalized clinical risk group."""

		self.criteria.clinical_risk_group = None
		expected = 0.0
		normalized = self.criteria.normalized_clinical_risk_group()
		assert normalized == expected

		expected = 1.0
		for value in ClinicalRiskGroupOption:

			self.criteria.clinical_risk_group = value
			normalized = self.criteria.normalized_clinical_risk_group()
			assert math.isclose(normalized, expected), f"Unexpected normlaized for {value.name}"
			expected = max(0,expected-0.5)

	def test_normalized_has_social_support(self):
		"""Check that is calculated the normalized has social support."""

		self.criteria.has_social_support = None
		expected = 0.0
		normalized = self.criteria.normalized_has_social_support()
		assert normalized == expected

		self.criteria.has_social_support = True
		normalized = self.criteria.normalized_has_social_support()
		assert normalized == expected

		expected = 1.0
		self.criteria.has_social_support = False
		normalized = self.criteria.normalized_has_social_support()
		assert normalized == expected

	def test_normalized_independence_at_admission(self):
		"""Check that is calculated the normalized independence at admission."""

		self.criteria.independence_at_admission = None
		expected = 0.0
		normalized = self.criteria.normalized_independence_at_admission()
		assert normalized == expected

		expected = [0.1, 0.4, 0.75, 0.95, 1.0, 0.0]
		for index,value in enumerate(BarthelIndex):

			self.criteria.independence_at_admission = value
			normalized = self.criteria.normalized_independence_at_admission()
			assert math.isclose(normalized, expected[index]), f"Unexpected normlaized for {value.name}"

	def test_normalized_independence_instrumental_activities(self):
		"""Check that is calculated the independence instrumental activities."""

		self.criteria.independence_instrumental_activities = None
		expected = 0.0
		normalized = self.criteria.normalized_independence_instrumental_activities()
		assert normalized == expected

		expected = [0.0, 0.13, 0.26, 0.38, 0.5, 0.63, 0.75, 0.88, 1.0]
		for index,value in enumerate(expected):

			self.criteria.independence_instrumental_activities = index
			normalized = self.criteria.normalized_independence_instrumental_activities()
			assert math.isclose(normalized, value), f"Unexpected normlaized for {index}"

	def test_normalized_has_advance_directives(self):
		"""Check that is calculated the normalized has advance directives."""

		self.criteria.has_advance_directives = None
		expected = 0.0
		normalized = self.criteria.normalized_has_advance_directives()
		assert normalized == expected

		self.criteria.has_advance_directives = True
		normalized = self.criteria.normalized_has_advance_directives()
		assert normalized == expected

		expected = 1.0
		self.criteria.has_advance_directives = False
		normalized = self.criteria.normalized_has_advance_directives()
		assert normalized == expected

	def test_normalized_is_competent(self):
		"""Check that is calculated the normalized is_competent."""

		self.criteria.is_competent = None
		expected = 0.0
		normalized = self.criteria.normalized_is_competent()
		assert normalized == expected

		self.criteria.is_competent = True
		normalized = self.criteria.normalized_is_competent()
		assert normalized == expected

		expected = 1.0
		self.criteria.is_competent = False
		normalized = self.criteria.normalized_is_competent()
		assert normalized == expected

	def test_normalized_has_been_informed(self):
		"""Check that is calculated the normalized has_been_informed."""

		self.criteria.has_been_informed = None
		expected = 0.0
		normalized = self.criteria.normalized_has_been_informed()
		assert normalized == expected

		self.criteria.has_been_informed = True
		normalized = self.criteria.normalized_has_been_informed()
		assert normalized == expected

		expected = 1.0
		self.criteria.has_been_informed = False
		normalized = self.criteria.normalized_has_been_informed()
		assert normalized == expected

	def test_normalized_is_coerced(self):
		"""Check that is calculated the normalized is_coerced."""

		self.criteria.is_coerced = None
		expected = 0.0
		normalized = self.criteria.normalized_is_coerced()
		assert normalized == expected

		self.criteria.is_coerced = True
		normalized = self.criteria.normalized_is_coerced()
		assert normalized == expected

		expected = 1.0
		self.criteria.is_coerced = False
		normalized = self.criteria.normalized_is_coerced()
		assert normalized == expected

	def test_normalized_has_cognitive_impairment(self):
		"""Check that is calculated the normalized frail VIG."""

		self.criteria.has_cognitive_impairment = None
		expected = 0.0
		normalized = self.criteria.normalized_has_cognitive_impairment()
		assert normalized == expected

		expected = 1.0
		for value in CognitiveImpairmentLevel:

			self.criteria.has_cognitive_impairment = value
			normalized = self.criteria.normalized_has_cognitive_impairment()
			assert math.isclose(normalized, expected), f"Unexpected normlaized for {value.name}"
			expected = max(0,expected-0.5)

	def test_normalized_has_emocional_pain(self):
		"""Check that is calculated the normalized has_emocional_pain."""

		self.criteria.has_emocional_pain = None
		expected = 0.0
		normalized = self.criteria.normalized_has_emocional_pain()
		assert normalized == expected

		self.criteria.has_emocional_pain = True
		normalized = self.criteria.normalized_has_emocional_pain()
		assert normalized == expected

		expected = 1.0
		self.criteria.has_emocional_pain = False
		normalized = self.criteria.normalized_has_emocional_pain()
		assert normalized == expected

	def test_normalized_discomfort_degree(self):
		"""Check that is calculated the normalized discomfort degree."""

		self.criteria.discomfort_degree = None
		expected = 0.0
		normalized = self.criteria.normalized_discomfort_degree()
		assert normalized == expected

		expected = 1.0
		for value in DiscomfortDegree:

			self.criteria.discomfort_degree = value
			normalized = self.criteria.normalized_discomfort_degree()
			assert math.isclose(normalized, expected), f"Unexpected normlaized for {value.name}"
			expected = max(0,expected-0.5)


if __name__ == '__main__':
    unittest.main()
