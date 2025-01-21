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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import math
import unittest

from json_resources import load_treatment_json

from c2_treatment_nonmaleficence_valuator.nonmaleficence_valuator import NonmaleficenceValuator
from c2_treatment_nonmaleficence_valuator.patient_status_criteria import PatientStatusCriteria
from c2_treatment_nonmaleficence_valuator.treatment_payload import TreatmentPayload


class TestNonmaleficenceValuator(unittest.TestCase):
	"""Class to test the nonmaleficence valuator
	"""

	def setUp(self):
		"""Create the valuator.
		"""
		self.valuator = NonmaleficenceValuator(
				age_range_weight=0.013,
				ccd_weight=0.026,
				maca_weight=0.039,
				expected_survival_weight=0.238,
				frail_VIG_weight=0.079,
				clinical_risk_group_weight=0.013,
				has_social_support_weight=0.0,
				independence_at_admission_weight=0.158,
				independence_instrumental_activities_weight=0.158,
				has_advance_directives_weight=0.026,
				is_competent_weight=0.0,
				has_been_informed_weight=0.0,
				is_coerced_weight=0.0,
				has_cognitive_impairment_weight=0.026,
				has_emocional_pain_weight=0.0,
				discomfort_degree_weight=0.224
			)


	def test_align_nonmaleficence(self):
		"""Test calculate alignment for a treatment
		"""

		treatment = TreatmentPayload(**load_treatment_json())
		alignment = self.valuator.align_nonmaleficence(treatment)
		assert math.isclose(alignment, 0.24644), 'Unexpected treatment nonmaleficence alignment value'

	def test_align_nonmaleficence_for_treatment_without_expected_status(self):
		"""Test calculate alignment with an empty treatment
		"""

		treatment = TreatmentPayload(**load_treatment_json())
		treatment.expected_status = None
		alignment = self.valuator.align_nonmaleficence(treatment)
		assert math.isclose(alignment, 0.0), 'Unexpected treatment nonmaleficence alignment value'

	def test_align_nonmaleficence_for_treatment_with_empty_expected_status(self):
		"""Test calculate alignment with an empty treatment
		"""

		treatment = TreatmentPayload(**load_treatment_json())
		treatment.expected_status = PatientStatusCriteria()
		alignment = self.valuator.align_nonmaleficence(treatment)
		assert math.isclose(alignment, -0.48109999999999997), 'Unexpected treatment nonmaleficence alignment value'

if __name__ == '__main__':
    unittest.main()
