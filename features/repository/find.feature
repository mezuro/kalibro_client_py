Feature: Repositories finding
  In order to be able to visualize a specific repository
  As a developer
  I want to find that repository

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Repositories finding with existing project repository
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Conf"
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    When I ask to find the given repository
    Then I should get the given repository
