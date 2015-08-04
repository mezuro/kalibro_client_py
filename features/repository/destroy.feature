Feature: Repositories destroying
  In order to manipulate repositories
  As a developer
  I want to destroy a given repository

  @skip @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With existing repository
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    When I destroy the repository
    Then the repository should no longer exist
