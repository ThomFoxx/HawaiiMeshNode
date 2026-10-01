from data.zip_request_repository import ZipRequestRepository


zip_request_repository = ZipRequestRepository()


def show_popular_zips(arguments):
    rows = zip_request_repository.get_most_requested()

    if len(rows) == 0:
        print("No ZIP requests have been recorded.")
        return

    print("Most requested ZIP codes:")

    for zip_code, request_count, last_requested in rows:
        print(
            f"  {zip_code} - "
            f"{request_count} requests - "
            f"last: {last_requested}"
        )