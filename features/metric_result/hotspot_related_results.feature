Feature: Related HotspotMetricResults
  In order to list which HotspotMetricResult is related to a given one
  As a developer
  I want to be able to call them directly as they were associated

  @kalibro_configuration_restart @kalibro_processor_restart
  Scenario: when there are HotspotMetricResults
    Given I have a kalibro configuration with name "Conf"
    And I have a flay configuration within the given kalibro configuration
    And I have the given repository:
      |        name       | scm_type |                   address                        |  branch |
      | Kalibro Processor |    GIT   | https://github.com/mezuro/kalibro_processor.git  | v0.11.0 |
    And I call the process method for the given repository
    And I wait up for a ready processing
    When I request the first hotspot metric result from the root module result
    And I ask for the related results for the given metric result
    Then I should get a list of hotspot metric results including the given one
