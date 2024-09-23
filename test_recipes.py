from main import app
from fastapi.testclient import TestClient
from pathlib import Path


def test_recipe():
    test_client = TestClient(app)
    response = test_client.post(
        "/",
        json={
            "full_text": Path(__file__)
            .parent.joinpath("test", "black-grape-red-wine-sorbet.txt")
            .read_text()
        },
    )
    assert response.json()["Ingredient"] == "Grape"
