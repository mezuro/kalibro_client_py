import kalibro_client


def before_scenario(context, scenario):
    if 'kalibro_processor_restart' in scenario.tags:
        kalibro_client.clean_processor()

    if 'kalibro_configuration_restart' in scenario.tags:
        kalibro_client.clean_configurations()

    if 'skip' in scenario.tags:
        scenario.mark_skipped()
