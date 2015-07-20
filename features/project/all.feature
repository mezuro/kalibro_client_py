Feature: All
  In order to be able to have projects
  As a developer
  I want to get all the available projects

  @kalibro_processor_restart
  Scenario: one project
    Given I have a project with name "Kalibro"
    When I ask for all the projects
    Then I should get a list with the given project