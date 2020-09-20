Feature: Servv.ai billing

    Scenario: Upgrade current plan
        Given I am on the Billing page
        When I activate Superstar plan
        And I approve the subscription
        Then I should see Superstar plan activated

    Scenario: Downgrade current plan
        Given I am on the Billing page
        When I activate Star plan
        And I approve the subscription
        Then I should see Star plan activated

    Scenario: Test plan switch from Star to All Star
        Given I am subscribed to "Star" plan
        When I change to "All Star" plan
        And I create 1 recurring meetings, Recurring
        Then I should see no error on the last meeting
        And I delete all meetings

    Scenario: Test plan switch from Star to Superstar
        Given I am subscribed to "Star" plan
        When I create 1 recurring meetings, Recurring
        And I change to "Superstar" plan
        When I create 1 recurring meetings, Recurring
        Then I should see no error on the last meeting
        And I delete all meetings

    Scenario: Test plan switch from All Star to Star
        Given I am subscribed to "All Star" plan
        And I create 5 recurring meetings, Recurring
        When I change to "Star" plan
        And I create 1 recurring meetings, Recurring
        Then I should see error on the last meeting

    Scenario: Test plan switch from All Star to Superstar
        Given I am subscribed to "All Star" plan
        When I change to "Superstar" plan
        And I create 6 recurring meetings, Recurring
        Then I should see no error on the last meeting
        And I delete all meetings

    Scenario: Test plan switch from Superstar to All Star
        Given I am subscribed to "Superstar" plan
        And I create 15 recurring meetings, Recurring
        When I change to "All Star" plan
        And I create 1 recurring meetings, Recurring
        Then I should see error on the last meeting

    Scenario: Test plan switch from Superstar to Star
        Given I am subscribed to "Superstar" plan
        When I change to "Star" plan
        And I create 1 recurring meetings, Recurring
        Then I should see error on the last meeting
        And I delete all meetings