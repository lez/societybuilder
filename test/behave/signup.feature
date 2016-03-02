Feature: REST API

  Scenario: signup with a user
     When the testuser signs up
     Then the testuser is able to log in
      And the testuser is able to log out

  Scenario: create page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
     Then I get a 200 OK
      And I can view the page called "mokus" with description "fenn a fan"

  Scenario: create invalid page over REST
    Given I am signed in
     When I create a page called "mokusssssssssssssssssssssssssss" with description "fenn a fan"
     Then I get a 400 error
      And Value of "name" is invalid because "Name is too long"

  Scenario: modify page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
      And I modify the page description to "hello vilag"
     Then I get a 200 OK
      And I can view the page called "mokus" with description "hello vilag"

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
     Then I get a 200 OK
      And I cannot view the page

  Scenario: delete a nonexistent page over REST
    Given I am signed in
     When I delete a nonexistent page
     Then I get a 404 error

# posts
  Scenario: post on my wall
    Given I am signed in
     When I post "hello world" on my wall
     Then I get a 200 OK
      And I can view the post with content "hello world"

  Scenario: post on my page
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
      And I post "hello world" on the wall of the page
     Then I get a 200 OK
      And I can view the post with content "hello world"
      And The post is on the wall of the page
#FIX  And the post is the first on my wall


# comments
  Scenario: comment on a post
    Given I am signed in
      And I have a post
     When I comment "bazinga" on the post
     Then I get a 200 OK
      And the comment author is me
      And the comment created time is just now
      And the comment modified time is null
      And the post has 1 comment "bazinga"

  Scenario: modify a comment
    Given I am signed in
      And I have a post
      And I have a comment on the post
     When I modify the comment to "not really"
     Then I get a 200 OK
      And the comment modified time is just now
      And the post has 1 comment "not really"
