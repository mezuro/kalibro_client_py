Feature: Repositories listing
  In order to be able to check know if a repository still exists
  As a developer
  I want to check that on the service

  @skip @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With existing project repository
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    When I ask to check if the given repository exists
    Then I should get true
