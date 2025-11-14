import pytest
from fastapi.testclient import TestClient

from app.main import app, get_db


@pytest.fixture(autouse=True)
def override_db_dependency():
    # provide a dummy async dependency that yields None for the AsyncSession
    async def _override_get_db():
        yield None

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


def test_list_programs(monkeypatch):
    # fake async function to return program list
    async def fake_get_all(db, skip=0, limit=100):
        return [{"id": 1, "program_name": "Test Program", "program_code": "TP", "cal_year": 2025}]

    monkeypatch.setattr('app.crud.program.get_all', fake_get_all)

    client = TestClient(app)
    resp = client.get('/programs')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]['program_name'] == 'Test Program'


def test_create_program(monkeypatch):
    # fake async create that echoes back the created object with an id
    async def fake_create(db, obj_in):
        d = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else dict(obj_in)
        d['id'] = 42
        return d

    monkeypatch.setattr('app.crud.program.create', fake_create)

    client = TestClient(app)
    payload = {"program_name": "New", "program_code": "N", "cal_year": 2025}
    resp = client.post('/programs', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == 42
    assert data['program_name'] == 'New'


def test_list_survey_types(monkeypatch):
    async def fake_get_all(db, skip=0, limit=100):
        return [{"survey_type_cd": "ST1", "survey_type_desc": "Type 1"}]

    monkeypatch.setattr('app.crud.survey_type.get_all', fake_get_all)

    client = TestClient(app)
    resp = client.get('/survey_types')
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]['survey_type_cd'] == 'ST1'


def test_get_program(monkeypatch):
    async def fake_get_detail(db, id):
        return {"id": id, "program_name": "Test Program", "program_code": "TP", "cal_year": 2025}

    monkeypatch.setattr('app.crud.program.get_detail', fake_get_detail)
    client = TestClient(app)
    resp = client.get('/programs/1')
    assert resp.status_code == 200
    assert resp.json()['id'] == 1


def test_patch_program(monkeypatch):
    async def fake_get(db, id):
        return {"id": id, "program_name": "Old", "program_code": "O", "cal_year": 2024}

    async def fake_update(db, db_obj, payload):
        data = payload.model_dump() if hasattr(payload, 'model_dump') else dict(payload)
        data['id'] = db_obj['id']
        return data

    monkeypatch.setattr('app.crud.program.get', fake_get)
    monkeypatch.setattr('app.crud.program.update', fake_update)

    client = TestClient(app)
    resp = client.patch('/programs/1', json={"program_name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()['program_name'] == 'Updated'


def test_list_surveys(monkeypatch):
    async def fake_get_all(db, skip=0, limit=100):
        return [{"id": 10, "title": "S1", "survey_type_cd": "ST1", "cal_year": 2025}]

    monkeypatch.setattr('app.crud.survey.get_all', fake_get_all)
    client = TestClient(app)
    resp = client.get('/surveys')
    assert resp.status_code == 200
    assert resp.json()[0]['id'] == 10


def test_get_survey(monkeypatch):
    async def fake_get_detail(db, id):
        return {"id": id, "title": "S1", "survey_type_cd": {"survey_type_cd": "ST1", "survey_type_desc": "Type 1"}, "cal_year": 2025}

    monkeypatch.setattr('app.crud.survey.get_detail', fake_get_detail)
    client = TestClient(app)
    resp = client.get('/surveys/10')
    assert resp.status_code == 200
    assert resp.json()['id'] == 10


def test_create_survey(monkeypatch):
    async def fake_create(db, obj_in):
        d = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else dict(obj_in)
        d['id'] = 99
        return d

    monkeypatch.setattr('app.crud.survey.create', fake_create)
    client = TestClient(app)
    payload = {"title": "New Survey", "survey_type_cd": "ST1", "cal_year": 2025}
    resp = client.post('/surveys', json=payload)
    assert resp.status_code == 200
    assert resp.json()['id'] == 99


def test_patch_survey(monkeypatch):
    async def fake_get(db, id):
        return {"id": id, "title": "Old Survey", "survey_type_cd": "ST1", "cal_year": 2024}

    async def fake_update(db, db_obj, payload):
        data = payload.model_dump() if hasattr(payload, 'model_dump') else dict(payload)
        data['id'] = db_obj['id']
        return data

    monkeypatch.setattr('app.crud.survey.get', fake_get)
    monkeypatch.setattr('app.crud.survey.update', fake_update)

    client = TestClient(app)
    resp = client.patch('/surveys/10', json={"title": "Updated Survey"})
    assert resp.status_code == 200
    assert resp.json()['title'] == 'Updated Survey'


def test_get_survey_type(monkeypatch):
    async def fake_get_detail(db, code):
        return {"survey_type_cd": code, "survey_type_desc": "Desc"}

    monkeypatch.setattr('app.crud.survey_type.get_detail', fake_get_detail)
    client = TestClient(app)
    resp = client.get('/survey_types/ST1')
    assert resp.status_code == 200
    assert resp.json()['survey_type_cd'] == 'ST1'


def test_create_survey_type(monkeypatch):
    async def fake_create(db, obj_in):
        d = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else dict(obj_in)
        return d

    monkeypatch.setattr('app.crud.survey_type.create', fake_create)
    client = TestClient(app)
    payload = {"survey_type_cd": "STX", "survey_type_desc": "X"}
    resp = client.post('/survey_types', json=payload)
    assert resp.status_code == 200
    assert resp.json()['survey_type_cd'] == 'STX'


def test_patch_survey_type(monkeypatch):
    async def fake_get_detail(db, code):
        return {"survey_type_cd": code, "survey_type_desc": "Old"}

    async def fake_update(db, db_obj, payload):
        d = payload.model_dump() if hasattr(payload, 'model_dump') else dict(payload)
        d['survey_type_cd'] = db_obj['survey_type_cd']
        return d

    monkeypatch.setattr('app.crud.survey_type.get_detail', fake_get_detail)
    monkeypatch.setattr('app.crud.survey_type.update', fake_update)

    client = TestClient(app)
    # send partial payload (only the field being updated)
    resp = client.patch('/survey_types/STX', json={"survey_type_desc": "New"})
    assert resp.status_code == 200
    assert resp.json()['survey_type_desc'] == 'New'


def test_list_categories(monkeypatch):
    async def fake_get_all(db, skip=0, limit=100):
        return [{"category_cd": "C1", "category_desc": "Cat1"}]

    monkeypatch.setattr('app.crud.category.get_all', fake_get_all)
    client = TestClient(app)
    resp = client.get('/categories')
    assert resp.status_code == 200
    assert resp.json()[0]['category_cd'] == 'C1'


def test_get_category(monkeypatch):
    async def fake_get_detail(db, code):
        return {"category_cd": code, "category_desc": "Cat"}

    monkeypatch.setattr('app.crud.category.get_detail', fake_get_detail)
    client = TestClient(app)
    resp = client.get('/categories/C1')
    assert resp.status_code == 200
    assert resp.json()['category_cd'] == 'C1'


def test_create_category(monkeypatch):
    async def fake_create(db, obj_in):
        return obj_in.model_dump() if hasattr(obj_in, 'model_dump') else dict(obj_in)

    monkeypatch.setattr('app.crud.category.create', fake_create)
    client = TestClient(app)
    payload = {"category_cd": "C2", "category_desc": "Cat2"}
    resp = client.post('/categories', json=payload)
    assert resp.status_code == 200
    assert resp.json()['category_cd'] == 'C2'


def test_patch_category(monkeypatch):
    async def fake_get_detail(db, code):
        return {"category_cd": code, "category_desc": "Old"}

    async def fake_update(db, db_obj, payload):
        d = payload.model_dump() if hasattr(payload, 'model_dump') else dict(payload)
        d['category_cd'] = db_obj['category_cd']
        return d

    monkeypatch.setattr('app.crud.category.get_detail', fake_get_detail)
    monkeypatch.setattr('app.crud.category.update', fake_update)

    client = TestClient(app)
    # send partial payload (only the field being updated)
    resp = client.patch('/categories/C2', json={"category_desc": "New"})
    assert resp.status_code == 200
    assert resp.json()['category_desc'] == 'New'
