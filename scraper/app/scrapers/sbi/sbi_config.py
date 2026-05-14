class SBIConfig:

    URL = "https://www.sbimf.com/portfolios"

    PORTFOLIO_ROW_XPATH = (
        "(//td[contains(normalize-space(),'All Schemes Monthly Portfolio')])[1]"
    )

    XLSX_BUTTON_RELATIVE_XPATH = (
        "/../td[4]"
    )