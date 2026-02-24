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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.If not, see <http://www.gnu.org/licenses/>.

import os
import random
import unittest
import uuid

from mov_api import mov_get_log_message_with
from unittest_parametrize import ParametrizedTestCase, param, parametrize

from c2_treatment_nonmaleficence_valuator.change_parameters_handler import ChangeParametersHandler
from c2_treatment_nonmaleficence_valuator.change_parameters_payload import ChangeParametersPayload
from c2_treatment_nonmaleficence_valuator.message_service import MessageService
from c2_treatment_nonmaleficence_valuator.mov import MOV

PROPERTY_NAME_PARAMETERS = [
		param("age_range_weight"),
		param("ccd_weight"),
		param("maca_weight"),
		param("expected_survival_weight"),
		param("frail_VIG_weight"),
		param("clinical_risk_group_weight"),
		param("has_social_support_weight"),
		param("independence_at_admission_weight"),
		param("independence_instrumental_activities_weight"),
		param("has_advance_directives_weight"),
		param("is_competent_weight"),
		param("has_been_informed_weight"),
		param("is_coerced_weight"),
		param("has_cognitive_impairment_weight"),
		param("has_emocional_pain_weight"),
		param("discomfort_degree_weight")
	]

class TestChangeParametersHandler(ParametrizedTestCase):
    """Class to test the handler of the messages to change the component parameters."""

    @classmethod
    def setUpClass(cls):
        """Create the handler."""

        cls.message_service = MessageService()
        cls.mov = MOV(cls.message_service)
        cls.handler = ChangeParametersHandler(cls.message_service, cls.mov)
        cls.message_service.start_consuming_and_forget()

    @classmethod
    def tearDownClass(cls):
        """Stops the message service."""

        cls.mov.unregister_component()
        cls.message_service.close()

    def random_weight(self):
        """Generate a random weight value"""

        return random.randrange(0, 10000) / 10000.0

    def test_capture_bad_json_message_body(self):
        """Check that the handler can manage when the body is not a valid JSON"""

        parameters = {
            "is_competent_weight": f"BAD_VALUE {uuid.uuid4()}"
        }
        self.__assert_process_change_parameters('ERROR', parameters)

    def __assert_process_change_parameters(self, level: str, parameters: dict):
        """Check that the parameters are processed correctly.

        Parameters
        ----------
        level: str
            The expected level of the message when the parameters are changed.
        parameters: dict
            The parameters that were sent.
        """

        self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/control/parameters', parameters)
        mov_get_log_message_with(level, parameters)

    def test_change_parameters(self):
        """Check that the handler changes the parameters"""

        parameters = {
			"age_range_weight": self.random_weight(),
			"ccd_weight": self.random_weight(),
			"maca_weight": self.random_weight(),
			"expected_survival_weight": self.random_weight(),
			"frail_VIG_weight": self.random_weight(),
			"clinical_risk_group_weight": self.random_weight(),
			"has_social_support_weight": self.random_weight(),
			"independence_at_admission_weight": self.random_weight(),
			"independence_instrumental_activities_weight": self.random_weight(),
			"has_advance_directives_weight": self.random_weight(),
			"is_competent_weight": self.random_weight(),
			"has_been_informed_weight": self.random_weight(),
			"is_coerced_weight": self.random_weight(),
			"has_cognitive_impairment_weight": self.random_weight(),
			"has_emocional_pain_weight": self.random_weight(),
			"discomfort_degree_weight": self.random_weight()
		}
        self.__assert_process_change_parameters('INFO', parameters)
        for param_name in parameters:
            expected = str(parameters[param_name])
            env_property_name = param_name.upper()
            env_property = os.getenv(env_property_name)
            assert expected == env_property

    @parametrize("param_name", PROPERTY_NAME_PARAMETERS)
    def test_not_change_param_with_a_bad_value(self, param_name: str):
        """Check that the handler does not change a parameter when it is not valid"""

        bad_value = str(uuid.uuid4())
        parameters = {param_name: bad_value}
        self.__assert_process_change_parameters('ERROR', parameters)

    @parametrize("param_name", PROPERTY_NAME_PARAMETERS)
    def test_not_change_param_with_a_value_less_than_0(self, param_name: str):
        """Check that the handler does not change a parameter if the value is less than 0"""

        bad_value = -0.000001 - self.random_weight()
        parameters = {param_name: bad_value}
        self.__assert_process_change_parameters('ERROR', parameters)

    @parametrize("param_name", PROPERTY_NAME_PARAMETERS)
    def test_not_change_param_with_a_value_more_than_1(self, param_name: str):
        """Check that the handler does not change a parameter if the value is more than 1"""

        bad_value = self.random_weight() + 1.000000001
        parameters = {param_name: bad_value}
        self.__assert_process_change_parameters('ERROR', parameters)

    @parametrize("param_name", PROPERTY_NAME_PARAMETERS)
    def test_change_param(self, param_name: str):
        """Check that the handler changes a parameter"""

        value = self.random_weight()
        parameters = ChangeParametersPayload(**{param_name: value})
        self.__assert_process_change_parameters('INFO', parameters)
        expected = str(value)
        current = os.getenv(param_name.upper())
        assert expected == current


if __name__ == '__main__':
    unittest.main()
