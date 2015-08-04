Feature: Descendant values
  In order to be able to get the descendant values of a processed repository
  As a developer
  I want to get the descendant metric results of the given module result

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
    And I search a metric result with descendant values for the given metric result
    Then I should get a Float list
