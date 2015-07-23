from kalibro_client.base import attributes_class_constructor


class Metric(attributes_class_constructor('MetricAttr', (('type', None), ('name', None), ('code', None), ('scope', None), ('description', None)))):
    pass