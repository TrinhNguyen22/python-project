from fastapi.testclient import TestClient


def test_list_tasks(client: TestClient, admin_token, created_task):
    r = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    tasks = r.json()
    assert any(t["id"] == created_task['id'] for t in tasks)


def test_get_task_detail(client: TestClient, admin_token, created_task):
    r = client.get(
        f"/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    task = r.json()
    assert task["id"] == created_task['id']


def test_update_task(client: TestClient, admin_token, created_task):
    update_data = {"status": "done", "priority": 3}
    r = client.put(
        f"/tasks/{created_task['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == update_data["status"]
    assert body["priority"] == update_data["priority"]


# def test_delete_task(
#     client: TestClient,
#     admin_token,
#     create_task_to_be_deleted
# ):
#     r = client.delete(
#         f"/tasks/{create_task_to_be_deleted['id']}",
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )
#     assert r.status_code == 204
