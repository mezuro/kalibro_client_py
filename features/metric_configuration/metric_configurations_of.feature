Feature: MetricConfigurationsOf
  In order to be able to have configurations
  As a developer
  I want to get all metric_configurations of a kalibro configuration

  @kalibro_configuration_restart
  Scenario: get a list of all metric configurations of some kalibro configuration
	  Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    When I request all metric configurations of the given kalibro configuration
    Then I should get a list of its metric configurations

  @kalibro_configuration_restart
  Scenario: get an empty list for a kalibro configuration without metric configurations
  	Given I have a kalibro configuration with name "Kalibro for Java"
    When I request all metric configurations of the given kalibro configuration
    Then I should get an empty list of metric configurations
