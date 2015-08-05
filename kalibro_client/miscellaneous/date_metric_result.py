from collections import namedtuple
from datetime import datetime
import dateutil.parser

import kalibro_client.processor

class DateMetricResult(namedtuple('DateMetricResult', 'date metric_result')):
    __slots__ = ()

    # __new__ is overriden since namedtuple is a imutable type
    def __new__(cls, date, metric_result):
        if metric_result is not None and not isinstance(metric_result, kalibro_client.processor.MetricResult):
            parsed_metric_result = kalibro_client.processor.MetricResult(**metric_result)
        else:
            parsed_metric_result = metric_result

        if date is not None and not isinstance(date, datetime):
            parsed_date = dateutil.parser.parse(date)
        else:
            parsed_date = date

        return super(cls, DateMetricResult).__new__(cls, parsed_date, parsed_metric_result)

    def _asdict(self):
        dict_ = super(DateMetricResult, self)._asdict()

        dict_['metric_result'] = self.metric_result._asdict()

        return dict_
