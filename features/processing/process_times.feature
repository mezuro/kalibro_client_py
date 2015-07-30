Feature: ProcessTimes
  In order to be able to have Processings
  As a developer
  I want to get all the ProcessTimes for the given processing

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With a ready processing
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                address                   |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_client |
    And I call the process method for the given repository
    And I wait up for a ready processing
    When I call the processing method for the given repository
    When I call the processes_times method for the given processing
    Then I should get a list of ProcessTimes
