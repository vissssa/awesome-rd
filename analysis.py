"""
pygraphviz 需要先安装包，具体系统可以去官网http://graphviz.org/download/查看
然后
pip install pygraphviz
即可使用
"""
import os
import sys
import webbrowser
import pygraphviz as pgv


def show_stack(frame=None, slient=False):
    if not frame:
        frame = sys._getframe().f_back

    g = pgv.AGraph(strict=False, directed=True)

    stack = []

    node_set = set()
    subgraph_set = {}

    while frame:
        filename = frame.f_code.co_filename
        firstlineno = frame.f_code.co_firstlineno
        function = frame.f_code.co_name

        node = '{0}:{1}:{2}'.format(filename, firstlineno, function)
        if node not in node_set:
            node_set.add(node)
            if filename not in subgraph_set:
                subgraph_set[filename] = g.add_subgraph(
                    name='cluster' + filename,
                    label=filename
                )
            subgraph = subgraph_set[filename]
            subgraph.add_node(
                node,
                label='{0}:{1}'.format(firstlineno, function)
            )

        stack.append(frame)
        frame = frame.f_back

    stack.reverse()

    len_stack = len(stack)

    for index, start in enumerate(stack):

        if index + 1 < len_stack:
            start_filename = start.f_code.co_filename
            start_firstlineno = start.f_code.co_firstlineno
            start_function = start.f_code.co_name
            start_lineno = start.f_lineno
            start_subgraph = subgraph_set[start_filename]

            end = stack[index + 1]
            end_filename = end.f_code.co_filename
            end_firstlineno = end.f_code.co_firstlineno
            end_function = end.f_code.co_name
            end_subgraph = subgraph_set[end_filename]

            if index == 0:
                color = 'green'
            elif index == len_stack - 2:
                color = 'red'
            else:
                color = 'black'

            g.add_edge(
                '{0}:{1}:{2}'.format(start_filename,
                                     start_firstlineno,
                                     start_function),
                '{0}:{1}:{2}'.format(end_filename,
                                     end_firstlineno,
                                     end_function),
                color=color,
                ltail=start_subgraph.name,
                lhead=end_subgraph.name,
                label='#{0} at {1}'.format(index + 1, start_lineno)
            )

    file = os.path.abspath('stack.png')
    open(file, 'w').close()
    g.draw(file, prog='dot')
    g.close()
    if not slient:
        webbrowser.open('file://' + file)

    return file
