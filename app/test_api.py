from fastapi.testclient import TestClient

import sys

sys.path.insert(0, "..")

try:
    from main import app
except ImportError:
    print('No Import')

client = TestClient(app)


def test_learners_get_user():
    user_id = "962cec7f-9fe7-41ff-8a9a-544110247e7d"
    response = client.get(f"/api/v1/learners/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": "962cec7f-9fe7-41ff-8a9a-544110247e7d",
        "is_active": True,
        "is_superuser": False,
        "car_type": "string",
        "full_name": "string",
        "email": "string",
        "phone_number": "string",
        "date_of_birth": "2021-01-19",
        "address": "string",
        "profile_image_one": None
    }


def test_instructors_get_user():
    user_id = "3060ea30-ba8c-48d9-b8b9-167cf7b5c132"
    response = client.get(f"/api/v1/instructors/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": "3060ea30-ba8c-48d9-b8b9-167cf7b5c132",
        "full_name": "s",
        "phone_number": "s",
        "email": "dsadsa",
        "is_active": True,
        "is_superuser": False,
        "sex": "s",
        "car_type": "dosa",
        "area_covered": "s",
        "driving_school_name": "s",
        "driving_school_description": None,
        "adi_license": "codebase-w_payment.png",
        "profile_image_one": "codebase-w_payment.png",
        "profile_image_two": None,
        "profile_image_three": None
    }


def test_create_existing_learner():
    response = client.post("/api/v1/learners/", json={
        "sex": "Male",
        "car_type": "Manual",
        "full_name": "Sharjeel",
        "email": "string",
        "phone_number": "string",
        "date_of_birth": "2021-05-19",
        "hashed_password": "string",
        "address": "string"
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_create_new_learner():
    import uuid;
    test_email = "test__" + str(uuid.uuid4())

    response = client.post("/api/v1/learners/", json={
        "sex": "string",
        "car_type": "string",
        "full_name": "string",
        "email": test_email,
        "phone_number": "string",
        "date_of_birth": "2021-05-19",
        "hashed_password": "string",
        "address": "string"
    })

    assert response.status_code == 200

    """
    This is a bit of a sticky one, code will need to be modified to cater 
    for generated uuid & hashed_password
    """

    assert response.json() == {
        "full_name": "string",
        "date_of_birth": "2021-05-19",
        "car_type": "string",
        "is_superuser": False,
        "hashed_password": "$2b$12$LCLf4T1FjBS7goREwrzVqe5obBWK2MP0WcIHd/Mo5OvbpbPjJTvWC",
        "phone_number": "string",
        "id": "b9248dca-7a57-4af1-861d-b7d4613ee5fc",
        "address": "string",
        "profile_image_one": None,
        "sex": "Male",
        "is_active": True,
        "email": test_email
    }

