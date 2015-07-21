Feature: Creation
  In order to be able to have kalibro configurations
  As a developer
  I want to create kalibro configurations

  @kalibro_configuration_restart
  Scenario: create a valid kalibro configuration
    When I create the kalibro configuration with name "Kalibro"
    Then the kalibro configuration should exist
