from database.DB.procedures.crud.operation import (
    get_or_create_amc,
    get_or_create_scheme,
    get_or_create_industry,
    get_or_create_stock,
    insert_portfolio,
)


class PortfolioProcessor:

    def process(self, df):

        for _, row in df.iterrows():

            amc_id = get_or_create_amc(row["amc_name"])

            scheme_id = get_or_create_scheme(
                amc_id, row["scheme_code"], row.get("scheme_name"),row.get("fund_type")
            )

            industry_id = get_or_create_industry(row["industry"])

            stock_id = get_or_create_stock(
                isin=row["isin"], stock_name=row["stock_name"], industry_id=industry_id
            )

            insert_portfolio(
                scheme_id=scheme_id,

                stock_id=stock_id,
                report_month=row["report_month"],
                quantity=row["quantity"],
                market_value=row["market_value"],
            )
