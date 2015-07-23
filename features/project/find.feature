Feature: Find
  In order to be able to have projects
  As a developer
  I want to find projects

  @kalibro_processor_restart
  Scenario: find a valid project
    Given I have a project with name "Kalibro"
    When I search a project with the same id of the given project
    Then it should return the same project as the given one