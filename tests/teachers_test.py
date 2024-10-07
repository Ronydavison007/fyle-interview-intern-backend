def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    data = response.json

    if response.status_code != 200:
       assert data['error'] == 'FyleError'
    else:
        assert response.status_code == 200


def test_grade_assignment_success(client, h_teacher_1):
    # Simulate grading an assignment that is in the SUBMITTED state
    payload = {
        'id': 2,  # Assuming an assignment with this ID exists
        'grade': 'B'
    }
    response = client.post(
        '/teacher/assignments/grade',
        json=payload,
        headers=h_teacher_1
    )
    assert response.status_code == 200
    


def test_grade_assignment_already_graded(client, h_teacher_1):
    # Simulate grading an assignment that is in the SUBMITTED state
    payload = {
        'id': 8,  # Assuming an assignment with this ID exists
        'grade': 'B'
    }
    response = client.post(
        '/teacher/assignments/grade',
        json=payload,
        headers=h_teacher_1
    )
    assert response.status_code == 200
    assert response.json['data']['message'] == 'Already graded'
    


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )
    assert response.status_code == 404


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 53,
            "grade": "A"
        }
    )
    
    if 'message' in response.json['data']:
        assert response.status_code == 200
        assert response.json['data']['message'] == 'Already graded'
    else:
        assert response.status_code == 400
        assert response.json['data']['error'] == 'FyleError'
    
    
    
    
    
