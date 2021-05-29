from flask import Flask,render_template,request
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher,walk,LIKE
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
        print(query)
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
                node_set.append({"name":n,"nodeType":"Person_entity"})
            print(request.form)
            print("查询成功")
            return {"data": node_set,"links": edges, "info":"当前检索策略下，检出 %d 个节点以及 %d 条连边。" % (len(node_set),len(edges))}
        else:
            print(request.form)
            print("查询失败！")
            return {"data": None, "info": "发生错误！请检查您的点击操作是否准确。"}
    elif request.form['field']=="事件":
        query = request.form['query']
        # 在这里可以加一个模糊匹配查询
        matcher = NodeMatcher(graph)
        node = matcher.match("Object", name=query).first()
        if node:
            matcher = RelationshipMatcher(graph)
            relations = matcher.match({node}).limit(10)
            nodes = [node["name"]]
            edges = []
            for relation in relations:
                nodes.append(relation.start_node["name"])
                nodes.append(relation.end_node["name"])
                edges.append({"source": relation.start_node["name"], "target": relation.end_node['name'],
                              "value": relation["type"]})
            nodes = list(set(nodes))
            node_set = []
            for n in nodes:
                node_set.append({"name": n})
            print(request.form)
            print("查询成功")
            return {"data": node_set, "links": edges}
        else:
            print(request.form)
            print("查询失败！")
            return ""
    elif request.form['field']=="关系":
        print(request.form)
        print("查询失败！")
        return ""
    else:
        print(request.form)
        print("查询失败！")
        return ""

@app.route('/querynode',methods=['POST'])
def query_node():
    if request.form['field'] == '人物':
        query = request.form['query']
        matcher = NodeMatcher(graph)
        nodes = matcher.match("Person_entity", name=LIKE(query)).all()
        if nodes:
            node_set = []
            for node in nodes:
                node_set.append({"name": node["name"],"nodeType":"Person_entity"})
            return {"data": node_set, "links": {}, "info":"根据检索条件，共检出 %d 个匹配节点." % len(node_set)}
        else:
            print(request.form)
            print("查询失败！")
            return {"data": None, "info": "根据检索条件，无对应节点被检出。"}






if __name__ == '__main__':
    app.run()
