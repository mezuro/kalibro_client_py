Feature: Last processing
  In order to be able to retrieve processing results
  As a developer
  I want to be able to retrieve the last processing

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Last processing with one repository just after starting to process
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the last_processing method for the given repository
    Then I should get a Processing
