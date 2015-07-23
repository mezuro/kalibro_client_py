Feature: Destroy
  In order to manipulate metric configurations
  As a developer
  I want to destroy a given metric configuration

  @kalibro_configuration_restart
  Scenario: destroying a metric configuration
	  Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    When I destroy the metric configuration
    Then the metric configuration should no longer exist
