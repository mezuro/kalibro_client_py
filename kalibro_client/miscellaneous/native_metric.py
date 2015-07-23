from kalibro_client.miscellaneous import Metric


class NativeMetric(Metric):
    def __init__(self, languages=None, metric_collector_name=None, *init_args, **init_kwargs):
        init_kwargs['type'] = 'NativeMetricSnapshot'
        super(NativeMetric, self).__init__(*init_args, **init_kwargs)
        self.languages = languages
        self.metric_collector_name = metric_collector_name

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def metric_collector_name(self):
        return self._metric_collector_name

    @metric_collector_name.setter
    def metric_collector_name(self, value):
        self._metric_collector_name = value

    def _asdict(self):
        dict_ = super(NativeMetric, self)._asdict()
        dict_['languages'] = self.languages
        dict_['metric_collector_name'] = self.metric_collector_name
        return dict_
