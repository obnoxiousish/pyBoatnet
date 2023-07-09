import web
import json

from pymongo import MongoClient

from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

HTTPServer.ssl_adapter = BuiltinSSLAdapter(
    certificate='cert/domain.crt',
    private_key='cert/domain.key'
)

# URLs mapping
urls = (
    '/', 'index',
    '/login', 'login',
    '/logout', 'logout',
    '/agent/report', 'agent_report',
    '/agent/task', 'agent_task',
)

def getCPUID():
    id = secrets.token_hex(32)
    return id

# App and session initialization
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'init': False})
client = MongoClient(port=27017)
db = client.boatnet
web.config.debug = False

render = web.template.render('templates/')

def check_auth_header():
    auth_header = web.ctx.env.get('HTTP_AUTHORIZATION')
    if auth_header != 'cocks123':
        return False
    return True

class index:
    def GET(self):
        if session.get('login'):
            return render.index(render.header())
        else:
            raise web.seeother('/login')

class login:
    def check_credentials(self, username, password):
        # Query the users collection for a user with the provided username and password
        user = db.users.find_one({'username': username, 'password': password})
        if user:
            # User and password match, return True
            return True
        else:
            # No match found
            return False
    
    def GET(self):
        if session.get('login'):
            raise web.seeother('/')
        
        return render.login(header=render.header())
    
    def POST(self):
        i = web.input()
        username = i.get('username')
        password = i.get('password')
        
        print(f'Signing in as {username}:{password}')

        # Check the credentials against your database here
        if self.check_credentials(username, password):
            session.login = True
            session.user = username
            session.error_message = None
            return web.seeother('/')
        else:
            return render.login(header=render.header(error_message='Invalid credentials'))
        
class agent_report:
    def POST(self):
        if not check_auth_header():
            return json.dumps({"error": "Unauthorized access"})

        data = web.data()  # get POST data
        status_info = json.loads(data)  # assuming it's JSON data
        status = status_info['status']

        # Get the agent_id from the 'X-Agent-ID' header
        agent_id = web.ctx.env.get('HTTP_X_AGENT_ID')
        
        print(f'Agent {agent_id} reported status {status}')
        
        if not agent_id:
            return json.dumps({"error": "Missing 'X-Agent-ID' header"})

        # Update the agent's status in your database, if agent doesn't exist insert a new one
        db.agents.update_one({'agentId': agent_id}, {'$set': {'status': status}}, upsert=True)
        return json.dumps({"message": "Status updated successfully"})


class agent_task:
    def GET(self):
        if not check_auth_header():
            return json.dumps({"error": "Unauthorized access"})

        # Get the agent_id from the 'X-Agent-ID' header
        agent_id = web.ctx.env.get('HTTP_X_AGENT_ID')
        
        if not agent_id:
            return json.dumps({"error": "Missing 'X-Agent-ID' header"})

        # Retrieve all tasks from the database
        all_tasks = db.tasks.find({})

        tasks_to_return = []
        for task in all_tasks:
            assigned_to_agents = task.get('assignedToAgents', [])

            # If the agent is not already assigned to this task, assign it
            if agent_id not in assigned_to_agents:
                assigned_to_agents.append(agent_id)
                db.tasks.update_one({'_id': task['_id']}, {'$set': {'assignedToAgents': assigned_to_agents}})
                tasks_to_return.append(task)

        if not tasks_to_return:
            tasks_to_return = {'tasks': [{'task': None}]}

        return json.dumps(tasks_to_return)  # return tasks as JSON


class logout:
    def GET(self):
        try:
            session.kill()
            raise web.seeother('/')
        except:
            raise web.seeother('/login')

if __name__ == "__main__":
    app.run()
