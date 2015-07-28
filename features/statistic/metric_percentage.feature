Feature: Calculating the percentage of metrics used
  In order to be able to calculate the metric percentage used
  As a developer
  I want to know which metrics are more used

  @kalibro_configuration_restart
  Scenario: With an used metric
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric with name "Lines of Code"
    And I have a loc configuration within the given kalibro configuration
    When I request the metric_percentage
    Then I should get a hash containing a real number
