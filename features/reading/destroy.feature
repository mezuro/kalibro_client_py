Feature: Reading destruction
  In order to be able to manipulate readings
  As a developer
  I want to destroy a given reading

  @kalibro_configuration_restart
  Scenario: Destroying an existing reading
    Given I have a reading group with name "RG"
    And the given reading group has the following readings:
      |   label   | grade |     color    |
      | "Awesome" |  10   |     3333ff   |
    When I destroy the reading
    Then the reading should no longer exist
