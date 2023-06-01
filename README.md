# request 표준
## POST url/<action_name>
```json
{
    "sender": "chanhee",
    "content": {
        "to": "seungpyo",
        "message": "hello",
        "debug": true,
        "mention": ["seungpyo", "chanhee", "ChatGPT"]
    }
}
```
# response 표준
```json
{
    "status": 200,
    "content": "안녕"
}
```
