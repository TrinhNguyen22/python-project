from fastapi.testclient import TestClient


def test_list_users(client: TestClient, admin_token, created_user):
    r = client.get(
        "/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    users = r.json()
    assert isinstance(users, list)
    assert any(u["username"] == created_user["username"] for u in users)


def test_get_user_detail(client: TestClient, admin_token, created_user):
    r = client.get(f"/users/{created_user['id']}",
                   headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200
    user = r.json()
    assert user["username"] == created_user["username"]


def test_update_user(client: TestClient, admin_token, created_user):
    update_data = {"first_name": "Updated", "last_name": "Name"}
    r = client.put(
        f"/users/{created_user['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    body = r.json()
    assert body["first_name"] == update_data["first_name"]
    assert body["last_name"] == update_data["last_name"]


# def test_delete_user(
#     client: TestClient,
#     admin_token,
#     create_user_to_be_deleted
# ):
#     r = client.delete(
#         f"/users/{create_user_to_be_deleted['id']}",
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )
#     assert r.status_code == 204
