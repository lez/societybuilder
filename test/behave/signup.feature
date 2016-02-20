Feature: signup

  Scenario: signup with a user
     When the testuser signs up
     Then the testuser is able to log in

  Scenario: create page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
     Then I can view the page called "mokus" with description "fenn a fan"
