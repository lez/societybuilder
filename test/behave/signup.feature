Feature: REST API

  Scenario: login failure
     When I log in as "nonexistent"
     Then I get a 401 error
      And the error message is "login failed"

  Scenario: signup with a user
     When I sign up as "testuser"
     Then I get a 200 OK

  Scenario: log out
     When I log in as "testuser"
      And I log out
     Then I get a 302 redirect to "/"
# check cookie

  Scenario: signup with a short login
     When I sign up as "I"
     Then I get a 400 error
      And the error message is "login name is too short"

  Scenario: signup with a short login 2
     When I sign up as "ba"
     Then I get a 400 error
      And the error message is "login name is too short"

  Scenario: signup with a short password
     When I sign up as "bazmegye" using password "yo"
     Then I get a 400 error
      And the error message is "password too short"

  Scenario: signup with invalid login name
     When I sign up as "GrétaGarbó"
     Then I get a 400 error
    And the error message is "invalid character, use alphanumeric letters, '_' and '-'"

  Scenario: in memoriam Ian Murdock
     When I sign up as "IanMurdock"
      And I visit "/ianMURDOCK"
     Then I get a 301 redirect to "/IanMurdock"

  Scenario: user info
    Given I am signed in
     When I query /api/me
     Then my "login" is "testuser"
      And my "email" is "testuser@jovilag.hu"

  Scenario: modify user info
    Given I am signed in
     When I change my "email" to "nextgeneration@jovilag.hu"
     Then I get a 200 OK
      And my "login" is "testuser"
      And my "email" is "nextgeneration@jovilag.hu"

  Scenario: modify user info with reload
    Given I am signed in
     When I change my "email" to "something.different@jovilag.hu"
      And I query /api/me
     Then I get a 200 OK
      And my "login" is "testuser"
      And my "email" is "something.different@jovilag.hu"

  Scenario: try to modify user login
    Given I am signed in
     When I change my "login" to "littleme"
     Then I get a 400 error
      And the error message is "invalid field"

  Scenario: create page over REST
    Given I am signed in
     When I create a page called "mokus" with description "fenn a fan"
     Then I get a 200 OK
      And I can view the page called "mokus" with description "fenn a fan"

  Scenario: cannot create page if the user exists with the same name
    Given I am signed in
     When I create a page called "testUSER" with description "Whatsup"
     Then I get a 400 error
      And the error message is "this name is already taken"

  Scenario: cannot signup if page exists with the same name
    Given I am signed in
     When I create a page called "pWer" with description "soka"
      And I log out
      And I sign up as "PweR"
     Then I get a 400 error
      And the error message is "this name is already taken"

  Scenario: page permalink redirection works
    Given I am signed in
     When I create a page called "Capitaly" with description "nope"
      And I visit "/capitaly"
     Then I get a 301 redirect to "/Capitaly"

  Scenario: create invalid page over REST
    Given I am signed in
     When I create a page called "mokusssssssssssssssssssssssssss" with description "fenn a fan"
     Then I get a 400 error
      And Value of "name" is invalid because "name is too long"

  Scenario: create page with invalid field
    Given I am signed in
     When I create a page with an invalid field
     Then I get a 400 error
      And the error message is "invalid field"

  Scenario: modify page over REST
    Given I am signed in
      And Page records are cleaned from the database
     When I create a page called "mokus" with description "fenn a fan"
      And I modify the page description to "hello vilag"
     Then I get a 200 OK
      And I can view the page called "mokus" with description "hello vilag"

  Scenario: modify page over REST with another user
    Given I am signed in
      And Page records are cleaned from the database
     When I create a page called "mokus" with description "fenn a fan"
      And I log out
      And I sign up as "black"
      And I log in as "black"
      And I modify the page description to "hello vilag"
     Then I get a 403 error
      And the error message is "permission denied"

  Scenario: modify invalid field of a page over REST
    Given I am signed in
      And Page records are cleaned from the database
     When I create a page called "mokus" with description "fenn a fan"
      And I modify the page invalid_field to "not really"
     Then I get a 400 error
      And I can view the page called "mokus" with description "fenn a fan"

  Scenario: modify page without data returns error
    Given I am signed in
      And Page records are cleaned from the database
      And There is a page called "mokus" with description "fenn a fan"
     When I modify the page without request body
     Then I get a 400 error
      And the error message is "missing request body"

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

  Scenario: delete page over REST with another user
    Given I am signed in
      And Page records are cleaned from the database
      And There is a page called "mokus" with description "fenn a fan"
     When I log out
      And I log in as "black"
      And I delete the page
     Then I get a 403 error
      And the error message is "permission denied"

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
      And Page records are cleaned from the database
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
      And the comment created time is just now
      And the comment modified time is just now
      And the post has 1 comment "not really"

  Scenario: modify a comment with other user
    Given I am signed in
      And I have a post
      And I have a comment on the post
     When I log out
      And I log in as "black"
      And I modify the comment to "not really"
     Then I get a 403 error
      And the error message is "permission denied"
