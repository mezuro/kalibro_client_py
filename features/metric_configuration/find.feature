Feature: Find
  In order to be able to have configurations
  As a developer
  I want to find metric_configurations

  @kalibro_configuration_restart
  Scenario: find a valid metric configuration
	  Given I have a kalibro configuration with name "Kalibro for Java"
    And I have a reading group with name "Group"
    And I have a loc configuration within the given kalibro configuration
    When I search a metric configuration with the same id of the given metric configuration
    Then it should return the same metric configuration as the given one


  @kalibro_configuration_restart
  Scenario: try to find an inexistent metric configuration
    When I search an inexistent metric configuration
    Then I should get an error
