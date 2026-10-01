from data.zip_request_repository import ZipRequestRepository


def test_record_zip_request(tmp_path):
    db_path = tmp_path / "test.db"

    repository = ZipRequestRepository(db_path)
    repository.initialize()

    repository.record_request("96814")
    repository.record_request("96814")

    assert repository.get_request_count("96814") == 2

def test_get_most_requested(tmp_path):
    db_path = tmp_path / "test.db"

    repository = ZipRequestRepository(db_path)
    repository.initialize()

    repository.record_request("96814")
    repository.record_request("96814")
    repository.record_request("96734")

    rows = repository.get_most_requested()

    assert rows[0][0] == "96814"
    assert rows[0][1] == 2
    assert rows[1][0] == "96734"
    assert rows[1][1] == 1