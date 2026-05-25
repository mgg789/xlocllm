from xlocllm._server import extract_content, openai_chat_response


def test_extract_content_from_browser_result() -> None:
    assert extract_content({"content": "hello"}) == "hello"
    assert extract_content({"raw": {"choices": [{"message": {"content": "hi"}}]}}) == "hi"


def test_openai_chat_response_shape() -> None:
    response = openai_chat_response({"model": "test-model"}, {"content": "hello"})

    assert response["object"] == "chat.completion"
    assert response["model"] == "test-model"
    assert response["choices"][0]["message"]["content"] == "hello"


def test_openai_chat_response_keeps_rag_extension() -> None:
    response = openai_chat_response(
        {"model": "test-model"},
        {"content": "hello", "raw": {"rag": {"results": [{"id": "a"}]}}},
    )

    assert response["xlocllm"]["rag"]["results"][0]["id"] == "a"
