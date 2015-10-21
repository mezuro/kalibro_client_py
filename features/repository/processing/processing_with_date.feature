Feature: Processing with date
  In order to be able to retrieve processing results
  As a developer
  I want to be able to retrieve the processing for a given date

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Processing with date with one repository just after starting to process and tomorrow's date
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the processing_with_date method for the given repository and tomorrow's date
    Then I should get a Processing

  @kalibro_processor_restart @kalibro_configuration_restart
  Scenario: Processing with date with one repository just after starting to process and yesterday's date
    Given I have a project with name "Kalibro"
    And I have a sample configuration with MetricFu metrics
    And the given project has the following Repositories:
      |   name    | scm_type |                       address                    |
      |  Kalibro  |    GIT   | https://github.com/mezuro/kalibro_processor.git  |
    And I call the process method for the given repository
    And I wait up to 1 seconds
    When I call the processing_with_date method for the given repository and yesterday's date
    Then I should get a Processing
