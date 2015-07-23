Feature: Readings Of
  In order to be able to have readings
  As a developer
  I want to get the readings of the given reading group

  @kalibro_configuration_restart @skip
  Scenario: readings of a valid reading group
    Given I have a reading group with name "Kalibro"
    And I have a reading within the given reading group
    When I ask for the readings of the given reading group
    Then I should get a list with the given reading
