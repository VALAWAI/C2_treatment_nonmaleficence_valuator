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
#

import json
from pathlib import Path


def __load_json(file:str):
	"""Load the json file"""
	with Path(__file__).parent.joinpath(file).open() as file:
		return json.load(file)

def load_treatment_json():
	"""Obtain the distionary defined in the treatment.json"""

	return __load_json('treatment.json')

def load_change_parameters_json():
	"""Obtain the distionary defined in the change_parameters.json"""

	return __load_json('change_parameters.json')
