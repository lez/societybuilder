Feature: signup

  Scenario: signup with a user
     When the testuser signs up
     Then the testuser is able to log in
      And the testuser is able to log out

  Scenario: create page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
     Then I can view the page called "mokus" with description "fenn a fan"

  Scenario: modify page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
      And I modify the page description to "hello vilag"
     Then I can view the page called "mokus" with description "hello vilag"

  Scenario: modify a nonexistent page over REST
    Given I am signed in
     When I modify a nonexistent page
     Then I get a 404 error

  Scenario: list pages over REST
    Given I am signed in
      And Page records are cleaned from the database
     When I create a page called "mokus" with description "fenn a fan"
      And I create a page called "hinta" with description "palinta"
     Then I see 2 pages in page listing
      And The first page in the list is called "mokus"
      And The second page in the list is called "hinta"

  Scenario: delete page over REST
    Given I am signed in
      And Page records are cleaned from the database
      And There is a page called "mokus" with description "fenn a fan"
     When I delete the page
     Then I cannot view the page

  Scenario: delete a nonexistent page over REST
    Given I am signed in
     When I delete a nonexistent page
     Then I get a 404 error