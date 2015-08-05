Feature: First processing after
  In order to be able to retrieve processing results
  As a developer
  I want to be able to retrieve the first processing after a given date

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: First processing after with one repository just after starting to process
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/rafamanzo/runge-kutta-vtk.git |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the first_processing_after method for the given repository and yesterday's date
    Then I should get a Processing
