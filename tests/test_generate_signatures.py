import os
import sys
import json
import pytest
from unittest import mock
from scripts import generate_signatures

TEST_USERS = [
    {
        'DisplayName': 'Test User',
        'GivenName': 'Test',
        'Surname': 'User',
        'UserPrincipalName': 'test.user@example.com',
        'JobTitle': 'Tester',
        'Department': 'QA',
        'OfficeLocation': 'HQ',
        'BusinessPhones': ['123-456-7890'],
        'MobilePhone': '555-555-5555',
        'CompanyName': 'TestCo',
        'WebsiteUrl': 'https://example.com',
        'Pronouns': 'they/them',
        'PhotoUrl': '',
    }
]

@pytest.fixture
def tmp_users_json(tmp_path):
    users_path = tmp_path / 'users.json'
    with open(users_path, 'w', encoding='utf-8') as f:
        json.dump(TEST_USERS, f)
    return str(users_path)

@pytest.fixture
def tmp_template(tmp_path):
    template_dir = tmp_path / 'templates'
    template_dir.mkdir()
    template_path = template_dir / 'signature_template.html'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write('<div>{{ display_name }}</div>')
    return str(template_dir)

def test_load_users_success(tmp_users_json, monkeypatch):
    monkeypatch.setattr(generate_signatures, 'DATA_PATH', tmp_users_json)
    users = generate_signatures.load_users()
    assert users[0]['DisplayName'] == 'Test User'

def test_load_users_missing(monkeypatch):
    monkeypatch.setattr(generate_signatures, 'DATA_PATH', 'nonexistent.json')
    with pytest.raises(SystemExit):
        generate_signatures.load_users()

def test_template_missing(tmp_users_json, tmp_path, monkeypatch):
    monkeypatch.setattr(generate_signatures, 'DATA_PATH', tmp_users_json)
    monkeypatch.setattr(generate_signatures, 'TEMPLATE_PATH', str(tmp_path / 'notemplates'))
    with pytest.raises(SystemExit):
        generate_signatures.render_signatures(TEST_USERS, [1])

def test_render_signature_success(tmp_users_json, tmp_template, tmp_path, monkeypatch):
    monkeypatch.setattr(generate_signatures, 'DATA_PATH', tmp_users_json)
    monkeypatch.setattr(generate_signatures, 'TEMPLATE_PATH', tmp_template)
    monkeypatch.setattr(generate_signatures, 'OUTPUT_DIR', str(tmp_path / 'output'))
    users = generate_signatures.load_users()
    generate_signatures.render_signatures(users, [1])
    output_file = os.path.join(tmp_path, 'output', 'test.user@example.com.html')
    assert os.path.isfile(output_file)
    with open(output_file, encoding='utf-8') as f:
        assert 'Test User' in f.read() 