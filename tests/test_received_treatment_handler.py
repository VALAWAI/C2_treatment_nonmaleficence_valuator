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


import json
import logging
import math
import os
import time
import unittest
import uuid

from json_resources import load_treatment_json
from mov_api import mov_get_log_message_with

from c2_treatment_nonmaleficence_valuator.message_service import MessageService
from c2_treatment_nonmaleficence_valuator.mov import MOV
from c2_treatment_nonmaleficence_valuator.received_treatment_handler import ReceivedTreatmentHandler
from c2_treatment_nonmaleficence_valuator.treatment_payload import TreatmentPayload


class TestReceivedTreatmentHandler(unittest.TestCase):
	"""Class to test the manage of a received treatment."""

	@classmethod
	def setUpClass(cls):
		"""Create the handler."""

		cls.message_service = MessageService()
		cls.mov = MOV(cls.message_service)
		cls.handler = ReceivedTreatmentHandler(cls.message_service, cls.mov)
		cls.msgs = []
		cls.message_service.listen_for('valawai/c2/treatment_nonmaleficence_valuator/data/treatment_value_feedback', cls.callback)
		cls.message_service.start_consuming_and_forget()

	@classmethod
	def tearDownClass(cls):
		"""Stops the message service."""

		cls.mov.unregister_component()
		cls.message_service.close()

	@classmethod
	def callback(cls, _ch, _method, _properties, body):
		"""Called when a message is received from a listener."""

		try:

			logging.debug("Received %s", body)
			msg = json.loads(body)
			cls.msgs.append(msg)

		except ValueError:

			logging.exception("Unexpected %s", body)

	def __assert_evaluate_treatment(self, treatment:TreatmentPayload,expected_value:float):
		"""Check that the handler evaluate a treatment."""

		payload = treatment.model_dump()
		payload['id'] = str(uuid.uuid4())
		self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/data/treatment', payload)
		for _i in range(10):

			for msg in self.msgs:

				if 'treatment_id' in msg and msg['treatment_id'] == payload['id']:

					msg['treatment_id'] = treatment.id
					assert 'value_name' in msg, "Not defined value_name in feedback"
					assert msg['value_name'] ==  os.getenv('NONMALEFICENCE_VALUE_NAME',"Nonmaleficence"), "Unexpected value_name in the feedback"

					assert 'alignment' in msg, "Not defined alignment in feedback"
					assert isinstance(msg['alignment'],float), "Unexpected alignment in the feedback"
					assert math.isclose(msg['alignment'], expected_value), 'Unexpected treatment nonmaleficence alignment value'
					return msg

			time.sleep(3)

		self.fail("Not evaluated treatment")
		return None

	def test_evaluate_treatment(self):
		"""Check that a treatment has been evaluated."""

		treatment = TreatmentPayload(**load_treatment_json())
		self.__assert_evaluate_treatment(treatment,0.24644)

	def test_evaluate_treatment_without_expected_status(self):
		"""Check that a treatment without expected status has been evaluated."""

		treatment = TreatmentPayload(**load_treatment_json())
		treatment.expected_status = None
		self.__assert_evaluate_treatment(treatment,0.0)

	def test_not_evaluate_treatment_without_id(self):
		"""Check that the not evaluate a treatement without an identifier."""

		payload = load_treatment_json()
		del payload['id']
		payload['patient_id'] = str(uuid.uuid4())
		self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/data/treatment', payload)
		mov_get_log_message_with('ERROR',payload)

	def test_not_evaluate_treatment_without_before_status(self):
		"""Check that the not evaluate a treatement without before status."""

		payload = load_treatment_json()
		payload['id'] = str(uuid.uuid4())
		del payload['before_status']
		self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/data/treatment', payload)
		mov_get_log_message_with('ERROR',payload)

	def test_not_evaluate_treatment_without_actions(self):
		"""Check that the not evaluate a treatement without actions."""

		payload = load_treatment_json()
		payload['id'] = str(uuid.uuid4())
		del payload['actions']
		self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/data/treatment', payload)
		mov_get_log_message_with('ERROR',payload)

	def test_not_evaluate_treatment_with_empty_actions(self):
		"""Check that the not evaluate a treatement with empty actions."""

		payload = load_treatment_json()
		payload['id'] = str(uuid.uuid4())
		payload['actions'] = []
		self.message_service.publish_to('valawai/c2/treatment_nonmaleficence_valuator/data/treatment', payload)
		mov_get_log_message_with('ERROR',payload)


if __name__ == '__main__':
    unittest.main()
