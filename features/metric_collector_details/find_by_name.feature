Feature: Find By Name
  In order to be able to have metric collectors
  As a developer
  I want to get a metric collector by name

  Scenario: get a metric collector by name
    When I search metric collector Analizo by name
    Then I should get Analizo metric collector

  Scenario: get a metric collector by inexistent name
    When I search metric collector Avalio by name
    Then I should get an error