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

from pydantic import BaseModel, Field


class AgeRangeOption(str,Enum):
	"""The different ranges of ages for a patient."""

	# The age is between 0 and 19 years old.
	AGE_BETWEEN_0_AND_19 = "AGE_BETWEEN_0_AND_19"

	# The age is between 20 and 29 years old.
	AGE_BETWEEN_20_AND_29 = "AGE_BETWEEN_20_AND_29"

	# The age is between 30 and 39 years old.
	AGE_BETWEEN_30_AND_39 = "AGE_BETWEEN_30_AND_39"

	# The age is between 40 and 49 years old.
	AGE_BETWEEN_40_AND_49 = "AGE_BETWEEN_40_AND_49"

	# The age is between 50 and 59 years old.
	AGE_BETWEEN_50_AND_59 = "AGE_BETWEEN_50_AND_59"

	# The age is between 60 and 69 years old.
	AGE_BETWEEN_60_AND_69 = "AGE_BETWEEN_60_AND_69"

	# The age is between 70 and 79 years old.
	AGE_BETWEEN_70_AND_79 = "AGE_BETWEEN_70_AND_79"

	# The age is between 80 and 89 years old.
	AGE_BETWEEN_80_AND_89 = "AGE_BETWEEN_80_AND_89"

	# The age is between 90 and 99 years old.
	AGE_BETWEEN_90_AND_99 = "AGE_BETWEEN_90_AND_99"

	# The age greater than 99 years old.
	AGE_MORE_THAN_99 = "AGE_MORE_THAN_99"

class SurvivalOptions(str,Enum):
	"""The possible survival options."""

	# The survival is less than 12 month
	LESS_THAN_12_MONTHS = "LESS_THAN_12_MONTHS"

	# The survival is more than 12 month
	MORE_THAN_12_MONTHS = "MORE_THAN_12_MONTHS"

	# The survival is unknown.
	UNKNOWN = "UNKNOWN"

class SPICT_Scale(str,Enum):
	""" It helps identify the most fragile people who have one or more health
		problems. It is based on the comprehensive geriatric assessment (applicable
		to non-geriatric patients) that evaluates areas such as functional
		independence, nutritional status, cognitive, emotional, social, geriatric
		syndromes (confusion syndrome, falls, ulcers, polypharmacy, dysphagia),
		symptoms (pain or dyspnea) and diseases oncological, respiratory, cardiac,
		neurological, digestive or renal).
	"""

	# The low option of the SPICT scale.
	LOW = "LOW"

	# The moderate option of the SPICT scale.
	MODERATE = "MODERATE"

	# The high option of the SPICT scale.
	HIGH = "HIGH"

	# The level in the SPICT scale.
	UNKNOWN = "UNKNOWN"

class ClinicalRiskGroupOption(str,Enum):
	""" The possible clinical risk groups."""

	# The clinical risk group is promotion & prevention.
	PROMOTION_AND_PREVENTION = "PROMOTION_AND_PREVENTION"

	# The clinical risk group is self-management support.
	SELF_MANAGEMENT_SUPPORT = "SELF_MANAGEMENT_SUPPORT"

	# The clinical risk group is illness management.
	ILLNESS_MANAGEMENT = "ILLNESS_MANAGEMENT"

	# The clinical risk group is case AgeRangeOption.management.
	CASE_MANAGEMENT = "CASE_MANAGEMENT"

	# The clinical risk group is unknown.
	UNKNOWN = "UNKNOWN"

class BarthelIndex(str,Enum):
	""" This index allow to check the functional independence for basic activities."""

	# When the functional independence is between 0 and 20%.
	TOTAL = "TOTAL"

	# When the functional independence is between 21 and 60%.
	SEVERE = "SEVERE"

	# When the functional independence is between 61 and 90%.
	MODERATE = "MODERATE"

	# When the functional independence is between 91 and 99%.
	MILD = "MILD"

	# When the functional independence is 100%.
	INDEPENDENT = "INDEPENDENT"

	# When the functional independence is unknown.
	UNKNOWN = "UNKNOWN"

class CognitiveImpairmentLevel(str,Enum):
	""" Define the posible cognitive impairment levels."""

	# The cognitive impairment is absent.
	ABSENT = "ABSENT"

	# The cognitive impairment is mild-moderate.
	MILD_MODERATE = "MILD_MODERATE"

	# cognitive impairment is severe.
	SEVERE = "SEVERE"

	# The cognitive level is unknown.
	UNKNOWN = "UNKNOWN"

class DiscomfortDegree(str,Enum):
	""" The degree of discomfort."""

	# The discomfort degree is Low or no discomfort.
	LOW = "LOW"

	# The discomfort degree is medium.
	MEDIUM = "MEDIUM"

	# The discomfort degree is medium.
	HIGH ="HIGH"

	# The cognitive level is unknown.
	UNKNOWN = "UNKNOWN"

class NITLevel(str,Enum):
	""" The level of therapeutic intensity."""

	# It includes all possible measures to prolong survival
	ONE = "ONE"

	# Includes all possible measures except CPR.
	TWO_A = "TWO_A"

	# Includes all possible measures except CPR and ICU.
	TWO_B = "TWO_B"

	# Includes complementary scans and non-invasive treatments.
	THREE = "THREE"

	# It includes empiric symptomatic treatments according to clinical suspicion,
	# which can be agreed as temporary.
	FOUR = "FOUR"

	# No complementary examinations or etiological treatments are carried out, only
	# treatments for comfort.
	FIVE = "FIVE"

class PatientStatusCriteria(BaseModel):
	"""The status of a patient by some criteria."""

	age_range: AgeRangeOption | None = Field(default=None, title="The range of age of the patient status.")
	ccd: bool | None = Field(default=None, title="Check if the patient status has a Complex Cronic Disease (CCD).")
	maca: bool | None = Field(default=None, title="A MACA patient status has answered no to the question: Would you be surprised if this patient died in less than 12 months?")
	expected_survival: SurvivalOptions | None = Field(default=None, title="The expected survival time for the patient status.")
	frail_VIG: SPICT_Scale| None = Field(default=None, title="The fragility index of the patient status.")
	clinical_risk_group: ClinicalRiskGroupOption | None = Field(default=None, title="The clinical risk group of the patient status.")
	has_social_support: bool | None = Field(default=None, title="Check if the patient status has social support.")
	independence_at_admission: BarthelIndex | None = Field(default=None, title="The independence for basic activities of daily living at admission.")
	independence_instrumental_activities: int | None = Field(default=None, title="The index that measures the independence for instrumental activities.")
	has_advance_directives: bool | None = Field(default=None, title="The answers to the question: Does the patient status have advance directives?")
	is_competent: bool | None = Field(default=None, title="The answers to the question: Is the patient status competent to understand the instructions of health personnel?")
	has_been_informed: bool | None = Field(default=None, title="The answers to the question: To the patient status or his/her referent authorized has been informed of possible treatments and the consequences of receiving it or No.")
	is_coerced: bool | None = Field(default=None, title="The answers to the question: Is it detected that the patient status has seen coerced/pressured by third parties?")
	has_cognitive_impairment: CognitiveImpairmentLevel| None = Field(default=None, title="Inform if the patient status has cognitive impairment.")
	has_emocional_pain: bool | None = Field(default=None, title="Inform if the patient status has emotional pain.")
	discomfort_degree: DiscomfortDegree | None = Field(default=None, title="Describe the degree of discomfort of the patient status before applying any action.")
	nit_level: NITLevel | None = Field(default=None, title="Describe the level of therapeutic intensity of the patient.")

	def normalized_age_range(self):
		"""Return the normalized value of the age range."""

		match self.age_range:
			case AgeRangeOption.AGE_BETWEEN_0_AND_19:
				return 0.1
			case AgeRangeOption.AGE_BETWEEN_20_AND_29:
				return 0.2
			case AgeRangeOption.AGE_BETWEEN_30_AND_39:
				return 0.3
			case AgeRangeOption.AGE_BETWEEN_40_AND_49:
				return 0.4
			case AgeRangeOption.AGE_BETWEEN_50_AND_59:
				return 0.5
			case AgeRangeOption.AGE_BETWEEN_60_AND_69:
				return 0.6
			case AgeRangeOption.AGE_BETWEEN_70_AND_79:
				return 0.7
			case AgeRangeOption.AGE_BETWEEN_80_AND_89:
				return 0.8
			case AgeRangeOption.AGE_BETWEEN_90_AND_99:
				return 0.9
			case AgeRangeOption.AGE_MORE_THAN_99:
				return 1.0
			case _:
				return 0.0


	def normalized_ccd(self):
		"""Return the normalized value of the CCD."""

		if self.ccd is False:

			return 1.0

		return 0.0


	def normalized_maca(self):
		"""Return the normalized value of the MACA."""

		if self.maca is False:

			return 1.0

		return 0.0


	def normalized_expected_survival(self):
		"""Return the normalized value of the expected survival."""

		match self.expected_survival:
			case SurvivalOptions.MORE_THAN_12_MONTHS:
				return 1.0
			case _:
				return 0.0

	def normalized_frail_vig(self):
		"""Return the normalized value of the frail VIG."""

		match self.frail_VIG:
			case SPICT_Scale.LOW:
				return 1.0
			case SPICT_Scale.MODERATE:
				return 0.5
			case _:
				return 0.0

	def normalized_clinical_risk_group(self):
		"""Return the normalized value of the clinical risk group."""

		match self.clinical_risk_group:
			case ClinicalRiskGroupOption.PROMOTION_AND_PREVENTION:
				return 1.0
			case ClinicalRiskGroupOption.SELF_MANAGEMENT_SUPPORT:
				return 0.5
			case _:
				return 0.0

	def normalized_has_social_support(self):
		"""Return the normalized value of the has social support."""

		if self.has_social_support is True:

			return 1.0

		return 0.0


	def normalized_independence_at_admission(self):
		"""Return the normalized value of the independence at admission."""

		match self.independence_at_admission:
			case BarthelIndex.TOTAL:
				return 0.1
			case BarthelIndex.SEVERE:
				return 0.4
			case BarthelIndex.MODERATE:
				return 0.75
			case BarthelIndex.MILD:
				return 0.95
			case BarthelIndex.INDEPENDENT:
				return 1.0
			case _:
				return 0.0

	def normalized_independence_instrumental_activities(self):
		"""Return the normalized value of the independence instrumental activities."""

		match self.independence_instrumental_activities:
			case 1:
				return 0.13
			case 2:
				return 0.26
			case 3:
				return 0.38
			case 4:
				return 0.5
			case 5:
				return 0.63
			case 6:
				return 0.75
			case 7:
				return 0.88
			case 8:
				return 1.0
			case _:
				return 0.0

	def normalized_has_advance_directives(self):
		"""Return the normalized value of the has advance directives."""

		if self.has_advance_directives is True:

			return 1.0

		return 0.0

	def normalized_is_competent(self):
		"""Return the normalized value of the is competent."""

		if self.is_competent is True:

			return 1.0

		return 0.0


	def normalized_has_been_informed(self):
		"""Return the normalized value of the has been informed."""

		if self.has_been_informed is True:

			return 1.0

		return 0.0


	def normalized_is_coerced(self):
		"""Return the normalized value of the is coerced."""

		if self.is_coerced is False:

			return 1.0

		return 0.0


	def normalized_has_cognitive_impairment(self):
		"""Return the normalized value of the has cognitive impairment."""

		match self.has_cognitive_impairment:
			case CognitiveImpairmentLevel.ABSENT:
				return 1.0
			case CognitiveImpairmentLevel.MILD_MODERATE:
				return 0.5
			case _:
				return 0.0

	def normalized_has_emocional_pain(self):
		"""Return the normalized value of the has emocional pain."""

		if self.has_emocional_pain is False:

			return 1.0

		return 0.0


	def normalized_discomfort_degree(self):
		"""Return the normalized value of the has discomfort degree."""

		match self.discomfort_degree:
			case DiscomfortDegree.LOW:
				return 1.0
			case DiscomfortDegree.MEDIUM:
				return 0.5
			case _:
				return 0.0
