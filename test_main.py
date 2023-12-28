from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_books_default_pagination():
    # Test the endpoint with default pagination values (page=1, per_page=3)
    response = client.get("/book/")
    assert response.status_code == 200
    assert len(response.json()) == 3  # Assuming default per_page is 3

def test_list_books_custom_pagination():
    # Test the endpoint with custom pagination values (page=2, per_page=3)
    response = client.get("/book?page=2&per_page=5")
    assert response.status_code == 200

    # Check if the returned data corresponds to the expected page
    returned_data = response.json()
    assert len(returned_data) == 3  # per_page is set to 3
    # You can add additional assertions based on the structure or content of the returned data

    # Check pagination metadata
    pagination_info = response.headers.get("Link")
    assert pagination_info is not None

    # Assuming a simple check for the presence of next and previous links
    assert 'rel="next"' in pagination_info
    assert 'rel="prev"' in pagination_info
    # You may want to parse and validate the actual URLs if needed
    # For example, check if the next link corresponds to the next page in your logic
