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
     Then the page name is "Universe"
      And the page description is "42"

  Scenario: edit a page description
    Given I am logged in
     When I create a page called "Universe" with the description "42"
      And I visit the edit page
      And I set the page description to "everything"
      And I press the button "Mentés"
     Then the page description on edit page is "everything"

  Scenario: edit a page description with refresh
    Given I am logged in
     When I create a page called "Universe" with the description "42"
      And I visit the edit page
      And I set the page description to "everything"
      And I press the button "Mentés"
      And I refresh the page
     Then the page description on edit page is "everything"

  Scenario: post on a page
    Given I am logged in
     When I create a page called "Universe" with the description "42"
      And I post "kukuriku"
     Then I see a post with content "kukuriku"