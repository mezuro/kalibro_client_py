Feature: Has processing before
  In order to be able to retrieve processing results from a given date
  As a developer
  I want to be able to check if a repository has processings before it

  @skip @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With one repository just after starting to process
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the has_processing_before for the given repository with tomorrows's date
    Then I should get true
