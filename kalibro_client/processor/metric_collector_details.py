from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.miscellaneous import NativeMetric
from kalibro_client.errors import KalibroClientNotFoundError

@entity_name_decorator
class MetricCollectorDetails(attributes_class_constructor('MetricCollectorDetailsAttr',
                                                          (('name', None),
                                                           ('description', None)),
                                                          identity=False),
                            Base):
    def __init__(self, supported_metrics=None, *init_args, **init_kwargs):
        super(MetricCollectorDetails, self).__init__(*init_args, **init_kwargs)
        self.supported_metrics = supported_metrics

    def _asdict(self):
        dict_ = super(MetricCollectorDetails, self)._asdict()
        dict_['supported_metrics'] = self.supported_metrics
        return dict_

    @property
    def supported_metrics(self):
        return self._supported_metrics

    @supported_metrics.setter
    def supported_metrics(self, value):
        self._supported_metrics = {}
        if value is not None:
            for code, metric in value.iteritems():
                self._supported_metrics[code] = NativeMetric(**metric) if not isinstance(metric, NativeMetric) else metric

    def find_metric_by_name(self, name):
        for code, metric in self.supported_metrics.iteritems():
            if metric.name == name:
                return metric

    @classmethod
    def find_by_name(cls, name):
        response = cls.request('find', params={"name": name})
        try:
            return cls(**response['metric_collector_details'])
        except KeyError:
            error = response.get('error', None)
            raise KalibroClientNotFoundError(error)

    @classmethod
    def all_names(cls):
        return cls.request('names', method='get')['metric_collector_names']

    @classmethod
    def all(cls):
        return cls.array_to_objects_array(cls.request('', method='get'))
