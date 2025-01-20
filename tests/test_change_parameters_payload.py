#
# This file is part of the C2_change_parameters_nonmaleficence_valuator distribution
# (https://github.com/VALAWAI/C2_change_parameters_nonmaleficence_valuator).
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

from json_resources import load_change_parameters_json
from pydantic import ValidationError

from c2_treatment_nonmaleficence_valuator.change_parameters_payload import ChangeParametersPayload


class TestChangeParametersPayload(unittest.TestCase):
	"""Class to test the change_parameters
	"""


	def test_load_json(self):
		"""Test can obtain a change_parameters from a json"""

		json_dict = load_change_parameters_json()
		change_parameters = ChangeParametersPayload(**json_dict)
		assert math.isclose(change_parameters.age_range_weight,0.1)
		assert math.isclose(change_parameters.ccd_weight, 0.2)
		assert math.isclose(change_parameters.maca_weight, 0.3)
		assert math.isclose(change_parameters.expected_survival_weight, 0.4)
		assert math.isclose(change_parameters.frail_VIG_weight, 0.5)
		assert math.isclose(change_parameters.clinical_risk_group_weight, 0.6)
		assert math.isclose(change_parameters.has_social_support_weight, 0.7)
		assert math.isclose(change_parameters.independence_at_admission_weight, 0.8)
		assert math.isclose(change_parameters.independence_instrumental_activities_weight, 0.9)
		assert math.isclose(change_parameters.has_advance_directives_weight, 0.11)
		assert math.isclose(change_parameters.is_competent_weight, 0.12)
		assert math.isclose(change_parameters.has_been_informed_weight, 0.13)
		assert math.isclose(change_parameters.is_coerced_weight, 0.14)
		assert math.isclose(change_parameters.has_cognitive_impairment_weight, 0.15)
		assert math.isclose(change_parameters.has_emocional_pain_weight, 0.16)
		assert math.isclose(change_parameters.discomfort_degree_weight, 0.17)

	def test_allow_define_empty_change_parameters(self):
		"""Test can create an empty change_parameters"""

		change_parameters = ChangeParametersPayload()
		assert change_parameters is not None

	def test_load_empty_json(self):
		"""Test can not load a change parameters payload from an empty json"""

		change_parameters = ChangeParametersPayload()
		assert change_parameters is not None

	def test_fail_load_change_parameters_without_bad_field_value(self):
		"""Test can not load a change_parameters without identifier"""

		error = False
		try:

			json_value = load_change_parameters_json()
			json_value['age_range_weight'] = "Bad value"
			payload = ChangeParametersPayload(**json_value)
			assert payload is None

		except ValidationError:
			error = True

		# Can load a change parameters without a bad value
		assert error


if __name__ == '__main__':
    unittest.main()
