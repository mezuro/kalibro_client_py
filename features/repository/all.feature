Feature: Repositories listing
  In order to be able to visualize repositories
  As a developer
  I want to see all the repositories on the service

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Repositories listing with existing project repository
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Conf"
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    And I have an independent repository
    When I ask for all the repositories
    Then the response should contain the given repositories
