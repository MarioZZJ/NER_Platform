from flask import Flask,render_template,request
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher,walk
from config_params import params

app = Flask(__name__)
url, auths = params()
graph = Graph(url, auth=auths)

@app.route('/')
def hello_world():
    return render_template('graph-simple.html')

@app.route('/querysample',methods=['POST'])
def query():
    if(request.form['field']=="人物"):
        query = request.form['query']
        matcher = NodeMatcher(graph)
        node = matcher.match("Person_entity", name=query).first()
        if node:
            matcher = RelationshipMatcher(graph)
            relations = matcher.match({node}).limit(10)
            nodes = [node["name"]]
            edges = []
            for relation in relations:
                nodes.append(relation.start_node["name"])
                nodes.append(relation.end_node["name"])
                edges.append({"source":relation.start_node["name"],"target":relation.end_node['name'], "value":type(relation).__name__, "texts":relation['content']})
            nodes = list(set(nodes))
            node_set = []
            for n in nodes:
                node_set.append({"name":n})
            print(request.form)
            print("查询成功")
            return {"data": node_set,"links": edges}
        else:
            print(request.form)
            print("查询失败！")
            return ""
    else:
        print(request.form)
        print("查询失败！")
        return ""

if __name__ == '__main__':
    app.run()

