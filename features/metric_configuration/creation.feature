Feature: Create
  In order to manipulate metric configurations
  As a developer
  I want to create a metric configuration

  @kalibro_configuration_restart
  Scenario: creating a metric configuration
	  Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a reading group with name "Group"
    When I have a loc configuration within the given kalibro configuration
    Then the metric configuration should exist
