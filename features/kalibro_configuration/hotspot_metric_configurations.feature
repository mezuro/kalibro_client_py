Feature: HotspotMetricConfiguration retrieval
  In order to be able to list just with the HotspotMetricConfigurations
  As a developer
  I want to get all HotspotMetricConfigurations of a given KalibroConfiguration

  @kalibro_configuration_restart
  Scenario: get a list of all hotspot metric configurations of some kalibro configuration
    Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a hotspot metric configuration within the given kalibro configuration
    When I request for hotspot_metric_configurations of the given kalibro configuration
    Then I should get a list with the given HotspotMetricConfiguration
