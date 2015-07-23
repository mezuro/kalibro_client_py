Feature: Creation
  In order to be able to have projects
  As a developer
  I want to create projects

  @kalibro_processor_restart
  Scenario: create a valid project
    When I create the project with name "Kalibro"
    Then the project should exist
