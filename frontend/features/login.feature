Feature: user handling

  Scenario: signing up
   Given I am on the front page
    When I sign up
    Then I am logged in
# And I received welcome email

  Scenario: logging in
   Given I am on the front page
    When I log in
    Then I am logged in

  Scenario: log out
   Given I am a logged in user
    When I log out
    Then I am logged out
