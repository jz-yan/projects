Feature: Servv.ai meetings

    Scenario: Valid meeting
        Given I click on Create Meeting
        When I fill in one-time meeting data, All Valid
        Then I should see successful dialogue alert
    
    Scenario: Missing topic
        Given I click on Create Meeting
        When I fill in one-time meeting data, Missing Topic
        Then I should see "The topic field is required." on screen
    
    Scenario: Topic name length exceeds limit
        Given I click on Create Meeting
        When I fill in one-time meeting data, >200 Char Topic
        Then I should see "The topic field may not be greater than 200 characters." on screen
    