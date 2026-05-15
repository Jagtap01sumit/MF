class QUANTConfig:

    URL = "https://quantmutual.com/statutory-disclosures"

    MONTHLY_PORTFOLIO_XPATH = (
        "//span[text()='MONTHLY PORTFOLIO']"
    )
    YEAR_XPATH=("(//div[contains(@class,'statutory disclouser')] [.//span[text()='MONTHLY PORTFOLIO']] /following-sibling::div[1][1]//li[1])[1]");
    MONTH_XPATH=("(//div[contains(@class,'statutory disclouser')] [.//span[text()='MONTHLY PORTFOLIO']] /following-sibling::div[1][1]//li[1])//a");
   