from fastapi.testclient import TestClient


def test_list_companies(client: TestClient, admin_token, created_company):
    r = client.get(
        "/companies",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    companies = r.json()
    assert any(c["id"] == created_company['id'] for c in companies)


def test_get_company_detail(client: TestClient, admin_token, created_company):
    r = client.get(
        f"/companies/{created_company['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    company = r.json()
    assert company["id"] == created_company['id']


def test_update_company(client: TestClient, admin_token, created_company):
    update_data = {"description": "Updated description", "rating": 5}
    r = client.put(
        f"/companies/{created_company['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    company = r.json()
    assert company["description"] == update_data["description"]
    assert company["rating"] == update_data["rating"]


def test_delete_company(
    client: TestClient,
    admin_token,
    create_company_to_be_deleted,
    create_user_to_be_deleted,
    create_task_to_be_deleted
):
    tasks = client.delete(
        f"/tasks/{create_task_to_be_deleted['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert tasks.status_code == 204

    users = client.delete(
        f"/users/{create_user_to_be_deleted['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert users.status_code == 204

    companies = client.delete(
        f"/companies/{create_company_to_be_deleted['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert companies.status_code == 204


