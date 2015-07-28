Feature: Metric Configurations
  In order to see the metric configurations
  As a developer
  I want to list all the metric configurations of a kalibro configuration

  @kalibro_configuration_restart
  Scenario: one metric configuration
    Given I have a kalibro configuration with name "Java"
    And the kalibro configuration has a metric configuration
    When I list all the metric configurations of the kalibro configuration
    Then I should get a list with the given metric configuration
