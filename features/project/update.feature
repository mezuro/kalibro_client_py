Feature: Update
  In order to be able to have projects
  As a developer
  I want to update projects

  @kalibro_processor_restart
  Scenario: Setting and resetting the name of a valid project (ensures that update is getting called instead of create)
    Given I have a project with name "Kalibro"
    And I set the project name to "QtCalculator"
    And I save the given project
    And I set the project name to "Kalibro"
    And I save the given project
    Then I should get true as the response