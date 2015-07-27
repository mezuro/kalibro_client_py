from collections import namedtuple

class DateMetricResult(namedtuple('DateMetricResult', 'date metric_result')):
    __slots__ = ()

    def __new__(cls, metric_result, *args, **kwargs):
        kwargs['metric_result'] = MetricResult(**metric_result)
        return super(cls, DateMetricResult).__new__(cls, *args, **kwargs)

