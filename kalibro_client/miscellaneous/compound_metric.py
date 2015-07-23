from kalibro_client.miscellaneous import Metric


class CompoundMetric(Metric):
    def __init__(self, script, *init_args, **init_kwargs):
        init_kwargs['type'] = 'CompoundMetricSnapshot'
        super(CompoundMetric, self).__init__(*init_args, **init_kwargs)

        self.script = script

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, value):
        if value is None:
            raise ValueError("Script cannot be None")

        self._script = value

    def _asdict(self):
        dict_ = super(CompoundMetric, self)._asdict()
        dict_['script'] = self.script
        return dict_