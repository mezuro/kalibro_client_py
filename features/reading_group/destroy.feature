Feature: Destroy
  In order to manipulate reading groups
  As a developer
  I want to destroy a given reading group

  @kalibro_configuration_restart
  Scenario: destroying a valid reading group
    Given I have a reading group with name "Kalibro"
    When I destroy the reading group
    Then the reading group should no longer exist

