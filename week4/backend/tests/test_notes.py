def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note(client):
    # Arrange - Create a note first
    payload = {"title": "Original Title", "content": "Original Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Act - Update the note
    update_payload = {"title": "Updated Title", "content": "Updated Content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)

    # Assert - Verify update succeeded
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"


def test_update_note_not_found(client):
    # Act - Try to update a non-existent note
    update_payload = {"title": "Updated", "content": "Updated"}
    r = client.put("/notes/99999", json=update_payload)

    # Assert - Should return 404
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_update_note_partial(client):
    # Arrange - Create a note
    payload = {"title": "Original", "content": "Original"}
    r = client.post("/notes/", json=payload)
    note_id = r.json()["id"]

    # Act - Update only title (partial update)
    update_payload = {"title": "New Title"}
    r = client.put(f"/notes/{note_id}", json=update_payload)

    # Assert - Title updated, content unchanged
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "Original"
