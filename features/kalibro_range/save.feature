Feature: Save
  In order to be able to use ranges
  As a developer
  I want to save it on kalibro database

  @kalibro_configuration_restart
  Scenario: When there is a metric configuration
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have an unsaved range within the given reading
    When I ask to save the given range
    Then the id of the given range should be set