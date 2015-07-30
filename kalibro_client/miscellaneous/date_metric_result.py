from collections import namedtuple

from kalibro_client.processor import MetricResult

class DateMetricResult(namedtuple('DateMetricResult', 'date metric_result')):
    __slots__ = ()

    def __new__(cls, metric_result, *args, **kwargs):
        kwargs['metric_result'] = MetricResult(**metric_result)
        return super(cls, DateMetricResult).__new__(cls, *args, **kwargs)

    def _asdict(self):
        dict_ = super(DateMetricResult, self)._asdict()

        dict_['metric_result'] = self.metric_result._asdict()
        return dict_
