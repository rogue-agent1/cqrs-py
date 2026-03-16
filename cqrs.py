class Command:
    def __init__(s, name, data): s.name=name;s.data=data
class Query:
    def __init__(s, name, params=None): s.name=name;s.params=params or{}
class CommandBus:
    def __init__(s): s.handlers={}; s.log=[]
    def register(s, name, handler): s.handlers[name] = handler
    def dispatch(s, cmd):
        handler = s.handlers.get(cmd.name)
        if not handler: raise ValueError(f"No handler for {cmd.name}")
        result = handler(cmd.data); s.log.append(cmd); return result
class QueryBus:
    def __init__(s): s.handlers={}
    def register(s, name, handler): s.handlers[name] = handler
    def query(s, q):
        handler = s.handlers.get(q.name)
        if not handler: raise ValueError(f"No handler for {q.name}")
        return handler(q.params)
class App:
    def __init__(s):
        s.cmd_bus = CommandBus(); s.query_bus = QueryBus(); s.store = {}
        s.cmd_bus.register("create_user", s._create_user)
        s.cmd_bus.register("update_user", s._update_user)
        s.query_bus.register("get_user", s._get_user)
        s.query_bus.register("list_users", s._list_users)
    def _create_user(s, data): s.store[data["id"]] = data; return data["id"]
    def _update_user(s, data):
        if data["id"] in s.store: s.store[data["id"]].update(data); return True
        return False
    def _get_user(s, params): return s.store.get(params.get("id"))
    def _list_users(s, params): return list(s.store.values())
def demo():
    app = App()
    app.cmd_bus.dispatch(Command("create_user", {"id": 1, "name": "Alice"}))
    app.cmd_bus.dispatch(Command("create_user", {"id": 2, "name": "Bob"}))
    app.cmd_bus.dispatch(Command("update_user", {"id": 1, "name": "Alice Smith"}))
    user = app.query_bus.query(Query("get_user", {"id": 1}))
    print(f"User 1: {user}")
    users = app.query_bus.query(Query("list_users"))
    print(f"All users: {users}")
    print(f"Commands executed: {len(app.cmd_bus.log)}")
if __name__ == "__main__": demo()
