Feature: All Names
  In order to be able to have metric collectors
  As a developer
  I want to get all the available metric collector names

  Scenario: all metric collectors names
    When I get all metric collector names
    Then it should return Analizo string inside of an array