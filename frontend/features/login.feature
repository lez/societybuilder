Feature: user handling

  Scenario: signing up
   Given I am on the front page
    When I sign up
    Then I get logged in
# And I received welcome email

  Scenario: logging in
   Given I am on the front page
    When I log in
    Then I get logged in

  Scenario: log out
   Given I am logged in
    When I log out
    Then I get logged out
