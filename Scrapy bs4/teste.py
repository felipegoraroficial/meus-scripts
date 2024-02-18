import pytest
import extrair

def test_request_and_list():
    status_code, list_todos = extrair.get_data()

    # Verifique se o status do request é 200
    assert status_code == 200, "O status do request não é 200"

    # Verifique se a lista 'list_todos' não está vazia
    assert list_todos, "A lista 'list_todos' está vazia"