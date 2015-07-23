Feature: Creation
  In order to be able to have reading groups
  As a developer
  I want to create a reading group

  @kalibro_configuration_restart
  Scenario: creating a reading group
    When I create a reading group with name "Kalibro"
    Then the reading group should exist
