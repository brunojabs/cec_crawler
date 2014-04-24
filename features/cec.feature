Feature: Search product
    Extract products from CEC site

    Scenario: Check for product "tijolo"
        Given I search for "tijolo"
        When I check first product
        Then I see the result "Tijolo Refratário 11,5x23x5,1cm -"

    Scenario: Search for "tijolo"
        Given I search for "tijolo"
        When I run the crawler
        Then I see the result "54 products found"

    Scenario: Search for "telha"
        Given I search for "telha"
        When I run the crawler
        Then I see the result "123 products found"

    Scenario: Search for "pia"
        Given I search for "pia"
        When I run the crawler
        Then I see the result "672 products found"