Feature: Project repositories
  In order to be able to visualize repositories
  As a developer
  I want to see all the repository from a given project

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: With existing project repository
    Given I have a project with name "Kalibro"
    And I have a kalibro configuration with name "Conf"
    And the given project has the following Repositories:
      |   name    | scm_type |                   address                        |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    When I ask for repositories from the given project
    Then I should get a list with the given repository
    And the repositories should contain the project id
