Feature: Types listing
  In order to be able to create repositories
  As a developer
  I want to see all the repository types available

  Scenario: listing the types
    When I list types
    Then I should get an array of types
