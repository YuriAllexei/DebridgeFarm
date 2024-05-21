from Abstractions import QuoteInfo


def calculate_quote_metrics(quote_info: QuoteInfo):

    src_decimals = quote_info["src_decimals"]

    total_src_amount = int(quote_info["total_src_amount"]) / (10**src_decimals)
    src_operating_expense = int(quote_info["src_operating_expense"]) / (
        10**src_decimals
    )

    dst_recommended_amount = int(quote_info["dst_recommended_amount"]) / (
        10 ** quote_info["dst_decimals"]
    )

    src_token = total_src_amount - src_operating_expense

    revenue = dst_recommended_amount - total_src_amount

    print(f"Source fee: {src_operating_expense}")
    print(f"Margin: {src_token}")
    print(f"Amount received: {dst_recommended_amount}")
    print(f"Revenue: {revenue}")
