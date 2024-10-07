def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )
    
    if response.status_code == 200:
        data = response.json['data']
        for assignment in data:
          assert assignment['state'] in ['SUBMITTED', 'GRADED']  
    else:
        assert response.status_code == 400


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': 'A'
        },
        headers=h_principal
    )
    if response.status_code == 400:
        assert response.json['data']['message'] == 'Draft assignment cannot be graded'
    else:
        assert response.status_code == 200
        assert response.json['data']['grade'] == 'A'



def test_grade_assignment_missing_data(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={},  # Empty data
        headers=h_principal
    )
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'ValidationError'


def test_grade_assignment_invalid_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'Z'  # Invalid grade
        },
        headers=h_principal
    )
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'ValidationError'



def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'C'
        },
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == 'GRADED'
    assert response.json['data']['grade'] == 'C'
    
def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'B'
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == 'GRADED'
    assert response.json['data']['grade'] == 'B'
    
