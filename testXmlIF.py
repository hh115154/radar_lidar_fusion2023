import xml.dom.minidom

dom = xml.dom.minidom.parse('db.xml')
root = dom.documentElement      # 获得根节点
print(root.nodeName)            # 节点名称 dbconfig

# 获取mysql节点
mysql_node = root.getElementsByTagName('mysql')[0]
for node in mysql_node.childNodes:
    if node.nodeType == 1:   # ELEMENT_NODE
        print(node.nodeName, node.firstChild.data)


# def writeXML():
# 	domTree = parse("./customer.xml")
# 	# 文档根元素
# 	rootNode = domTree.documentElement
#
# 	# 新建一个customer节点
# 	customer_node = domTree.createElement("customer")
# 	customer_node.setAttribute("ID", "C003")
#
# 	# 创建name节点,并设置textValue
# 	name_node = domTree.createElement("name")
# 	name_text_value = domTree.createTextNode("kavin")
# 	name_node.appendChild(name_text_value)  # 把文本节点挂到name_node节点
# 	customer_node.appendChild(name_node)
#
# 	# 创建phone节点,并设置textValue
# 	phone_node = domTree.createElement("phone")
# 	phone_text_value = domTree.createTextNode("32467")
# 	phone_node.appendChild(phone_text_value)  # 把文本节点挂到name_node节点
# 	customer_node.appendChild(phone_node)
#
# 	# 创建comments节点,这里是CDATA
# 	comments_node = domTree.createElement("comments")
# 	cdata_text_value = domTree.createCDATASection("A small but healthy company.")
# 	comments_node.appendChild(cdata_text_value)
# 	customer_node.appendChild(comments_node)
#
# 	rootNode.appendChild(customer_node)
#
# 	with open('added_customer.xml', 'w') as f:
# 		# 缩进 - 换行 - 编码
# 		domTree.writexml(f, addindent='  ', encoding='utf-8')
#
# if __name__ == '__main__':
# 	writeXML()
