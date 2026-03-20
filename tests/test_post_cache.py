from fastapi.testclient import TestClient
from app.main import app
from app.core.redis import redis_client
from app.repositories.post_repository import PostRepository


def test_post_caching(monkeypatch):
    with TestClient(app) as client:
        redis_client.flushdb()

        create_response = client.post("/posts/", json={
            "title": "test",
            "content": "test content"
        })
        assert create_response.status_code == 200

        post_id = create_response.json()["id"]

        cache_key = f"post:{post_id}"
        cached_before = redis_client.get(cache_key)
        assert cached_before is None

        response1 = client.get(f"/posts/{post_id}")
        assert response1.status_code == 200

        cached_after = redis_client.get(cache_key)
        assert cached_after is not None

        original_get_by_id = PostRepository.get_by_id
        def _fail_get_by_id(*args, **kwargs):
            raise AssertionError("DB queried on cache hit")
        monkeypatch.setattr(PostRepository, "get_by_id", _fail_get_by_id)

        response2 = client.get(f"/posts/{post_id}")

        monkeypatch.setattr(PostRepository, "get_by_id", original_get_by_id)

        assert response2.status_code == 200
        assert response1.json() == response2.json()

        delete_response = client.delete(f"/posts/{post_id}")
        assert delete_response.status_code == 200
