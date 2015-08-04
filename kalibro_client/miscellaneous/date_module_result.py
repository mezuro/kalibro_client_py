from collections import namedtuple
from datetime import datetime
import dateutil.parser

import kalibro_client.processor

class DateModuleResult(namedtuple('DateModuleResult', 'date module_result')):
    __slots__ = ()

    # __new__ is overriden since namedtuple is a imutable type
    def __new__(cls, date, module_result):
        if module_result is not None and not isinstance(module_result, kalibro_client.processor.ModuleResult):
            parsed_module_result = kalibro_client.processor.ModuleResult(**module_result)
        else:
            parsed_module_result = module_result

        if date is not None and not isinstance(date, datetime):
            parsed_date = dateutil.parser.parse(date)
        else:
            parsed_date = date

        return super(cls, DateModuleResult).__new__(cls, parsed_date, parsed_module_result)

    def _asdict(self):
        dict_ = super(DateModuleResult, self)._asdict()

        dict_['module_result'] = self.module_result._asdict()

        return dict_

    def result(self):
        return self.module_result.grade
