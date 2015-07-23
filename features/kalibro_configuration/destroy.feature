Feature: Destroy
  In order to manipulate kalibro configurations
  As a developer
  I want to destroy a given kalibro configuration

  @kalibro_configuration_restart
  Scenario: destroying a kalibro configuration
    Given I have a kalibro configuration with name "Java"
    When I destroy the kalibro configuration
    Then the kalibro configuration should no longer exist
