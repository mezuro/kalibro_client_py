Feature: Find
  In order to be able to have ranges
  As a developer
  I want to find ranges

@kalibro_configuration_restart
Scenario: find a valid range
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have a range within the given reading
    When I search a range with the same id of the given range
    Then it should return the same range as the given one