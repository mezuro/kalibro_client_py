Feature: Module Results
  In order to be able to get the module result associated with this metric result
  As a developer
  I want to get the module result of the given metric result

  @kalibro_configuration_restart @kalibro_processor_restart
  Scenario: when there is a metric result
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                        |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up for a ready processing
    And I call the first_processing method for the given repository
    When I get the first metric result of the given processing
    And I ask for the module result of the given metric result
    Then I should get a module result
