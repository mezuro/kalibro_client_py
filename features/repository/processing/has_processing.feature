Feature: Has processing
  In order to be able to retrieve processing results
  As a developer
  I want to be able to check if a repository has processings

  @skip @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With one repository after process
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the has_processing for the given repository
    Then I should get true
