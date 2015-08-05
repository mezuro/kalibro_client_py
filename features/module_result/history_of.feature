Feature: history of
  In order to be able to have the history of a module result
  As a developer
  I want to get the history of module results

  @kalibro_configuration_restart @kalibro_processor_restart
  Scenario: get the history of a module result
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_client.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    And I get the module result of the processing
    When I ask for the history of the given module result
    Then I should get a list with date module results
