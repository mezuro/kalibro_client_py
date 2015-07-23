Feature: Destroy
  In order to be able to have projects
  As a developer
  I want to detroy projects

  @kalibro_processor_restart
  Scenario: destroy an existing project
    Given I have a project with name "Kalibro"
    When I destroy the project with the same id of the given project
    Then the project should no longer exist
