Feature: Children
  In order to be able to have the children of a module result
  As a developer
  I want to find children module results

  @skip @kalibro_configuration_restart @kalibro_processor_restart
  Scenario: ModuleResult children returns valid module result
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_client.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    When I ask for the children of the processing root module result
    Then I should get a list with the children module results
    And The first children should have a module
