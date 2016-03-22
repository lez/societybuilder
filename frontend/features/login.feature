Feature: user handling

  Scenario: sign up
   Given I visit "/signup"
    When I sign up
    Then I get logged in
# And I received welcome email

  Scenario: sign up with invalid username
    Given I visit "/signup"
    When I sign up as "x"
    Then the error message below "login" is "login name is too short"

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

  Scenario: create a page with too short fields
    Given I am logged in
     When I create a page called "U" with the description "4"
     Then the error message below "name" is "name is too short"
      And the error message below "description" is "description is too short"

  Scenario: edit a page description
    Given I am logged in
     When I create a page called "End of the World" with the description "42"
      And I click the edit page link
      And I set the page description to "everything"
      And I press the button "Mentés"
     Then the page description on edit page is "everything"

  Scenario: edit a page description with refresh
    Given I am logged in
     When I create a page called "Over the rainbow" with the description "42"
      And I click the edit page link
      And I set the page description to "everything"
      And I press the button "Mentés"
      And I refresh the page
     Then the page description on edit page is "everything"

  Scenario: post on a page
    Given I am logged in
     When I create a page called "Unicorns" with the description "42"
      And I post "kukuriku"
     Then I see a post with content "kukuriku"

  Scenario: edit profile
    Given I am logged in
    When I visit the edit profile page
    And I set the about me to "the best monkey"
    And I press the button "Mentés"
    Then the about me says I am "the best monkey"

  Scenario: post on my wall
    Given I am logged in
    When I visit "/komakoma"
    And I post "kukuriku"
    Then I see a post with content "kukuriku"

