from kalibro_client.miscellaneous import NativeMetric


class HotspotMetric(NativeMetric):
    def __init__(self, *init_args, **init_kwargs):
        init_kwargs['type'] = 'HotspotMetricSnapshot'
        init_kwargs['scope'] = 'SOFTWARE'
        super(HotspotMetric, self).__init__(*init_args, **init_kwargs)
