from app import create_app



def test_hello_world_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "hello world - Flask API 1"}



def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
