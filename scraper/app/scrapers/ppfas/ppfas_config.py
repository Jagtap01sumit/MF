class PPFASConfig:

    URL = "https://amc.ppfas.com/downloads/factsheet/"

    MONTHLY_PORTFOLIO_XPATH = "//*[@class='sidebarlinks']/a[text()='Monthly Factsheets']"
    YEAR_XPATH = "(//*[@role='tablist']//li[@class='nav-item'])[1]/a"
    MONTH_XPATH = "(//*[@id='accordion']/div/div[2][@class='collapse show'][1])[1]//a[3]"
    COLLAPSE_XPATH ="(//*[@id='accordion']/div/div[2][@class='collapse'][1])[1]"