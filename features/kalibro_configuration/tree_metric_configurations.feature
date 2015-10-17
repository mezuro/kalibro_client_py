Feature: TreeMetricConfiguration retrieval
  In order to be able to list just with the TreeMetricConfigurations
  As a developer
  I want to get all TreeMetricConfigurations of a given KalibroConfiguration

  @kalibro_configuration_restart
  Scenario: get a list of all metric configurations of some kalibro configuration
    Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a reading group with name "Group"
    And I have a tree metric configuration within the given kalibro configuration
    When I request for tree_metric_configurations of the given kalibro configuration
    Then I should get a list with the given TreeMetricConfiguration
