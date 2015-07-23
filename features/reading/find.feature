Feature: Find
  In order to be able to have readings
  As a developer
  I want to find a given reading

  @kalibro_configuration_restart @skip
  Scenario: find a valid reading
    Given I have a reading group with name "Kalibro"
    And I have a reading within the given reading group
    When I ask for a reading with the same id of the given reading
    Then I should get the given reading
