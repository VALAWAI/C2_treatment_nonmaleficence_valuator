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
#

from enum import Enum

from patient_status_criteria import PatientStatusCriteria
from pydantic import BaseModel, Field


class TreatmentAction(str,Enum):
	"""The possible action to do for a treatment.
	"""

	# The patient can receive a Cardiopulmonary resuscitation.
	CPR = "CPR"

	# The patient need an organ transplant.
	TRANSPLANT = "TRANSPLANT"

	# The patient can be in the intensive curing unit.
	ICU = "ICU"

	# The patient can have non-invasive mechanical ventilation.
	NIMV = "NIMV"

	# The patient can receive vasoactive drugs.
	VASOACTIVE_DRUGS = "VASOACTIVE_DRUGS"

	# The patient can have dialysis.
	DIALYSIS = "DIALYSIS"

	# The patient can receive simple clinical trials.
	SIMPLE_CLINICAL_TRIAL = "SIMPLE_CLINICAL_TRIAL"

	# The patient can receive medium clinical trials.
	MEDIUM_CLINICAL_TRIAL = "MEDIUM_CLINICAL_TRIAL"

	# The patient can receive advanced clinical trials.
	ADVANCED_CLINICAL_TRIAL = "ADVANCED_CLINICAL_TRIAL"

	# The patient can have palliative surgery.
	PALLIATIVE_SURGERY = "PALLIATIVE_SURGERY"

	# The patient can have surgery with the intention of curing.
	CURE_SURGERY = "CURE_SURGERY"

class TreatmentPayload(BaseModel):
	"""The treatment to apply to a patient."""
	id: str = Field(min_length=1,title="The identifier of the treatment.", json_schema_extra={"example":"Treatment_12345"})
	patient_id: str | None = Field(default=None,title="The identifier of the patient that the treatment is applied.", json_schema_extra={"example":"Patient_12345"})
	created_time: int | None = Field(default=None,title="The epoch time, in seconds, when the patient treatment is created.", json_schema_extra={"example":1736932587})
	before_status: PatientStatusCriteria = Field(title="The status before to apply the treatment.")
	actions:  list[TreatmentAction] = Field(min_length=1,title="The treatment actions to apply over the patient.")
	expected_status: PatientStatusCriteria | None = Field(default=None,title="The expected status of the patient after applying the treatment.")

