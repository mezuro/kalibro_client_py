Feature: All
  In order to be able to have kalibro configurations
  As a developer
  I want to get all the available kalibro configurations

  @kalibro_configuration_restart
  Scenario: one kalibro configuration
    Given I have a kalibro configuration with name "Java"
    When I get all the kalibro configurations
    Then I should get a list with the given kalibro configuration
