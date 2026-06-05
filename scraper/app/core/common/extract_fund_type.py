import pandas as pd

def extract_fund_type(scheme_name):

    scheme_name = scheme_name.lower()

    if "small cap" in scheme_name:
        return "Small Cap"
    
    if "large & mid" in scheme_name:
        return "Large & Mid"
    
    if "mid & large" in scheme_name:
        return "Large & Mid"

    if "mid cap" in scheme_name:
        return "Mid Cap"

    if "large cap" in scheme_name:
        return "Large Cap"

    if "flexi cap" or "flexcap" in scheme_name:
        return "Flexi Cap"

    if "multi cap" in scheme_name:
        return "Multi Cap"

    if "index fund" in scheme_name:
        return "Index Fund"

    if "etf" in scheme_name:
        return "ETF"

    return "Other"