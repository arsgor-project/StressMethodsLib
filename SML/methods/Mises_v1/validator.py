import pandas as pd

from StressMethodsLib.SML.utils.Validator.Validator import Validator
from ...utils.Logger import Logger


class MisesValidator(Validator):
	def validate(self, logger: Logger) -> tuple[bool, pd.DataFrame]:
		result, data = super().validate(logger)
		if not result:
			raise Exception()
		return result, data


def get_validator(_json_path: str, _data_path: str) -> Validator:
	val: Validator = MisesValidator(_json_path, _data_path)
	return val
