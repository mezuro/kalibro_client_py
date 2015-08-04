Feature: history of
  In order to be able to get the date metric results of a processed repository
  As a developer
  I want to get the date metric results of the given module result and the given metric name

  @skip @kalibro_configuration_restart @kalibro_processor_restart
  Scenario: when there is a metric result
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_client.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    And I call the first_processing method for the given repository
    When I call the history of method with the metric name and the results root id of the given processing
    Then I should get a list of date metric results
