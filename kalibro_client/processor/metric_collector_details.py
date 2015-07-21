from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.miscellaneous import NativeMetric


@entity_name_decorator
class MetricCollectorDetails(attributes_class_constructor('MetricCollectorDetailsAttr',
                                                          (('name', None),
                                                           ('description', None),
                                                           ('wanted_metrics', None),
                                                           ('processing', None)),
                                                          identity=False),
                            Base):
    def __init__(self, supported_metrics=None, *init_args, **init_kwargs):
        super(MetricCollectorDetails, self).__init__(init_args, init_kwargs)
        self.supported_metrics = supported_metrics

    @property
    def supported_metrics(self):
        return self._supported_metrics

    @supported_metrics.setter
    def supported_metrics(self, value):
        self._supported_metrics = {}
        if value is not None:
            for code, metric in value.iteritems():
                self._supported_metrics[code] = NativeMetric(**metric) if not isinstance(metric, NativeMetric) else metric
