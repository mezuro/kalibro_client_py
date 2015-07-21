Feature: All
  In order to be able to have reading groups
  As a developer
  I want to get all the available reading groups

  @kalibro_configuration_restart
  Scenario: one reading group
    Given I have a reading group with name "Kalibro"
    When I ask for all the reading groups
    Then I should get a list with the given reading group