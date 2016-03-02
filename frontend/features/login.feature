Feature: user handling

  Scenario: signing up
   Given I am on the front page
    When I sign up
    Then I am logged in

  Scenario: logging in
   Given I am on the front page
    When I log in
    Then I am logged in

