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

# working with pages
  Scenario: create a page
    Given I am logged in
     When I create a page called "Universe" with the description "42"
     Then the page is created
      And the page name is "Universe"
      And the page description is "42"
