Feature: ProcessTimes
  In order to be able to have Processings
  As a developer
  I want to get all the ProcessTimes for the given processing

  @skip @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With a ready processing
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    When I call the processing method for the given repository
    When I call the processes_times method for the given processing
    Then I should get a list of ProcessTimes
