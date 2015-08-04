Feature: Process
  In order to be have repositories
  As a developer
  I want to start the repository processing

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With one repository
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                        |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    When I call the process method for the given repository
    Then I should get success
