*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Send 3 References And Download 2
    Go To Send Page
    Select From List By Value  name:type  inCollection
    Click Button  submit
    Send inCollection Reference  Mikael Agricola  Abckiria  1543
        Go To Send Page
    Select From List By Value  name:type  inCollection
    Click Button  submit
    Send inCollection Reference  Mika Waltari  Sinuhe Egyptiläinen  1945
        Go To Send Page
    Select From List By Value  name:type  book
    Click Button  submit
    Send Book Reference  Charles Bukowski  Postitoimisto  Postitoimisto  1971  100-110
        Main Page Should Be Open
        Select Reference  1
        Select Reference  3
        Download Selected References
