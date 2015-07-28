Feature: Update
  In order to be able to change kalibro ranges
  As a developer
  I want to update a kalibro range

  @kalibro_configuration_restart
  Scenario: When the update is successful
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have a range within the given reading
    When I change the "beginning" to "-250"
    And I change the "end" to "250"
    And I change the "comments" to "my new range"
    And I ask to update the given range
    Then I should not receive errors

  @kalibro_configuration_restart
  Scenario: When trying to update beginning with an invalid value
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have a range within the given reading
    When I change the "beginning" to "bla"
    And I ask to update the given range
    Then I should get the error "Beginning is not a number"

  @kalibro_configuration_restart
  Scenario: When trying to set the beginning with a number greater than the end
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have a range within the given reading
    When I change the "beginning" to "INF"
    And I change the "end" to "-INF"
    And I ask to update the given range
    Then I should get the error "End The End value should be greater than the Beginning value."

  @kalibro_configuration_restart
  Scenario: When trying to set the beginning with a number greater than end
    Given I have a kalibro configuration with name "Java"
    And I have a reading group with name "Group"
    And I have a metric configuration within the given kalibro configuration
    And I have a reading within the given reading group
    And I have a range within the given reading
    And I have another range within the given reading
    When I change the "beginning" to "0"
    And I ask to update the given range
    Then I should get the error "Beginning Should be unique within a Metric Configuration"
    And I should get the error "Beginning There is already a KalibroRange within these boundaries! Please, choose another interval."

