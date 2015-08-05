Feature: Last ready processing
  In order to be able to retrieve processing results
  As a developer
  I want to be able to check the last ready processing

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Last ready processing with one repository just after with ready processing
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    When I call the last_ready_processing method for the given repository
    Then I should get a Processing
    And this processing should have process times
