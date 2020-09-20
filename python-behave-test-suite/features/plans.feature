Feature: Plans

    Scenario: Test Star plan recurring event limit
        Given I am subscribed to "Star" plan
        When I create 2 recurring meetings, Recurring
        Then I should see error on the last meeting

    Scenario: Test Star plan recurring event limit after deleting one event
        Given I am subscribed to "Star" plan
        When I delete 1 recurring meetings
        And I create 2 recurring meetings, Recurring
        Then I should see error on the last meeting
        And I delete all meetings

    Scenario: Test All Star plan recurring event limit
        Given I am subscribed to "All Star" plan
        When I create 11 recurring meetings, Recurring
        Then I should see error on the last meeting

    # Scenario: Test plan switch from All Star to Star
    #     Given I am subscribed to "All Star" plan
    #     When I change to "Star" plan
    #     And I create 1 recurring meetings, Recurring
    #     Then I should see error on the last meeting

    # Scenario: Test plan switch from All Star to Superstar
    #     Given I am subscribed to "All Star" plan
    #     When I change to "Superstar" plan
    #     And I create 1 recurring meetings, Recurring
    #     Then I should see no error on the last meeting
    #     And I delete all meetings

    Scenario: Test All Star plan recurring event limit after deleting one event
        Given I am subscribed to "All Star" plan
        When I delete 1 recurring meetings, Recurring
        And I create 11 recurring meetings, Recurring
        Then I should see error on the last meeting
        And I delete all meetings

    Scenario: Test Superstar plan recurring event limit
        Given I am subscribed to "Superstar" plan
        When I create 15 recurring meetings, Recurring
        Then I should see no error on the last meeting
        And I delete all meetings

    # Scenario: Test plan switch from Superstar to All Star
    #     Given I am subscribed to "Superstar" plan
    #     When I change to "All Star" plan
    #     And I create 1 recurring meetings, Recurring
    #     Then I should see error on the last meeting

    # Scenario: Test plan switch from Superstar to Star
    #     Given I am subscribed to "Superstar" plan
    #     When I change to "Star" plan
    #     And I create 1 recurring meetings, Recurring
    #     Then I should see error on the last meeting

    # Scenario: Test delete occurred meeting for Star plan
    #     Given I am subscribed to "Star" plan
    #     When I create 1 recurring meetings, Recurring Now
    #     And I delete all meetings
    #     When I create 1 recurring meetings, Recurring Now
    #     Then I should see dialogue alert "Temporary dialogue alert"





    